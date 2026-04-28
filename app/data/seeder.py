import json
import yaml
from pathlib import Path
from result import Ok, Err, Result
from app.events.logger import Logger
from aiosqlite import Error, Connection
from app.utils.exception import AppError, QueryError

class Seeder:
    def __init__(self, conn: Connection, tables: dict[str, Path], logger: Logger) -> None:
        self._tables = tables
        self._logger = logger
        self._connection = conn

    def _open(self, path: Path) -> list[dict]:
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data if data is not None else []

    async def seed(self) -> Result[bool, AppError]:
        total_inserted = 0
        total_skipped = 0

        for table, path in self._tables.items():
            rows = self._open(path)
            
            if not rows:
                self._logger.warn(f"Seeder: {table} è vuoto o mancante")
                continue

            table_count = 0
            for row in rows:
                try:
                    for key, value in row.items():
                        if isinstance(value, (list, dict)):
                            row[key] = json.dumps(value)

                    columns = ", ".join(row.keys())
                    placeholders = ", ".join(["?"] * len(row))
                    query = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
                    params = tuple(row.values())

                    self._logger.debug(f"SQL Seed: {query}")
                    await self._connection.execute(query, params)
                    
                    table_count += 1
                
                except Error as e:
                    self._logger.error(f"Seeder: Errore SQLite nella tabella {table}: {e}")
                    total_skipped += 1

            self._logger.info(f"Seeder: {table} -> {table_count} righe elaborate")
            total_inserted += table_count

        try:
            await self._connection.commit()
        except Error as e:
            return Err(QueryError(query="COMMIT Seeder", details=str(e)))

        self._logger.info(f"Seed completato: {total_inserted} inseriti, {total_skipped} saltati")
        return Ok(True)
