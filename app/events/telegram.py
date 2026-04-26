import html
import requests
from app.middleware.result import Ok
from app.models import Log, LogLevel
from app.middleware import result_wrap, Result
from requests.exceptions import RequestException


class Telegram:
    def __init__(self, token: str, chat_id: str):
        self._token = token
        self._chat_id = chat_id
        self._base_url = f"https://api.telegram.org/bot{self._token}/sendMessage"

    @result_wrap
    def send(self, log: Log) -> Result[bool, RequestException]:

        if log.level not in (LogLevel.ERROR, LogLevel.WARNING):
            return Ok(True)

        payload = {
            "chat_id": self._chat_id,
            "text": html.escape(str(log)),
            "parse_mode": "HTML"
        }

        response = requests.post(self._base_url, json=payload, timeout=5)
        response.raise_for_status()
        return Ok(True)
