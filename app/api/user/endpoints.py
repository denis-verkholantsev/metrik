from fastapi import APIRouter, status
from pydantic import SecretStr

from app.api.dependencies import (
    JWTServiceDependency,
    OAuth2PasswordRequestFormDependency,
    PasswordHasherServiceDependency,
    RequestAuthorDependency,
    UserRepositoryDependency,
)
from app.api.user.contracts import (
    BearerTokenResponse,
    PostRegisterRequestBody,
    UpdateUserPasswordBody,
    UpdateUserRequestBody,
    UserEntityResponse,
    UserEntityResponseWithToken,
)
from app.core.user.errors import (
    InvalidNewPasswordError,
    UserNotFoundError,
    UserPasswordMismatchError,
)

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserEntityResponseWithToken,
    response_model_exclude_defaults=True,
)
async def post_user_register(
    body: PostRegisterRequestBody,
    user_repository: UserRepositoryDependency,
    jwt_service: JWTServiceDependency,
    password_hasher_service: PasswordHasherServiceDependency,
):
    user_info = body.to_user_info()
    user_info.password = password_hasher_service.hash_password(user_info.password)

    user_entity = await user_repository.insert_one(user_info)

    token = jwt_service.generate_token(user_entity)

    return UserEntityResponseWithToken.from_user_entity_and_token(
        user_entity,
        token.decode(),
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=BearerTokenResponse,
)
async def post_user_login(
    form_data: OAuth2PasswordRequestFormDependency,
    user_repository: UserRepositoryDependency,
    jwt_service: JWTServiceDependency,
    password_hasher_service: PasswordHasherServiceDependency,
):
    user = await user_repository.select_one(
        username=form_data.username,
    )

    if user is None:
        raise UserNotFoundError()

    if not password_hasher_service.compare_passwords(
        SecretStr(form_data.password),
        user.info.password,
    ):
        raise UserPasswordMismatchError()

    token = jwt_service.generate_token(user)

    return BearerTokenResponse(access_token=token.decode())


@router.put(
    "",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def put_user(
    body: UpdateUserRequestBody,
    user_repository: UserRepositoryDependency,
    request_author: RequestAuthorDependency,
):
    result = await user_repository.update_one_info(
        request_author, body.to_user_info_update()
    )

    if not result:
        raise UserNotFoundError()


@router.put(
    "/password",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def put_user_password(
    body: UpdateUserPasswordBody,
    user_repository: UserRepositoryDependency,
    password_hasher: PasswordHasherServiceDependency,
    request_author: RequestAuthorDependency,
):
    update = body.to_user_password_update()

    user = await user_repository.select_one(uid=request_author)

    if not user:
        raise UserNotFoundError()

    if not password_hasher.compare_passwords(update.old_password, user.info.password):
        raise UserPasswordMismatchError()

    if update.new_password.get_secret_value() == update.old_password.get_secret_value():
        raise InvalidNewPasswordError()

    hashed_password = password_hasher.hash_password(update.new_password)
    result = await user_repository.update_one_password(request_author, hashed_password)

    if result is None:
        raise UserNotFoundError()


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserEntityResponse,
)
async def get_user_me(
    authorization_token: RequestAuthorDependency,
    user_repository: UserRepositoryDependency,
):
    user = await user_repository.select_one(uid=authorization_token)

    if user is None:
        raise UserNotFoundError()

    return UserEntityResponse.from_user_entity(entity=user)
