import json
import aiosqlite
from app.config.logger import logger
from app.core.result import Ok, Err, Result
from app.core.exception import ConnectionError

from app.services.registry import (
    feats, items, souls, armors, spells, weapons,
    origins, conditions, accessories, knowledges, weapon_tags,
)

REGISTRY = {
    "weapon_tags": (weapon_tags, ["key", "name", "description"]),
    "feats":       (feats,       ["key", "name", "description"]),
    "origins":     (origins,     ["key", "name", "description"]),
    "conditions":  (conditions,  ["key", "name", "description"]),
    "items":       (items,       ["key", "name", "description", "weight"]),
    "knowledges":  (knowledges,  ["key", "name", "attribute", "description"]),
    "accessories": (accessories, ["key", "name", "description", "weight", "can_be_removed"]),
    "souls":       (souls,       ["key", "name", "month", "description", "soul_trait"]),
    "weapons":     (weapons,     ["key", "name", "description", "weight", "base_damage", "two_hand_damage", "weapon_tags"]),
    "spells":      (spells,      ["key", "name", "description", "affinity_with_god", "required_affinity_level", "enhanced_effect"]),
    "armors":      (armors,      ["key", "name", "description", "weight", "defence", "penalty", "slashing_defence", "blunt_defence", "piercing_defence"]),
}


class DataSeeder:
    _conn: aiosqlite.Connection | None

    async def seed(self) -> Result[None]:
        if self._conn is None:
            logger.error("Seed avviato senza connessione attiva")
            return Err(ConnectionError("Non connesso"))
        logger.info("Seed in corso...")
        try:
            seeded = 0
            for table, (registry, columns) in REGISTRY.items():
                if not await self._table_exists(table):
                    logger.error(f"Tabella '{table}' non trovata — schema non applicato?")
                    return Err(ConnectionError(f"Tabella '{table}' non trovata — schema non applicato?"))
                if not await self._is_table_empty(table):
                    logger.debug(f"Tabella '{table}' già popolata, skip")
                    continue
                if not registry:
                    logger.warning(f"Registry '{table}' vuoto, skip")
                    continue

                placeholders = ", ".join("?" * len(columns))
                sql  = f"INSERT OR IGNORE INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
                rows = [
                    tuple(self._extract(model, col) for col in columns)
                    for model in registry.values()
                ]
                await self._conn.executemany(sql, rows)
                logger.debug(f"'{table}' — {len(rows)} record inseriti")
                seeded += len(rows)

            await self._conn.commit()
            logger.info(f"Seed completato — {seeded} record totali")
            return Ok(None)
        except Exception as e:
            logger.error("Seed fallito", exc=e)
            return Err(ConnectionError(f"Seed fallito: {e}"))

    async def _table_exists(self, table: str) -> bool:
        if self._conn is None:
            return False
        async with self._conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ) as q:
            return await q.fetchone() is not None

    async def _is_table_empty(self, table: str) -> bool:
        if self._conn is None:
            return True
        async with self._conn.execute(f"SELECT count(*) FROM {table}") as cursor:
            row = await cursor.fetchone()
            return row[0] == 0 if row else True

    def _extract(self, model, column: str):
        value = getattr(model, column, None)
        if value is None:                        return None
        if hasattr(value, "value"):              return value.value
        if isinstance(value, (list, dict)):      return json.dumps(value)
        if hasattr(value, "model_dump"):         return json.dumps(value.model_dump())
        return value