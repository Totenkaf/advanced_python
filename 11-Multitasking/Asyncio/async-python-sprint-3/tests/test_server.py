# Copyright (c) 2023 Artem Ustsov

import asyncio

import pytest

from client.client import Client
from config import Settings
from server.server import Server
from server.models import Gateway, Message

settings = Settings()


@pytest.mark.asyncio
async def test_server_able_to_start_and_stop() -> None:
    server = Server(settings.SERVER_HOST, settings.SERVER_PORT)
    await server.start()
    assert isinstance(server, Server)
    assert isinstance(server._server, asyncio.Server)
    assert server._server.sockets[0].getsockname() == (settings.SERVER_HOST, settings.SERVER_PORT)
    await server.stop()
    assert server._server is None


@pytest.mark.asyncio
async def test_client_able_to_connect_to_server(server: Server, clients: list[Client]) -> None:
    assert Gateway.objects.count() == 0
    async with clients[0] as client:
        await asyncio.sleep(0.1)
        assert Gateway.objects.count() == 1
        assert client._transport._writer.get_extra_info('peername') == (settings.SERVER_HOST, settings.SERVER_PORT)


@pytest.mark.asyncio
async def test_client_able_to_send_message_to_server(server: Server, clients: list[Client]) -> None:
    assert Message.objects.count() == 0
    expected_message = 'hello server!'
    async with clients[0] as client:
        await client.send(f'send {expected_message}')
        await asyncio.sleep(0.3)
        assert Message.objects.count() == 1
        assert Message.objects.get(text=expected_message)
        assert Message.objects.get(text=expected_message).target == Gateway.BROADCAST
        assert Message.objects.get(text=expected_message).sender == Gateway.objects.first()


@pytest.mark.asyncio
async def test_client_able_to_send_message_to_another_client(server: Server, clients: list[Client]) -> None:
    amount_of_msg = len(Message.objects.all())
    expected_message = 'hello client!'
    async with clients[0] as client1, clients[1]:
        user1 = Gateway.objects.first()
        user2 = Gateway.objects.last()
        await client1.send(f'send -u {user2.username} {expected_message}')
        await asyncio.sleep(0.3)
        assert amount_of_msg + 1 == Message.objects.count()
        assert Message.objects.get(text=expected_message)
        message = Message.objects.get(text=expected_message)
        assert message.sender == user1
        assert message.target == user2


@pytest.mark.asyncio
async def test_client_unable_to_send_message_to_another_client_with_wrong_username(
    server: Server,
    clients: list[Client],
) -> None:

    expected_message = 'hello client!'
    async with clients[0] as client1:
        await client1.send(f'send -u not_actual_name {expected_message}')
        await asyncio.sleep(0.3)
        assert Message.objects.count() == 0


@pytest.mark.asyncio
async def test_client_able_to_schedule_message(server: Server, clients: list[Client]) -> None:
    expected_message = 'hello client!'
    async with clients[0] as client1, clients[1]:
        user1 = Gateway.objects.first()
        user2 = Gateway.objects.last()
        assert Message.objects.count() == 0

        await client1.send(f'send -u {user2.username} -t 2 {expected_message}')
        await asyncio.sleep(0.3)
        assert Message.objects.count() == 1
        assert Message.objects.get(text=expected_message)
        message = Message.objects.get(text=expected_message)
        assert message.status == 'PENDING'
        assert message.sender == user1
        assert message.target == user2

        await asyncio.sleep(2)
        assert message.status == 'FINISHED'
        assert Message.objects.count() == 1


@pytest.mark.asyncio
async def test_client_able_to_cancel_scheduled_message(server: Server, clients: list[Client]) -> None:
    expected_message = 'hello client!'
    async with clients[0] as client1, clients[1]:
        user2 = Gateway.objects.last()
        assert Message.objects.count() == 0

        await client1.send(f'send -u {user2.username} -t 2 {expected_message}')
        await asyncio.sleep(0.3)
        assert Message.objects.count() == 1
        assert Message.objects.get(text=expected_message)
        message = Message.objects.get(text=expected_message)
        assert message.status == 'PENDING'

        await client1.send(f'cancel')
        await asyncio.sleep(0.3)
        assert message.status == 'CANCELLED'
        assert Message.objects.count() == 0


@pytest.mark.asyncio
async def test_client_able_to_rename_himself(server: Server, clients: list[Client]) -> None:
    async with clients[0] as client1:
        await client1.send(f'rename new_name')
        await asyncio.sleep(0.3)
        assert Gateway.objects.get(username='new_name')
        assert Gateway.objects.count() == 1


@pytest.mark.asyncio
async def test_client_able_report_other_client(server: Server, clients: list[Client]) -> None:
    async with clients[0] as client1, clients[1]:
        good_user = Gateway.objects.first()
        bad_user = Gateway.objects.last()
        assert good_user not in bad_user.reported_by
        assert len(bad_user.reported_by) == 0

        await client1.send(f'report {bad_user.username}')
        await asyncio.sleep(0.3)

        assert good_user in bad_user.reported_by
        assert len(bad_user.reported_by) == 1


@pytest.mark.asyncio
async def test_client_able_to_be_banned_after_report(server: Server, clients: list[Client]) -> None:
    async with clients[0] as client1, clients[1] as client2, clients[2] as client3:
        bad_user = Gateway.objects.last()
        await client1.send(f'report {bad_user.username}')
        await client2.send(f'report {bad_user.username}')
        await asyncio.sleep(0.3)

        assert bad_user.is_banned
        assert len(bad_user.reported_by) == 2
        assert Message.objects.count() == 0

        await client3.send(f'send hello')
        await asyncio.sleep(0.3)
        assert Message.objects.count() == 1


@pytest.mark.asyncio
async def test_client_able_to_leave_server(server: Server, clients: list[Client]) -> None:
    async with clients[0] as client1:
        await asyncio.sleep(0.1)
        assert Gateway.objects.count() == 1
        await client1.send(f'exit')
        await asyncio.sleep(0.1)
        assert Gateway.objects.count() == 0
