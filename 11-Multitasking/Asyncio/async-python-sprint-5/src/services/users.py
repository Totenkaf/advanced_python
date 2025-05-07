from models.users import Token, User
from schemas.users import UserCreate

from services.base import RepositoryDBToken, RepositoryDBUser


class RepositoryUsers(RepositoryDBUser[User, UserCreate]):
    pass


user_crud = RepositoryUsers(User)
token_crud = RepositoryDBToken(Token)
