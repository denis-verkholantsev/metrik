from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EdgeDBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="EDGEDB_",
        frozen=True,
    )

    DSN: str = Field(default="edgedb://localhost:5656")
    TLS_SECURITY: str = Field(default="insecure")
