from pydantic import BaseModel, ConfigDict


class Skill(BaseModel):
    key:         str
    name:        str
    description: str
    model_config = ConfigDict(frozen=True)


class Feat(Skill):
    pass


class EnhancedEffect(BaseModel):
    effect:                  str
    affinity_level_required: int  
    model_config = ConfigDict(frozen=True)


class Spell(Skill):
    required_affinity_level: int        
    affinity_with_god:       str          
    enhanced_effect:         EnhancedEffect 