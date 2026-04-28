import os
from result import Err, Ok, Result
from app.utils.exception import EnvError
from dotenv import find_dotenv, load_dotenv

if os.getenv("ENV") != "PRODUCTION":
    load_dotenv(find_dotenv())

class Environment:
    def get_env(self, key: str) -> Result[str, EnvError]:
        value = os.getenv(key)

        if value is None:
            return Err(EnvError(key))

        return Ok(value)

    def require(self, key: str) -> str:
        result = self.get_env(key)

        if isinstance(result, Err):
            raise result.unwrap()

        return result.value