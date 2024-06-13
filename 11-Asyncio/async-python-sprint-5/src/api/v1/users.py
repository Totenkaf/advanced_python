from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from common.logger import get_logger
from db.db import get_session
from schemas import users as schema_users
from services.users import token_crud, user_crud
from services.utils import validate_password

router = APIRouter()
LOG = get_logger()


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=schema_users.UserID,
    description='Registering a new user.',
)
async def register_user(
    user: schema_users.UserCreate,
    db: AsyncSession = Depends(get_session),
) -> schema_users.UserID:
    answer = await user_crud.add_user(db=db, obj_in=user)
    LOG.info('New user %s registered.', answer.login)
    return schema_users.UserID(id=answer.id, login=answer.login)


@router.post(
    '/auth',
    status_code=status.HTTP_201_CREATED,
    response_model=schema_users.UserToken,
    description='Authenticating user and getting a token.',
)
async def auth_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
) -> schema_users.UserToken:
    LOG.info('Get user %s by login', form_data.username)
    user = await user_crud.get_user_by_name(db=db, login=form_data.username)
    if (not user
            or not validate_password(
                user.hashed_password,
                form_data.password
            )):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong login or password."
        )
    LOG.info('Creating token for %s', form_data.username)
    token = await token_crud.create_token(db=db, id=user.id)
    LOG.info('Auth token for %s successfully created', form_data.username)
    return schema_users.UserToken(
        access_token=token.token,
        expires=token.expires
    )
