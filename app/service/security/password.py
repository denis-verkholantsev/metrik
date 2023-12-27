from bcrypt import checkpw
from passlib.handlers.bcrypt import bcrypt
from pydantic import SecretStr

from app.core.user.services import PasswordHasherService


class PasslibPasswordHasherService(PasswordHasherService):
    def hash_password(self, password: SecretStr) -> SecretStr:
        hashed_password: str = bcrypt.hash(password.get_secret_value())
        return SecretStr(hashed_password)

    def compare_passwords(
        self, input_password: SecretStr, original_password: SecretStr
    ) -> bool:
        if checkpw(
            input_password.get_secret_value().encode(),
            original_password.get_secret_value().encode(),
        ):
            return True
        return False
