from flask import g

import db

__all__ = ["create", "get", "get_login", "get_all"]


GET_USERS = """SELECT
  id,
  username,
  display_name
FROM
  users"""

GET_LOGIN_BY_USERNAME = """SELECT
  id,
  username,
  display_name,
  password_hash
FROM
  users
WHERE
  username = LOWER(?)"""

GET_LOGIN_BY_USER_ID = """SELECT
  id,
  username,
  display_name,
  password_hash
FROM
  users
WHERE
  id = LOWER(?)"""

GET_USER_BY_USERNAME = """SELECT
  id,
  username,
  display_name
FROM
  users
WHERE
  username = LOWER(?)"""

GET_USER_BY_USER_ID = """SELECT
  id,
  username,
  display_name
FROM
  users
WHERE
  id = LOWER(?)"""

GET_USER_BY_ROWID = """SELECT
  id,
  username,
  display_name
FROM
  users
WHERE
  ROWID = ?"""

GET_LAST_INSERTED_USER = """SELECT
  id,
  username,
  display_name
FROM
  users
WHERE
  ROWID = last_insert_rowid()"""

GET_USER_PAGE_BY_USER_ID = """SELECT
  u.id,
  u.username,
  u.display_name,
  u.created_at,
  p.id AS post_id,
  p.title,
  p.created_at AS post_created_at,
  p.updated_at AS post_updated_at,
  p.unlisted,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  users AS u
  JOIN posts AS p ON u.id = p.user_id
  LEFT JOIN posts_likes AS pl ON p.id = pl.post_id
WHERE
  p.unlisted = FALSE
  AND u.id = LOWER(?)
GROUP BY
  p.id"""

GET_USER_PAGE_BY_USERNAME = """SELECT
  u.id,
  u.username,
  u.display_name,
  u.created_at,
  p.id AS post_id,
  p.title,
  p.created_at AS post_created_at,
  p.updated_at AS post_updated_at,
  p.unlisted,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  users AS u
  JOIN posts AS p ON u.id = p.user_id
  LEFT JOIN posts_likes AS pl ON p.id = pl.post_id
WHERE
  p.unlisted = FALSE
  AND u.username = LOWER(?)
GROUP BY
  p.id"""

CREATE_USER = """INSERT INTO
  users (username, display_name, password_hash)
VALUES
  (LOWER(?), ?, ?)"""


def get_all():
    return db.query(GET_USERS)


def get(user):
    result = db.query(
        GET_USER_BY_USER_ID if len(user) == 32 else GET_USER_BY_USERNAME,
        [user],
    )

    return result[0] if result and "id" in result[0].keys() else {}


def get_login(user):
    result = db.query(
        GET_LOGIN_BY_USER_ID if len(user) == 32 else GET_LOGIN_BY_USERNAME,
        [user],
    )

    return result[0] if result and "id" in result[0].keys() else {}


def create(name, password_hash):
    username = name.lower()
    display_name = name

    result = db.queries_get_last(
        [
            [CREATE_USER, [username, display_name, password_hash]],
        ],
        GET_LAST_INSERTED_USER,
    )

    # db.execute(CREATE_USER, [username, display_name, password_hash])
    # result = db.query(GET_USER_BY_ROWID, [g.last_insert_id])

    return result[0] if result and "id" in result[0].keys() else {}
