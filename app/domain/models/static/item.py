from pydantic import BaseModel, ConfigDict

class Item(BaseModel):
    key:         str
    name:        str
    weight:      int
    quantity:    int
    description: str
    model_config = ConfigDict(frozen=True)


class DamagePool(BaseModel):
    dice_count: int
    dice_value: int
    model_config = ConfigDict(frozen=True)

    def __str__(self) -> str:
        return f"{self.dice_count}d{self.dice_value}"


class Weapon(Item):
    weapon_tags:      list[str]
    base_damage:      DamagePool
    two_hand_damage:  DamagePool


class Armor(Item):
    defence:           int
    penalty:           int
    slashing_defence:  bool = False
    blunt_defence:     bool = False
    piercing_defence:  bool = False


class Accessory(Item):
    can_be_removed: bool = True