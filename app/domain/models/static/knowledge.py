from pydantic import BaseModel, ConfigDict
from app.domain.models.static.stat import Attribute

class Knowledge(BaseModel):
    key:         str
    name:        str
    description: str = ""
    attribute:   Attribute
    model_config = ConfigDict(frozen=True)