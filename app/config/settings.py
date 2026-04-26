from pathlib import Path
from app.utils import Env

_YAML_FILES = [
    Path("app/assets/templates/feats.yaml"),
    Path("app/assets/templates/items.yaml"),
    Path("app/assets/templates/souls.yaml"),
    Path("app/assets/templates/armors.yaml"),
    Path("app/assets/templates/spells.yaml"),
    Path("app/assets/templates/origins.yaml"),
    Path("app/assets/templates/weapons.yaml"),
    Path("app/assets/templates/conditions.yaml"),
    Path("app/assets/templates/knowledges.yaml"),
    Path("app/assets/templates/accessories.yaml"),
    Path("app/assets/templates/weapon_tags.yaml"),
]


class Settings:
    def __init__(self):
        _env = Env()
        self._yaml_files = _YAML_FILES
        self._log_dir = "app/assets/logs"
        self._database_url = _env.require("DATABASE_URL")
        self._sql_schema = "app/assets/templates/schema.sql"
        self._telegram_token = _env.get_env("TELEGRAM_TOKEN")
        self._telegram_chat_id = _env.get_env("TELEGRAM_CHAT_ID")


settings = Settings()
