# Copyright (c) 2023 Artem Ustsov

from common.exceptions import ValidationError


def validate_username(username: str) -> None:
    """Check the user's nickname for correctness"""

    if not 3 < len(username) < 15:
        raise ValidationError('Username must be least 3 characters and no longer than 15 characters')
    if ' ' in username:
        raise ValidationError('The username must not contain spaces')


def validate_message_delay(delay: str):
    """Check the message sending delay for correctness"""

    if not delay.isdigit():
        raise ValidationError('Delay must be an integer')
    if int(delay) < 0:
        raise ValidationError('Delay must be a positive number')
