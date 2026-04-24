from enum import Enum as _Enum
from pydantic import BaseModel, ConfigDict


class Attribute(str, _Enum):
    GUTS       = "GRINTA"
    TENACITY   = "TENACIA"
    INTENSITY  = "INTENSITÀ"
    RESILIENCE = "RESILIENZA"


class GritStats(BaseModel):
    model_config = ConfigDict(frozen=True)
    guts:       int = 0
    tenacity:   int = 0
    intensity:  int = 0
    resilience: int = 0


class VitalStats(BaseModel):
    model_config = ConfigDict(frozen=True)
    current: int = 0
    maximum: int = 4

    def increase(self, amount: int = 1) -> "VitalStats":
        return VitalStats(
            current=min(self.current + amount, self.maximum),
            maximum=self.maximum,
        )

    def decrease(self, amount: int = 1) -> "VitalStats":
        return VitalStats(
            current=max(self.current - amount, 0),
            maximum=self.maximum,
        )

    def is_full(self) -> bool:
        return self.current >= self.maximum

    def ratio(self) -> float:
        return self.current / self.maximum