from enum import Enum as _Enum
from pydantic import BaseModel, ConfigDict


class Month(str, _Enum):
    JANUARY   = "GENNAIO"
    FEBRUARY  = "FEBBRAIO"
    MARCH     = "MARZO"
    APRIL     = "APRILE"
    MAY       = "MAGGIO"
    JUNE      = "GIUGNO"
    JULY      = "LUGLIO"
    AUGUST    = "AGOSTO"
    SEPTEMBER = "SETTEMBRE"
    OCTOBER   = "OTTOBRE"
    NOVEMBER  = "NOVEMBRE"
    DECEMBER  = "DICEMBRE"


class SoulTrait(BaseModel):
    name:        str
    description: str
    model_config = ConfigDict(frozen=True)

class Soul(BaseModel):
    key:        str
    name:       str
    description: str
    month:      Month
    soul_trait: SoulTrait
    model_config = ConfigDict(frozen=True)