import db

from . import helpers

__all__ = [
    "create",
    "delete",
    "find",
    "get",
    "get_all",
    "get_all_of",
    "get_unlisted_of",
    "like",
    # "remove_like",
    "update",
    "update_filename",
]


GET_POSTS = """SELECT
  p.id,
  p.title,
  p.filename,
  p.created_at,
  p.updated_at,
  u.id AS user_id,
  u.display_name
FROM
  posts AS p
  JOIN users AS u ON p.user_id = u.id
WHERE
  unlisted = FALSE
GROUP BY
  p.created_at,
  p.id"""

GET_POSTS_OF_USER_ID = """SELECT
  p.id,
  p.title,
  p.filename,
  p.created_at,
  p.updated_at,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  posts AS p
  LEFT JOIN posts_likes AS pl ON p.id = pl.post_id
WHERE
  p.unlisted = FALSE
  AND p.user_id = LOWER(?)
GROUP BY
  p.created_at,
  p.id"""

GET_POSTS_OF_USERNAME = """SELECT
  p.id,
  p.title,
  p.filename,
  p.created_at,
  p.updated_at,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  posts AS p
  LEFT JOIN users AS u ON u.id = p.user_id
  LEFT JOIN posts_likes AS pl ON p.id = pl.post_id
WHERE
  p.unlisted = FALSE
  AND u.username = LOWER(?)
GROUP BY
  p.created_at,
  p.id"""

GET_POST_BY_ROWID = """SELECT
  p.id,
  p.title,
  p.description,
  p.filename,
  p.created_at,
  p.updated_at,
  p.user_id AS user_id,
  u.display_name,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  posts AS p
  LEFT JOIN users AS u ON u.id = p.user_id
  LEFT JOIN posts_likes AS pl ON pl.post_id = p.id
WHERE
  ROWID = ?"""

GET_LAST_INSERTED_POST = """SELECT
  p.id,
  p.title,
  p.description,
  p.filename,
  p.created_at,
  p.updated_at,
  p.user_id AS user_id,
  u.display_name,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  posts AS p
  LEFT JOIN users AS u ON u.id = p.user_id
  LEFT JOIN posts_likes AS pl ON pl.post_id = p.id
WHERE
  ROWID = last_insert_rowid()"""

GET_LAST_INSERTED_POST_ID = """SELECT
  id
FROM
  posts
WHERE
  ROWID = last_insert_rowid()"""

GET_POST_BY_POST_ID = """SELECT
  p.id,
  p.title,
  p.description,
  p.filename,
  p.unlisted,
  p.created_at,
  p.updated_at,
  p.user_id AS user_id,
  u.display_name,
  t.name AS tag,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  posts AS p
  LEFT JOIN users AS u ON u.id = p.user_id
  LEFT JOIN posts_likes AS pl ON pl.post_id = p.id
  LEFT JOIN posts_tags AS pt ON pt.post_id = p.id
  LEFT JOIN tags AS t ON t.id = pt.tag_id
WHERE
  p.id = ?"""

GET_ALL_POSTS_OF_USER_ID = """SELECT
  p.id,
  p.title,
  p.filename,
  p.created_at,
  p.updated_at,
  p.unlisted,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  posts AS p
  LEFT JOIN posts_likes AS pl ON p.id = pl.post_id
WHERE
  p.user_id = LOWER(?)
GROUP BY
  p.created_at,
  p.id"""

CREATE_POST = """INSERT INTO
  posts (title, description, unlisted, user_id)
VALUES
  (?, ?, ?, LOWER(?))"""

UPDATE = """UPDATE posts
SET
  description = ?,
  unlisted = ?
WHERE
  id = LOWER(?)"""

UPDATE_FILENAME = """UPDATE posts
SET
  filename = ?
WHERE
  id = LOWER(?)"""

UPDATE_DESCRIPTION = """UPDATE posts
SET
  description = ?
WHERE
  id = LOWER(?)"""

UPDATE_UNLISTED = """UPDATE posts
SET
  unlisted = ?
WHERE
  id = LOWER(?)"""

DELETE = """DELETE FROM posts
WHERE
  id = LOWER(?)"""

GET_POSTS_BY_TITLE = """SELECT
  p.id,
  p.title,
  p.filename,
  p.created_at,
  p.updated_at,
  u.id AS user_id,
  u.display_name
FROM
  posts AS p
  JOIN users AS u ON p.user_id = u.id
WHERE
  unlisted = FALSE
  AND p.title LIKE ?
GROUP BY
  p.created_at,
  p.id"""

LIKE = """INSERT INTO
  posts_likes (post_id, user_id, type)
VALUES
  (LOWER(?), LOWER(?), ?)"""

DELETE_LIKE = """DELETE FROM posts_likes
WHERE
  post_id = LOWER(?)
  AND user_id = LOWER(?)"""


def create(user_id, title, description="", unlisted=False):
    result = db.queries_get_last(
        [
            [CREATE_POST, [title, description, unlisted, user_id]],
        ],
        [GET_LAST_INSERTED_POST_ID],
    )

    return helpers.validate_object(result)


def delete(post_id):
    db.execute(DELETE, [post_id])


def find(query):
    result = db.query(GET_POSTS_BY_TITLE, ["%" + query + "%"])
    return helpers.validate_objects(result)


def get(post_id):
    result = db.query(GET_POST_BY_POST_ID, [post_id])
    return helpers.validate_object(result)


def get_all():
    result = db.query(GET_POSTS)
    return helpers.validate_objects(result)


def get_all_of(user):
    result = db.query(
        GET_POSTS_OF_USER_ID if len(user) == 32 else GET_POSTS_OF_USERNAME,
        [user],
    )

    return helpers.validate_objects(result)


def get_unlisted_of(user):
    result = db.query(GET_ALL_POSTS_OF_USER_ID, [user])
    return helpers.validate_objects(result)


def update(post_id, description, unlisted):
    result = db.queries_get_last(
        [
            [UPDATE, [description, unlisted, post_id]],
        ],
        [GET_POST_BY_POST_ID, [post_id]],
    )

    return helpers.validate_object(result)


def like(post_id, user_id, type):
    db.execute(LIKE, [post_id, user_id, type])


# def remove_like(post_id, user_id):
#     db.execute(DELETE_LIKE, [post_id, user_id])


# def update_description(post_id, new_value):
#     result = db.queries_get_last(
#         [
#             [UPDATE_DESCRIPTION, [new_value, post_id]],
#         ],
#         [GET_POST_BY_POST_ID, [post_id]],
#     )

#     return helpers.validate_object(result)


# def update_unlisted(post_id, new_value):
#     result = db.queries_get_last(
#         [
#             [UPDATE_UNLISTED, [new_value, post_id]],
#         ],
#         [GET_POST_BY_POST_ID, [post_id]],
#     )

#     return helpers.validate_object(result)


def update_filename(post_id, new_value):
    db.execute(UPDATE_FILENAME, [new_value, post_id])
