from datetime import datetime

from . import alert, csrf, image, session

__all__ = ["alert", "csrf", "session", "image", "to_localtime"]


def to_localtime(obj):
    if not obj:
        return

    def from_timestamp(ts):
        if not ts:
            return

        return str(datetime.fromtimestamp(ts).astimezone()).split("+")[0]

    return {
        **obj,
        "created_at": from_timestamp(obj["created_at"]),
        "updated_at": from_timestamp(obj["updated_at"]),
    }
