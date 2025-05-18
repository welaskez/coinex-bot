import logging
from pathlib import Path

from pydantic import AmqpDsn, BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class CoinexAPIConfig(BaseModel):
    base_url: str = "https://rates.coinex.kg"
    api_key: str


class RabbitMQConfig(BaseModel):
    url: AmqpDsn


class RedisConfig(BaseModel):
    host: str
    port: int
    decode_responses: bool = True


class LoggingConfig(BaseModel):
    format: str = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    level: int = logging.INFO


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        env_prefix="BOT_CONFIG__",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="allow",
    )

    bot_token: str
    redis: RedisConfig
    db: DatabaseConfig
    rmq: RabbitMQConfig
    coinex: CoinexAPIConfig
    log: LoggingConfig = LoggingConfig()
    channel_id: str


settings = Settings()
