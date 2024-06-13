# Copyright (c) 2023 Artem Ustsov

import asyncio
import getopt
import random
from typing import Callable

from common.base import DEFAULT_USERNAMES


async def execute_later(func: Callable, delay: int, *args, **kwargs) -> None:
    await asyncio.sleep(delay)
    if asyncio.iscoroutinefunction(func):
        await func(*args, **kwargs)
    else:
        func(*args, **kwargs)


def generate_random_name() -> str:
    return random.choice(DEFAULT_USERNAMES) + str(random.randint(0, 10000))


def parse_opts(query: str) -> tuple[str, str, str]:
    options = getopt.getopt(query.split(), 'u:t:', ['username=', 'time='])[0]
    options = dict(options)
    receiver_username = options.get('-u') or options.get('--username')
    delay = options.get('-t') or options.get('--time')
    message = query.replace(f'-u {receiver_username}', '').replace(f'--username {receiver_username}', '')
    message = message.replace(f'-t {delay}', '').replace(f'--time {delay}', '')
    return receiver_username, delay, message.strip()


def print_update(update: 'Update') -> None:
    match update.status:
        case 'ERROR':
            message = f'\033[1;31;40m[ERROR]: {update.data["message"]}'
        case 'OK':
            message = f'\033[1;32;40m{update.data["message"]}'
        case 'MSG':
            from_user = update.data['sender']
            target = update.data['target']
            text = update.data['text']
            if target == 'BROADCAST':
                message = f'\033[1;34;40m[BROADCAST] {from_user} >>> {text}'
            else:
                message = f'\033[1;35;40m[PRIVATE] {from_user} >>> {text}'
        case _:
            message = 'Undefined message'
    print(message)
