import os

__all__ = [
    "save",
    "validate_signature",
]


# def remove_exif(data):
#     start = data.find(b"\xff\xe1")
#     if start == -1:
#         return data

#     length = int.from_bytes(data[start + 2 : start + 4])

#     end = start + 2 + 2 + length

#     return data[:start] + data[end:]


def save(data, post_id):
    # clean_data = remove_exif(data)
    clean_data = data

    path = os.path.join("uploads")
    os.makedirs(path, exist_ok=True)

    output_file = os.path.join(path, f"{post_id}.jpg")

    with open(output_file, "wb") as f:
        f.write(clean_data)


def validate_signature(data):
    soi = data[:2]
    eoi = data[-2:]

    return soi == b"\xff\xd8" and eoi == b"\xff\xd9"
