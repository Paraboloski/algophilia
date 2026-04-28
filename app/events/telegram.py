import html
import requests
from result import Err, Ok, Result
from app.models import Log, LogLevel
from requests.exceptions import RequestException
from app.utils.exception import AppError, TelegramError

class Telegram:
    def __init__(self, token: str, chat_id: str):
        self._token = token
        self._chat_id = chat_id
        self._base_url = f"https://api.telegram.org/bot{self._token}/sendMessage"

    def send(self, log: Log) -> Result[bool, AppError]:
        if log.level not in (LogLevel.ERROR, LogLevel.WARNING):
            return Ok(True)

        payload = {
            "chat_id": self._chat_id,
            "text": html.escape(str(log)),
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(self._base_url, json=payload, timeout=5)
            if not response.ok:
                exception = TelegramError(
                    action="invio log", 
                    details=f"Status: {response.status_code} - {response.text}"
                )
                return Err(exception)

            return Ok(True)

        except RequestException as e:
            exception = TelegramError(action="connessione API", details=str(e))
            return Err(exception)
