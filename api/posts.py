from flask import session

import db

__all__ = [
    "create",
    "get",
    "get_all",
    "get_all_of",
    "get_unlisted_of",
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
  ) AS post_likes
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
  ) AS post_likes
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
  ) AS post_likes
FROM
  posts AS p
  LEFT JOIN users AS u ON u.id = p.user_id
  LEFT JOIN posts_likes AS pl ON pl.post_id = p.id
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
  p.id"""

CREATE_POST = """INSERT INTO
  posts (title, description, unlisted, user_id)
VALUES
  (?, ?, ?, LOWER(?))"""

UPDATE_FILENAME = """UPDATE
  posts
SET
  filename = ?
WHERE
  id = LOWER(?)"""


def get_all():
    return db.query(GET_POSTS)


def get_unlisted_of(user):
    return db.query(GET_ALL_POSTS_OF_USER_ID, [user])


def get(post_id):
    result = db.query(GET_POST_BY_POST_ID, [post_id])
    return result[0] if result and "id" in result[0].keys() else {}


def get_all_of(user):
    result = db.query(
        GET_POSTS_OF_USER_ID if len(user) == 32 else GET_POSTS_OF_USERNAME,
        [user],
    )

    return result if result and "id" in result[0].keys() else []


def update_filename(post_id, new_value):
    db.execute(UPDATE_FILENAME, [new_value, post_id])


def create(title, description="", unlisted=False):
    user_id = session["user_id"]

    result = db.queries_get_last(
        [
            [CREATE_POST, [title, description, unlisted, user_id]],
        ],
        GET_LAST_INSERTED_POST_ID,
    )

    # db.execute(CREATE_POST, [title, description, unlisted, user_id])
    # result = db.query(GET_POST_BY_ROWID, [g.last_insert_id])

    return result[0] if result and "id" in result[0].keys() else {}
