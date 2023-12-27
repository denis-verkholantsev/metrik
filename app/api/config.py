from fastapi import FastAPI
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="API_",
        frozen=True,
    )

    DEBUG: bool = Field(default=False)
    TITLE: str = Field(default="metrik")
    DESCRIPTION: str = Field(default="Metrik API")
    VERSION: str = Field(default="0.1.0")
    ROOT_PATH: str = Field(default="")

    CORS_ALLOW_ORIGINS: list[str] = Field(default=["*"])
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: list[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: list[str] = Field(default=["*"])

    def init_fastapi(self) -> FastAPI:
        return FastAPI(
            debug=self.DEBUG,
            title=self.TITLE,
            description=self.DESCRIPTION,
            version=self.VERSION,
            root_path=self.ROOT_PATH,
        )
