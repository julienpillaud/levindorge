from bson import ObjectId
from bson.errors import InvalidId


def is_str_object_id(value: str) -> bool:
    try:
        ObjectId(value)
        return True
    except InvalidId:
        return False
