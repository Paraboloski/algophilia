from pathlib import Path
from app.core.result import Err
from app.config.panic import Panic
from app.core.environment import Env

_DIR = Path(__file__).resolve().parent.parent.parent
_ICONS = _DIR / "app" / "assets" / "icons"
_IMAGES = _DIR / "app" / "assets" / "images"
_TEMPLATES = _DIR / "app" / "assets" / "templates"

_env = Env()


class Settings:
    APP_PAGE_WIGHT = 402
    APP_PAGE_HEIGHT = 874

    APP_NAME = "Algophilia"

    APP_PAGE_BG_LIGHT_COLOR = "#EFF6FF"
    APP_PAGE_BG_DARK_COLOR = "#15161A"
    APP_PAGE_INFO_DARK_COLOR = "#1E3A5F"
    APP_PAGE_INFO_LIGHT_COLOR = "#3B82F6"
    APP_PAGE_ERROR_DARK_COLOR = "#4A1515"
    APP_PAGE_ERROR_LIGHT_COLOR = "#AB3326"
    APP_PAGE_WARNING_DARK_COLOR = "#3D2A00"
    APP_PAGE_WARNING_LIGHT_COLOR = "#F59E0B"

    APP_PAGE_BG_FALLBACK_IMG = _IMAGES / "bg-fallback.png"

    APP_PAGE_INFO_ICON = _ICONS / "info.svg"
    APP_PAGE_ERROR_ICON = _ICONS / "error.svg"
    APP_PAGE_CLOSE_ICON = _ICONS / "close.svg"
    APP_PAGE_WARNING_ICON = _ICONS / "warning.svg"

    FONT_CINZEL_BOLD = "/fonts/Cinzel-Bold.ttf"
    FONT_CINZEL_BLACK = "/fonts/Cinzel-Black.ttf"
    FONT_CINZEL_MEDIUM = "/fonts/Cinzel-Medium.ttf"
    FONT_CINZEL_REGULAR = "/fonts/Cinzel-Regular.ttf"
    FONT_CINZEL_SEMIBOLD = "/fonts/Cinzel-SemiBold.ttf"
    FONT_CINZEL_EXTRABOLD = "/fonts/Cinzel-ExtraBold.ttf"

    SCHEMA_PATH = _TEMPLATES / "schema.sql"
    STATIC_ITEM_PATH = _TEMPLATES / "static_item.yaml"
    STATIC_SOUL_PATH = _TEMPLATES / "static_soul.yaml"
    STATIC_STAT_PATH = _TEMPLATES / "static_stat.yaml"
    STATIC_SKILL_PATH = _TEMPLATES / "static_skill.yaml"
    STATIC_ORIGIN_PATH = _TEMPLATES / "static_origin.yaml"
    STATIC_CONDITION_PATH = _TEMPLATES / "static_condition.yaml"
    STATIC_KNOWLEDGE_PATH = _TEMPLATES / "static_knowledge.yaml"
    STATIC_WEAPON_TAG_PATH = _TEMPLATES / "static_weapon_tag.yaml"

    _db_url = _env.string("DATABASE_URL")
    if isinstance(_db_url, Err):
        Panic._panic(str(_db_url.error))

    DATABASE_PATH: Path = Path(
        _db_url.unwrap().replace("sqlite:///", "")
    )


settings = Settings()
