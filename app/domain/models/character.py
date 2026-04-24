from __future__ import annotations

from sqlalchemy import JSON
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.models.base import Base, PydanticType
from app.domain.models.static import GritStats, VitalStats
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

class BodyParts(BaseModel):
    head:      bool = False
    torso:     bool = False
    left_arm:  bool = False
    right_arm: bool = False
    left_leg:  bool = False
    right_leg: bool = False
    model_config = ConfigDict(frozen=True)

class CharacterStats(BaseModel):
    moving:        int = 0
    current_hp:    int = 0
    current_mp:    int = 0
    stats:         GritStats
    model_config = ConfigDict(frozen=True)

    fear_progress:   VitalStats = VitalStats()
    hunger_progress: VitalStats = VitalStats()
    
    @model_validator(mode="after")
    def current_not_higher_than_max(self) -> "CharacterStats":
        if self.current_hp > self.health_points:
            self.current_hp = self.health_points
        if self.current_mp > self.mind_points:
            self.current_mp = self.mind_points 
        return self

    @property
    def health_points(self) -> int:
        return (self.stats.guts * 8) + 4

    @property
    def mind_points(self) -> int:
        return (self.stats.tenacity * 8) + 4
    
    def hp_ratio(self) -> float:
        return self.current_hp / self.health_points if self.health_points else 0.0

    def mp_ratio(self) -> float:
        return self.current_mp / self.mind_points if self.mind_points else 0.0

    @property
    def cargo_slots(self) -> int:
        return (self.stats.guts * 2) + 2

    @property
    def walk_distance(self) -> int:
        return self.stats.resilience + self.moving

    @property
    def run_distance(self) -> int:
        return self.walk_distance * 2

    @property
    def is_scared(self) -> bool:
        return self.fear_progress.is_full()

    @property
    def is_starving(self) -> bool:
        return self.hunger_progress.is_full()

class CharacterKnowledge(BaseModel):
    key:           str
    is_proficient: bool = False
    is_aptitude:   bool = False

    @field_validator("is_proficient", "is_aptitude", mode="before")
    @classmethod
    def at_least_is_proficient(cls, v: bool) -> bool:
        return v

class GodAffinity(BaseModel):
    god_key:        str
    affinity_level: int = 0

    @property
    def spell_cost_formula(self) -> int:
        return 4 * (2 ** (self.affinity_level - 1)) if self.affinity_level > 0 else 0

class CharacterSkills(BaseModel):
    feat_keys:            list[str] = []
    unlocked_spell_keys:  list[str] = []
    god_affinities:       list[GodAffinity] = []
    knowledges:           list[CharacterKnowledge] = []

class InventorySlot(BaseModel):
    key:      str
    quantity: int = 1

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
    name:        str
    origin_key:  str
    backstory:   str = ""
    notes:      CharacterNotes = CharacterNotes()
    soul_key:    str
    model_config = ConfigDict(frozen=True)

class Character(Base):
    __tablename__ = "characters"

    level: Mapped[int] = mapped_column(default=1)
    
    conditions: Mapped[list[str]] = mapped_column("conditions", JSON)
    
    id:    Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    body_parts: Mapped[BodyParts] = mapped_column("body_parts", PydanticType(BodyParts))
    
    info:       Mapped[CharacterInfo] = mapped_column("info", PydanticType(CharacterInfo))
    
    stats:      Mapped[CharacterStats] = mapped_column("stats", PydanticType(CharacterStats))
    
    skills:     Mapped[CharacterSkills] = mapped_column("skills", PydanticType(CharacterSkills))
    
    inventory:  Mapped[CharacterInventory] = mapped_column("inventory", PydanticType(CharacterInventory))

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
        return min(2 + (self.level - 1) // 4, 6)

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