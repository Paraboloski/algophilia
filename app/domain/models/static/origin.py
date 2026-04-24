from pydantic import BaseModel, ConfigDict

class Origin(BaseModel):
    key:         str
    name:        str
    description: str
    model_config = ConfigDict(frozen=True)