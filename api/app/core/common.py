from enum import Enum

from bson.objectid import ObjectId, InvalidId


class Environment(str, Enum):
    development = "development"
    production = "production"

    def is_production(self):
        return self == Environment.production


class ObjectIdStr(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")
        return str(v)
