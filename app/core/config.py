# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=no-self-use

import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pydantic import AnyUrl
from pydantic import (AnyHttpUrl, BaseSettings)


def load_config() -> Path:
    app_env = os.environ.get("APP_ENV", "leadhit.env")
    environ = f"{app_env}".lower()
    path = Path.cwd()
    full_path = src_path.joinpath(".deploy", ".envs", environ)
    logger.info(f"ENV_FILE: {app_env}  env: {environ}  src_path: {path}   path_file: {full_path}")
    load_dotenv(full_path)
    return path


class MongoDBDsn(AnyUrl):
    allowed_schemes = {"mongodb"}
    user_required = False


APP_ENV = os.environ.get("APP_ENV", "leadhit.env")
env = f"{APP_ENV}".lower()
src_path = Path.cwd()
path_file = src_path.joinpath(".deploy", ".envs", env)
logger.info(f"APP_ENV: {APP_ENV}  " f"env: {env}  src_path: {src_path}   path_file: {path_file}")


class LocalHost(str, Enum):
    localhost = "localhost"


class Settings(BaseSettings):
    load_dotenv(path_file)
    src_path = load_config()
    cfg_env = os.environ

    SERVER_HOST: AnyHttpUrl = AnyHttpUrl(url="", host="localhost", scheme="http")
    SERVER_PORT: int = 54002

    MONGO_URI: str = "mongodb://0.0.0.0:27017/"
    COLLECTION: str = "leadhit"


settings = Settings()
