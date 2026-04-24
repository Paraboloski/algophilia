import aiosqlite
from typing import Literal
from app.config.logger import logger
from app.core.result import Ok, Err, Result
from app.core.exception import ExecutionError, ConnectionError

class QueryExecutor:
    _conn: aiosqlite.Connection | None

    async def execute(
        self,
        sql: str,
        params: tuple = (),
        fetch: Literal["all", "one", "none"] = "none",
    ) -> Result[list[aiosqlite.Row] | aiosqlite.Row | None | int]:
        if self._conn is None:
            logger.error("Esecuzione query senza connessione attiva")
            return Err(ConnectionError("Non connesso"))
        try:
            logger.debug(f"[{fetch.upper()}] {sql.strip()} | params={params}")
            async with self._conn.execute(sql, params) as cursor:
                if fetch == "all":
                    rows = list(await cursor.fetchall())
                    logger.debug(f"{len(rows)} righe restituite")
                    return Ok(rows)
                if fetch == "one":
                    row = await cursor.fetchone()
                    logger.debug(f"{'1 riga restituita' if row else 'Nessuna riga trovata'}")
                    return Ok(row)
                await self._conn.commit()
                logger.debug(f"Scrittura completata — lastrowid={cursor.lastrowid or 0}")
                return Ok(cursor.lastrowid or 0)
        except Exception as e:
            logger.error(f"Query fallita: {sql.strip()}", exc=e)
            return Err(ExecutionError("Query fallita: ", e))