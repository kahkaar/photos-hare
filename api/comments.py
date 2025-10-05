import db
from api import helpers

__all__ = [
    "get_by",
    "get_of",
]

CREATE = """INSERT INTO
  posts_comments (text, post_id, user_id)
VALUES
  (?, LOWER(?), LOWER(?))"""

GET_LAST_INSERTED_COMMENT = """SELECT
  id,
  text,
  created_at,
  updated_at,
  post_id,
  user_id
FROM
  posts_comments
WHERE
  ROWID = last_insert_rowid()"""

GET_LAST_INSERTED_COMMENT_ID = """SELECT
  id
FROM
  posts_comments
WHERE
  ROWID = last_insert_rowid()"""

GET_COMMENTS_OF_POST_ID = """SELECT
  pc.id,
  pc.text,
  pc.created_at,
  pc.updated_at,
  pc.post_id,
  pc.user_id,
  u.display_name,
  SUM(
    CASE
      WHEN pcl.type = TRUE THEN 1
      WHEN pcl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM
  posts_comments AS pc
  LEFT JOIN users AS u ON u.id = pc.user_id
  LEFT JOIN posts_comments_likes AS pcl ON pcl.posts_comment_id = pc.post_id
WHERE
  pc.post_id = LOWER(?)
GROUP BY
  pc.id
ORDER BY
  pc.created_at DESC,
  pc.id"""

GET_COMMENTS_BY_USER_ID = """"""


def create(text, post_id, user_id):
    result = db.queries_get_last(
        [[CREATE, [text, post_id, user_id]]], [GET_LAST_INSERTED_COMMENT_ID]
    )

    return helpers.validate_object(result)


def get_by(user_id):
    return db.query(GET_COMMENTS_BY_USER_ID, [user_id])


def get_of(post_id):
    result = db.query(GET_COMMENTS_OF_POST_ID, [post_id])
    return helpers.validate_objects(result)
