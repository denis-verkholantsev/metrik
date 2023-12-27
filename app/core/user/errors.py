from app.common.errors import AppError


class UserNotFoundError(AppError):
    error_message = "user not found"


class UserPasswordMismatchError(AppError):
    error_message = "password mismatch"


class UserDuplicateEmailOrUsernameError(AppError):
    error_message = "attempted to insert user with duplicating email or username"


class InvalidSelectUserQueryParametersError(AppError):
    error_message = "cannot select user without email, username or id"


class InvalidNewPasswordError(AppError):
    error_message = "cannot update password as old is matching new one"
