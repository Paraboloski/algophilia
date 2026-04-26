from pathlib import Path
from app.data.seed import Seeder
from abc import ABC, abstractmethod
from aiosqlite import connect, Connection
from app.middleware import Result, Ok, SQliteError, async_result_wrap
from app.events.logger import Logger


class Database(ABC):
    def __init__(
        self,
        db_url: str,
        sql_schema: str,
        yaml_files: list[Path],
        logger: Logger
    ) -> None:

        self._db_url = db_url
        self._sql_path = sql_schema
        self._yaml_files = yaml_files
        self._logger = logger
        self._connection: Connection | None = None

    @async_result_wrap
    async def start(self) -> Result[bool, SQliteError]:
        self._connection = await connect(self._db_url)
        self._logger.info(f"Database: Connessione riuscita a {self._db_url}")

        if self._sql_path:
            with open(self._sql_path, "r", encoding="utf-8") as file:
                await self._connection.executescript(file.read())
            self._logger.info(f"Database: Schema {Path(self._sql_path).name} applicato")

        tables = {}
        for path in self._yaml_files:
            if path.exists():
                tables[path.stem] = path

        if tables:
            seeder = Seeder(self._connection, tables, self._logger)
            await seeder.seed()

        return Ok(True)

    @abstractmethod
    async def execute(self, query: str, params: tuple = ()) -> Result[bool, SQliteError]:
        ...

    @abstractmethod
    async def execute_all(self, queries: list[tuple[str, tuple]]) -> Result[bool, SQliteError]:
        ...

    @async_result_wrap
    async def disconnect(self) -> Result[bool, SQliteError]:
        if self._connection is not None:
            await self._connection.close()
            self._connection = None
        return Ok(True)


class Executor(Database):
    @async_result_wrap
    async def execute(self, query: str, params: tuple = ()) -> Result[bool, SQliteError]:
        if not self._connection:
            exc = "Database non connesso"
            self._logger.error(exc)
            raise SQliteError(exc)
        
        self._logger.debug(f"SQL Execute: {query} | Params: {params}")
        await self._connection.execute(query, params)
        await self._connection.commit()
        return Ok(True)

    @async_result_wrap
    async def execute_all(self, queries: list[tuple[str, tuple]]) -> Result[bool, SQliteError]:
        if not self._connection:
            exc = "Database non connesso"
            self._logger.error(exc)
            raise SQliteError(exc)
        
        async with self._connection.cursor() as cursor:
            for query, params in queries:
                self._logger.debug(f"SQL Execute All: {query} | Params: {params}")
                await cursor.execute(query, params)
        await self._connection.commit()
        return Ok(True)
