from pathlib import Path
from app.data.seeder import Seeder
from result import Result, Err, Ok
from app.events.logger import Logger
from aiosqlite import Connection, connect, Error
from app.utils.exception import AppError, ConnectionError, QueryError

class Database:
    def __init__(
        self,
        url: str,
        sql: str,
        yaml: list[Path],
        logger: Logger
    ) -> None:
        self._logger = logger
        self._sqlite_url = url
        self._sql_schema = sql
        self._yaml_seed = yaml
        self._connection: Connection | None = None

    def get_connection(self) -> Result[Connection, ConnectionError]:
        if not self._connection:
            exception = ConnectionError(
                url=self._sqlite_url, 
                action="get connection", 
                details="Connessione non inizializzata. Richiesto start()."
            )
            self._logger.error(str(exception))
            return Err(exception)
            
        return Ok(self._connection)

    async def start(self) -> Result[bool, AppError]:
        try:
            self._connection = await connect(self._sqlite_url)
            self._logger.info(f"Database: Connessione riuscita a {self._sqlite_url}")
        except Error as e:
            exception = ConnectionError(self._sqlite_url, action="connessione", details=str(e))
            self._logger.error(str(exception))
            return Err(exception)

        if self._sql_schema:
            try:
                with open(self._sql_schema, "r", encoding="utf-8") as file:
                    script = file.read()
                
                await self._connection.executescript(script)
                self._logger.info(f"Database: Schema SQL {Path(self._sql_schema).name} applicato")
            
            except Error as e:
                exception = QueryError(query=f"Schema SQL: {self._sql_schema}", details=str(e))
                self._logger.error(str(exception))
                await self.disconnect() 
                return Err(exception)
            
        tables = {}

        for path in self._yaml_seed:
            if path.exists():
                file_name = path.name 
                table_name = file_name.replace(".yaml", "").replace(".yml", "")
                tables[table_name] = path
            else:
                self._logger.warn(f"Database: File {path} non trovato, salto il seeding per questa tabella.")
            
        if tables:
            try:
                seeder = Seeder(self._connection, tables, self._logger)
                await seeder.seed()
            except Error as e:
                exception = QueryError(query="Seeding YAML", details=str(e))
                self._logger.error(str(exception))
                await self.disconnect()
                return Err(exception)

        return Ok(True)

    async def disconnect(self) -> Result[bool, ConnectionError]:
        if self._connection:
            try:
                await self._connection.close()
            except Error as e:
                exception = ConnectionError(self._sqlite_url, action="disconnessione", details=str(e))
                self._logger.error(str(exception))
                return Err(exception)
            finally:
                self._connection = None
                
        return Ok(True)
