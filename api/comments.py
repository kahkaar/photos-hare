import db

__all__ = ["get_of", "get_by"]

GET_COMMENTS_OF_POST_ID = """"""
GET_COMMENTS_BY_USER_ID = """"""


def get_of(post_id):
    return db.query(GET_COMMENTS_OF_POST_ID, [post_id])


def get_by(user_id):
    return db.query(GET_COMMENTS_BY_USER_ID, [user_id])
