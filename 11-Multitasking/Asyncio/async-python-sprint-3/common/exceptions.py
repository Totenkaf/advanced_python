# Copyright (c) 2023 Artem Ustsov

class ObjectDoesNotExist(Exception):
    """Specific exception for notify is object is not exist"""
    pass


class ValidationError(Exception):
    """Specific exception for notify is validation is fall"""
    pass
