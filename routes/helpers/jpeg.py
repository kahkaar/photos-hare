import os

__all__ = [
    "save",
    "validate_signature",
]


def save(data, post_id):
    path = os.path.join("uploads")
    os.makedirs(path, exist_ok=True)

    output_file = os.path.join(path, f"{post_id}.jpg")

    with open(output_file, "wb") as f:
        f.write(data)


def validate_signature(data):
    if not data or len(data) < 4:
        return False

    soi = data[:2]
    eoi = data[-2:]

    return soi == b"\xff\xd8" and eoi == b"\xff\xd9"
