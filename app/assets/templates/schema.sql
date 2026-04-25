CREATE TABLE IF NOT EXISTS weapon_tags (
    name TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT ''
);


CREATE TABLE IF NOT EXISTS weapons (
    name TEXT NOT NULL,
    two_hand_damage TEXT NOT NULL,
    base_damage TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT '',
    weapon_tags TEXT NOT NULL DEFAULT '[]',
    weight INTEGER NOT NULL CHECK (weight >= 0)
);

CREATE INDEX IF NOT EXISTS idx_weapons_name ON weapons (name);


CREATE TABLE IF NOT EXISTS armors (
    name TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT '',
    weight INTEGER NOT NULL CHECK (weight >= 0),
    defence INTEGER NOT NULL CHECK (defence >= 0),
    penalty INTEGER NOT NULL CHECK (penalty >= 0),
    piercing_defence INTEGER NOT NULL DEFAULT 0 CHECK (piercing_defence IN (0, 1)),
    slashing_defence INTEGER NOT NULL DEFAULT 0 CHECK (slashing_defence IN (0, 1)),
    blunt_defence INTEGER NOT NULL DEFAULT 0 CHECK (blunt_defence IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_armors_defence ON armors (defence);

CREATE INDEX IF NOT EXISTS idx_armors_defences ON armors (
    slashing_defence,
    blunt_defence,
    piercing_defence
);


CREATE TABLE IF NOT EXISTS accessories (
    name TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT '',
    weight INTEGER NOT NULL CHECK (weight >= 0),
    can_be_removed INTEGER NOT NULL DEFAULT 1 CHECK (can_be_removed IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_accessories_removable ON accessories (can_be_removed);


CREATE TABLE IF NOT EXISTS items (
    name TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT '',
    weight INTEGER NOT NULL CHECK (weight >= 0)
);
CREATE INDEX IF NOT EXISTS idx_items_name ON items (name);


CREATE TABLE IF NOT EXISTS feats (
    name TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_feats_name ON feats (name);


CREATE TABLE IF NOT EXISTS spells (
    name TEXT NOT NULL,
    affinity_with_god TEXT NOT NULL,
    enhanced_effect TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT '',
    required_affinity_level INTEGER NOT NULL CHECK (required_affinity_level >= 1)
);

CREATE INDEX IF NOT EXISTS idx_spells_god ON spells (affinity_with_god);

CREATE INDEX IF NOT EXISTS idx_spells_affinity_level ON spells (required_affinity_level);

CREATE INDEX IF NOT EXISTS idx_spells_god_level ON spells (affinity_with_god, required_affinity_level);


CREATE TABLE IF NOT EXISTS knowledges (
    name TEXT NOT NULL,
    attribute TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_knowledges_name ON knowledges (name);

CREATE INDEX IF NOT EXISTS idx_knowledges_attribute ON knowledges (attribute);


CREATE TABLE IF NOT EXISTS souls (
    name TEXT NOT NULL,
    soul_trait TEXT NOT NULL,
    month TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_souls_month ON souls (month);


CREATE TABLE IF NOT EXISTS origins (
    name TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_origins_name ON origins (name);


CREATE TABLE IF NOT EXISTS conditions (
    name TEXT NOT NULL,
    key TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_conditions_name ON conditions (name);


CREATE TABLE IF NOT EXISTS characters (
    info TEXT NOT NULL,
    stats TEXT NOT NULL,
    skills TEXT NOT NULL,
    inventory TEXT NOT NULL,
    body_parts TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 1 CHECK (level >= 1),
    conditions TEXT NOT NULL DEFAULT '[]',
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_cache TEXT GENERATED ALWAYS AS (json_extract(info, '$.name')) VIRTUAL
);

CREATE INDEX IF NOT EXISTS idx_characters_level ON characters (level);

CREATE INDEX IF NOT EXISTS idx_characters_name ON characters (name_cache);