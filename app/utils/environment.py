import os
import sys
from dotenv import find_dotenv, load_dotenv
from app.middleware import EnvError, Err, Ok, result_wrap

if os.getenv("ENV") != "PRODUCTION":
    load_dotenv(find_dotenv())


class Environment:

    @result_wrap
    def get_env(self, key: str) -> Ok | Err:
        value = os.getenv(key)

        if value is None:
            raise EnvError(f"Variabile d'ambiente assente: {key}")

        return Ok(value)

    def require(self, key: str) -> str:
        result = self.get_env(key)

        if isinstance(result, Err):
            sys.exit(1)

        return result.value
