from typing import Any


class AppError(Exception):
    error_message: str
    error_code: str
    meta: dict[str, Any]

    def __init__(self, **kwargs):
        self.meta = kwargs
        self.error_code = self.__class__.__name__.replace("Error", "")
        self.error_message = self.error_message.format(**kwargs)
