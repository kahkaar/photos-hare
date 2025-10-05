__all__ = ["get_all"]

import db
from api import helpers

ADD_TAG_TO_POST = """INSERT INTO
  posts_tags (post_id, tag_id)
VALUES
  (LOWER(?), LOWER(?))"""

GET_ALL_TAGS = """SELECT
  id,
  name
FROM
  tags"""

GET_TAGS_OF = """SELECT
  t.name,
  pt.post_id,
  pt.tag_id
FROM
  posts_tags AS pt
  LEFT JOIN tags AS t ON t.id = pt.tag_id
WHERE
  pt.post_id = LOWER(?)"""


def get_all():
    result = db.query(GET_ALL_TAGS)
    return helpers.validate_objects(result)


def get_of(post_id):
    result = db.query(GET_TAGS_OF, [post_id])
    return helpers.validate_objects(result)


def insert(post_id, tag_id):
    db.execute(ADD_TAG_TO_POST, [post_id, tag_id])
