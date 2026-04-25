import sys
from app.config.logger import logger

class Panic:
    @staticmethod
    def _panic(message: str) -> None:
        logger.error(f"CRITICAL PANIC: {message}")
        logger.shutdown()
        sys.exit(1)
