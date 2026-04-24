from pathlib import Path
from app.core.environment import Env

_DIR       = Path(__file__).resolve().parent.parent.parent
_TEMPLATES = _DIR / "assets" / "templates"

_env = Env()

class Settings:
    APP_PAGE_WIGHT  = 402
    APP_PAGE_HEIGHT = 874

    APP_NAME = "Algophilia"

    APP_PAGE_BG_COLOR   = "#1A1A1A"
    APP_PAGE_MAIN_COLOR = "#AB3326"

    APP_PAGE_BG_FALLBACK_IMG = "/images/background/fallback.png"

    FONT_CINZEL_BOLD      = "/fonts/Cinzel-Bold.ttf"
    FONT_CINZEL_BLACK     = "/fonts/Cinzel-Black.ttf"
    FONT_CINZEL_MEDIUM    = "/fonts/Cinzel-Medium.ttf"
    FONT_CINZEL_REGULAR   = "/fonts/Cinzel-Regular.ttf"
    FONT_CINZEL_SEMIBOLD  = "/fonts/Cinzel-SemiBold.ttf"
    FONT_CINZEL_EXTRABOLD = "/fonts/Cinzel-ExtraBold.ttf"

    SCHEMA_PATH            = _TEMPLATES / "schema.sql"
    STATIC_ITEM_PATH       = _TEMPLATES / "static_item.yaml"
    STATIC_SOUL_PATH       = _TEMPLATES / "static_soul.yaml"
    STATIC_STAT_PATH       = _TEMPLATES / "static_stat.yaml"
    STATIC_SKILL_PATH      = _TEMPLATES / "static_skill.yaml"
    STATIC_ORIGIN_PATH     = _TEMPLATES / "static_origin.yaml"
    STATIC_CONDITION_PATH  = _TEMPLATES / "static_condition.yaml"
    STATIC_KNOWLEDGE_PATH  = _TEMPLATES / "static_knowledge.yaml"
    STATIC_WEAPON_TAG_PATH = _TEMPLATES / "static_weapon_tag.yaml"

    DATABASE_PATH: Path = Path(
        _env.string("DATABASE_URL").unwrap_or("store/algophilia.db").replace("sqlite:///", "")
    )

settings = Settings()