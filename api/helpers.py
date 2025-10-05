__all__ = [
    "validate_object",
    "validate_objects",
]


def validate_object(obj):
    return obj[0] if obj and "id" in obj[0].keys() and obj[0]["id"] else {}


def validate_objects(objs):
    return objs if objs and "id" in objs[0].keys() else []
