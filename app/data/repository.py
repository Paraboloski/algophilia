from aiosqlite import Error
from result import Ok, Err, Result
from app.events.logger import Logger
from app.data.database import Database
from app.utils.exception import AppError, QueryError


class Repository:
    def __init__(self, db: Database, logger: Logger) -> None:
        self._database = db
        self._logger = logger

    async def execute(self, query: str, params: tuple = ()) -> Result[bool, AppError]:
        response = self._database.get_connection()
        if response.is_err():
            return Err(response.unwrap_err())
        
        conn = response.unwrap()

        try:
            self._logger.debug(f"SQL: {query} | Params: {params}")
            await conn.execute(query, params)
            await conn.commit()
            return Ok(True)
            
        except Error as e:
            exception = QueryError(query=query, details=str(e))
            self._logger.error(str(exception))
            return Err(exception)

    async def execute_all(self, queries: list[tuple[str, tuple]]) -> Result[bool, AppError]:
        response = self._database.get_connection()
        if response.is_err():
            return Err(response.unwrap_err())

        conn = response.unwrap()

        try:
            async with conn.cursor() as cursor:
                for query, params in queries:
                    self._logger.debug(f"SQL: {query} | Params: {params}")
                    await cursor.execute(query, params)
            
            await conn.commit()
            return Ok(True)

        except Error as e:
            await conn.rollback()
            exception = QueryError(query="Batch", details=str(e))
            self._logger.error(str(exception))
            return Err(exception)
