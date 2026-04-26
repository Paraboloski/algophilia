import json
import yaml
from pathlib import Path
from aiosqlite import Connection
from app.middleware import Result, Ok, SQliteError, async_result_wrap
from app.events.logger import Logger


class Seeder:
    def __init__(self, conn: Connection, tables: dict[str, Path], logger: Logger) -> None:
        self._connection = conn
        self._tables = tables
        self._logger = logger

    def _open(self, path: Path) -> list[dict]:
        with open(path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or []

    @async_result_wrap
    async def seed(self) -> Result[bool, SQliteError]:
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
                    self._logger.debug(f"SQL Seed: {query} | Params: {tuple(row.values())}")
                    await self._connection.execute(query, tuple(row.values()))

                    table_count += 1
                except Exception as e:
                    self._logger.error(f"Seeder: Errore riga in {table}", e)
                    total_skipped += 1

            self._logger.debug(f"Seeder: {table} -> {table_count} righe inserite")
            total_inserted += table_count

        await self._connection.commit()
        self._logger.debug(f"Seed completato: {total_inserted} totali, {total_skipped} saltate")
        return Ok(True)
