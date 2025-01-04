import asyncio
import contextvars
import random

# Определяем контекстные переменные
user_context = contextvars.ContextVar('user_context')
request_id_context = contextvars.ContextVar('request_id_context')


def log_message(message):
    user = user_context.get("Unknown User")
    request_id = request_id_context.get("Unknown Request ID")
    print(f"User: {user}, Request ID: {request_id}: {message}")


async def login():
    log_message("User logged in")
    await asyncio.sleep(random.random())


async def perform_work():
    log_message("Performing work")
    await asyncio.sleep(random.random())


async def logout():
    log_message("User logged out")
    await asyncio.sleep(random.random())


async def handle_user_request(user_id, request_id):
    user_token = user_context.set(user_id)
    request_id_token = request_id_context.set(request_id)
    try:
        await login()
        await perform_work()
        await logout()
    finally:
        user_context.reset(user_token)
        request_id_context.reset(request_id_token)


async def main():
    users_requests = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    tasks = []
    for user, req_id in users_requests:
        task = asyncio.create_task(handle_user_request(user, req_id))
        tasks.append(task)
    await asyncio.gather(*tasks)
    log_message('Unknown')


asyncio.run(main())