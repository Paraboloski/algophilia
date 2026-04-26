from __future__ import annotations

from typing import Optional
from sqlalchemy import JSON  
from app.models.base import Base, PydanticType
from sqlalchemy.orm import Mapped, mapped_column  
from pydantic import BaseModel, ConfigDict, field_validator, model_validator 


class SoulTrait(BaseModel):
    title:       str = ""
    description: str = ""

    model_config = ConfigDict(frozen=True)


class EnhancedEffect(BaseModel):
    title:             str = ""
    affinity_required: int = 0
    description:       str = ""

    model_config = ConfigDict(frozen=True)


class GodAffinity(BaseModel):
    god_key:        str
    affinity_level: int = 0
    


class InventorySlot(BaseModel):
    key:      str
    quantity: int = 1


   
class BodyParts(BaseModel):
    head:      bool = False
    torso:     bool = False
    left_arm:  bool = False
    right_arm: bool = False
    left_leg:  bool = False
    right_leg: bool = False

    model_config = ConfigDict(frozen=True)


class CharacterStats(BaseModel):
    guts:       int = 0
    tenacity:   int = 0
    intensity:  int = 0
    resilience: int = 0

    moving:     int = 0
    current_hp: int = 0
    current_mp: int = 0

    fear_current:   int = 0
    fear_maximum:   int = 4

    hunger_current: int = 0
    hunger_maximum: int = 4
    
    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def current_not_higher_than_max(self) -> "CharacterStats":
        object.__setattr__(self, "current_hp", min(self.current_hp, self.health_points))
        object.__setattr__(self, "current_mp", min(self.current_mp, self.mind_points))
        return self

    @property
    def health_points(self) -> int:
        return (self.guts * 8) + 4

    @property
    def mind_points(self) -> int:
        return (self.tenacity * 8) + 4

    def hp_ratio(self) -> float:
        return self.current_hp / self.health_points if self.health_points else 0.0

    def mp_ratio(self) -> float:
        return self.current_mp / self.mind_points if self.mind_points else 0.0

    @property
    def is_scared(self) -> bool:
        return self.fear_current >= self.fear_maximum

    @property
    def is_starving(self) -> bool:
        return self.hunger_current >= self.hunger_maximum

    @property
    def fear_ratio(self) -> float:
        return self.fear_current / self.fear_maximum if self.fear_maximum else 0.0

    @property
    def hunger_ratio(self) -> float:
        return self.hunger_current / self.hunger_maximum if self.hunger_maximum else 0.0

    @property
    def cargo_slots(self) -> int:
        return (self.guts * 2) + 2

    @property
    def walk_distance(self) -> int:
        return self.resilience + self.moving

    @property
    def run_distance(self) -> int:
        return self.walk_distance * 2


class CharacterKnowledge(BaseModel):
    key:           str
    is_proficient: bool = False
    is_aptitude:   bool = False


class CharacterSpell(BaseModel):
    key:             str
    name:            str
    enhanced_effect: EnhancedEffect

    model_config = ConfigDict(frozen=True)

class CharacterSkills(BaseModel):
    feat_keys:           list[str] = []
    unlocked_spells:     list[CharacterSpell] = []
    god_affinities:      list[GodAffinity] = []
    knowledges:          list[CharacterKnowledge] = []
    

class CharacterInventory(BaseModel):
    weapon_left:  Optional[str] = None
    weapon_right: Optional[str] = None
    armor:        Optional[str] = None
    items:        list[InventorySlot] = []
    accessories:  list[Optional[str]] = [None, None, None]

    @field_validator("accessories")
    @classmethod
    def check_accessory_slots(cls, v: list) -> list:
        if len(v) > 3:
            v = v[:3]
        elif len(v) < 3:
            v = v + [None] * (3 - len(v))
        return v


class CharacterNotes(BaseModel):
    feats:      str = ""
    conditions: str = ""
    body:       str = ""
    equipment:  str = ""
    inventory:  str = ""
    knowledges: str = ""
    spells:     str = ""
    general:    str = ""
    stats:      str = ""


class CharacterInfo(BaseModel):
    name:           str
    origin_key:     str
    soul_key:       str
    backstory:      str = ""
    notes:          CharacterNotes = CharacterNotes()

    knowledges:     list[str] = []
    starting_equip: list[str] = []
    soul_trait:     SoulTrait = SoulTrait()

    model_config = ConfigDict(frozen=True)



class Character(Base):
    __tablename__ = "characters"

    level: Mapped[int] = mapped_column(default=1)
    
    conditions: Mapped[list[str]] = mapped_column("conditions", JSON)
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    info: Mapped[CharacterInfo] = mapped_column("info", PydanticType(CharacterInfo))
    
    body_parts: Mapped[BodyParts] = mapped_column("body_parts", PydanticType(BodyParts))
    
    stats: Mapped[CharacterStats] = mapped_column("stats", PydanticType(CharacterStats))
    
    skills: Mapped[CharacterSkills] = mapped_column("skills", PydanticType(CharacterSkills))
    
    inventory: Mapped[CharacterInventory] = mapped_column("inventory", PydanticType(CharacterInventory))

    @property
    def health_points(self) -> int:
        return self.stats.health_points

    @property
    def mind_points(self) -> int:
        return self.stats.mind_points

    @property
    def cargo_slots(self) -> int:
        return self.stats.cargo_slots

    @property
    def walk_distance(self) -> int:
        return self.stats.walk_distance

    @property
    def run_distance(self) -> int:
        return self.stats.run_distance

    @property
    def proficiency(self) -> int:
        return (self.level + 3) // 4 + 1

    @property
    def aptitude(self) -> int:
        return self.proficiency * 2

    def __repr__(self) -> str:
        return (
            f"<Character("
            f"id={self.id}, "
            f"level={self.level}, "
            f"info={self.info.model_dump()}, "
            f"stats={self.stats.model_dump()}, "
            f"skills={self.skills.model_dump()}, "
            f"inventory={self.inventory.model_dump()}, "
            f"body_parts={self.body_parts.model_dump()}, "
            f"conditions={self.conditions}"
            f")>"
        )
