from sqlalchemy import JSON 
from sqlalchemy.types import TypeDecorator  
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class PydanticType(TypeDecorator):
    impl = JSON

    def __init__(self, pydantic_class):
        super().__init__()
        self.pydantic_class = pydantic_class

    def process_bind_param(self, value, dialect):
        return value.model_dump(mode="json") if value else None

    def process_result_value(self, value, dialect):
        return self.pydantic_class.model_validate(value) if value else None
