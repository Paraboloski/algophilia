class AppError(Exception):
    def __init__(self, message: str = "Errore Applicativo"):
        super().__init__(message)
        self._message = message

class EnvError(AppError):
    def __init__(self, variable: str):
        message = f"Variabile d'ambiente mancante o non valida: {variable}"
        super().__init__(message)
        self._var = variable

class ConnectionError(AppError):
    def __init__(self, url: str, action: str = "connessione", details: str = ""):
        message = f"Errore durante la {action} a: {url}"
        if details:
            message += f" | Dettagli: {details}"
        super().__init__(message)
        self._url = url
        self._action = action
        self._details = details
        
class QueryError(AppError):
    def __init__(self, query: str, details: str = ""):
        message = f"Errore SQLite nella query: {query}"
        if details:
            message += f" | Dettagli: {details}"
        super().__init__(message)
        self._query = query
        self._details = details
        
class TelegramError(AppError):
    def __init__(self, action: str, details: str = ""):
        message = f"Errore Telegram durante {action}"
        if details:
            message += f" | Dettagli: {details}"
        super().__init__(message)