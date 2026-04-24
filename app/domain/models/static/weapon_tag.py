from pydantic import BaseModel, ConfigDict

class WeaponTag(BaseModel):
    key:         str
    name:        str
    description: str
    model_config = ConfigDict(frozen=True)