import json
from app.config.logger import logger
from app.data.database import Database
from app.core.exception import DataError
from app.core.result import Ok, Err, Result

from app.services.registry import (
    feats, items, souls, armors, spells, weapons,
    origins, conditions, accessories, knowledges, weapon_tags,
)

SEED_DATA = {
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

async def seed_database(db: Database) -> Result[None]:
    if db.connection is None:
        logger.error("Seed avviato senza connessione attiva")
        return Err(DataError("Non connesso"))
    logger.info("Seed in corso...")
    try:
        seeded = 0
        for table, (registry, columns) in SEED_DATA.items():
            if not await _table_exists(db, table):
                logger.error(f"Tabella '{table}' non trovata — schema non applicato?")
                return Err(DataError(f"Tabella '{table}' non trovata — schema non applicato?"))
            if not await _is_table_empty(db, table):
                logger.debug(f"Tabella '{table}' già popolata, skip")
                continue
            if not registry:
                logger.warning(f"Registry '{table}' vuoto, skip")
                continue

            placeholders = ", ".join("?" * len(columns))
            sql  = f"INSERT OR IGNORE INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            rows = []
            for model in registry.values():
                dumped = model.model_dump(mode="json")
                rows.append(tuple(
                    json.dumps(dumped.get(col)) if isinstance(dumped.get(col), (list, dict)) else dumped.get(col)
                    for col in columns
                ))

            await db.connection.executemany(sql, rows)
            logger.debug(f"'{table}' — {len(rows)} record inseriti")
            seeded += len(rows)

        await db.connection.commit()
        logger.info(f"Seed completato — {seeded} record totali")
        return Ok(None)
    except Exception as e:
        logger.error("Seed fallito", exc=e)
        return Err(DataError(f"Seed fallito: {e}"))

async def _table_exists(db: Database, table: str) -> bool:
    if db.connection is None:
        return False
    async with db.connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ) as q:
        return await q.fetchone() is not None

async def _is_table_empty(db: Database, table: str) -> bool:
    if db.connection is None:
        return True
    async with db.connection.execute(f"SELECT 1 FROM {table} LIMIT 1") as cursor:
        return await cursor.fetchone() is None