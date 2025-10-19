import random
import time

from werkzeug.security import generate_password_hash

import db

# This will take longer to generate users if set to 'True', since generating real password hashes
# Set to 'False' if you do not need to log in as dummy user.
GENERATE_USERS_WITH_PASSWORDS = False

USER_COUNT = 10**4  # Amount of users to be generated
POST_COUNT = 10**5  # Amount of posts to be generated
COMMENT_COUNT = 10**5  # Amount of comments to be generated
POST_LIKES_COUNT = 10**6  # Amount of post likes to be generated
COMMENT_LIKES_COUNT = 10**6  # Amount of comment likes to be generated

# In how large of a batch will the items be inserted into the database
USERS_BATCH_SIZE = 5000
POSTS_BATCH_SIZE = 5000
COMMENT_BATCH_SIZE = 5000
POST_LIKES_BATCH_SIZE = 5000
COMMENT_LIKES_BATCH_SIZE = 5000


def log(message):
    print(message)


def generate_users(count):
    log(f"Generating {count} users...")
    start_time = time.time()
    data = [
        (
            f"admin-{i}",
            f"Admin-{i}",
            generate_password_hash(f"admin-{i}")
            if GENERATE_USERS_WITH_PASSWORDS
            else "password_hash",
        )
        for i in range(count)
    ]
    end_time = time.time()
    log(f"Generated {len(data)} users in {round(end_time - start_time, 2)} s")
    return data


def insert_users(cur, users, batch_size):
    n = len(users)
    log(f"Inserting {n} users in batches of {batch_size}...")
    start_time = time.time()
    for i in range(0, n, batch_size):
        cur.executemany(
            """INSERT INTO users (username, display_name, password_hash) VALUES (LOWER(?), ?, ?)""",
            users[i : i + batch_size],
        )
    end_time = time.time()
    log(f"Inserted {n} users in {round(end_time - start_time, 2)} s")


def get_user_ids(cur, users):
    log(f"Fetching {len(users)} user_ids and shuffling...")
    start_time = time.time()
    ids = [u["id"] for u in cur.execute("SELECT id FROM users").fetchall()]
    random.shuffle(ids)
    end_time = time.time()
    log(
        f"Retrieved {len(ids)} shuffled user_ids in {round(end_time - start_time, 2)} s"
    )
    return ids


def generate_posts(count, user_ids):
    log(f"Generating {count} posts...")

    user_ids_length = len(user_ids)

    start_time = time.time()
    data = [
        (
            f"title-{i}",
            f"description-{i}",
            "_dummy.jpg",
            random.randint(0, 1),
            user_ids[random.randint(0, user_ids_length - 1)],
        )
        for i in range(count)
    ]
    end_time = time.time()
    log(f"Generated {len(data)} posts in {round(end_time - start_time, 2)} s")
    return data


def insert_posts(cur, posts, batch_size):
    n = len(posts)
    start_time = time.time()
    log(f"Inserting {n} posts in batches of {batch_size}...")
    for i in range(0, n, batch_size):
        cur.executemany(
            """INSERT INTO posts (title, description, filename, unlisted, user_id)
            VALUES (?, ?, ?, ?, LOWER(?))""",
            posts[i : i + batch_size],
        )
    end_time = time.time()
    log(f"Inserted {n} posts in {round(end_time - start_time, 2)} s")


def get_post_ids(cur, posts):
    log(f"Fetching {len(posts)} post_ids and shuffling...")
    start_time = time.time()
    ids = [p["id"] for p in cur.execute("SELECT id FROM posts").fetchall()]
    random.shuffle(ids)
    end_time = time.time()
    log(
        f"Retrieved {len(ids)} shuffled post_ids in {round(end_time - start_time, 2)} s"
    )
    return ids


def generate_comments(count, post_ids, user_ids):
    log(f"Generating {count} comments...")

    post_ids_length = len(post_ids)
    user_ids_length = len(user_ids)

    start_time = time.time()
    data = [
        (
            f"text-{i}",
            post_ids[random.randint(0, post_ids_length - 1)],
            user_ids[random.randint(0, user_ids_length - 1)],
        )
        for i in range(count)
    ]
    end_time = time.time()
    log(
        f"Generated {len(data)} comments in {round(end_time - start_time, 2)} s"
    )
    return data


def insert_comments(cur, comments, batch_size):
    n = len(comments)
    log(f"Inserting {n} comments in batches of {batch_size}...")
    start_time = time.time()
    for i in range(0, n, batch_size):
        cur.executemany(
            """INSERT INTO posts_comments (text, post_id, user_id) VALUES (?, LOWER(?), LOWER(?))""",
            comments[i : i + batch_size],
        )
    end_time = time.time()
    log(f"Inserted {n} comments in {round(end_time - start_time, 2)} s")


def get_comment_ids(cur, comments):
    log(f"Fetching {len(comments)} comment_ids and shuffling...")
    start_time = time.time()
    ids = [
        pc["id"]
        for pc in cur.execute("SELECT id FROM posts_comments").fetchall()
    ]
    random.shuffle(ids)
    end_time = time.time()
    log(
        f"Retrieved {len(ids)} shuffled comment_ids in {round(end_time - start_time, 2)} s"
    )
    return ids


def generate_likes(count, to_ids, user_ids):
    log(f"Generating {count} post likes...")

    user_ids_length = len(user_ids)
    to_ids_length = len(to_ids)

    start_time = time.time()
    data = [
        (
            to_ids[random.randint(0, to_ids_length - 1)],
            user_ids[random.randint(0, user_ids_length - 1)],
            random.randint(0, 1),
        )
        for i in range(count)
    ]
    end_time = time.time()
    log(f"Generated {len(data)} likes in {round(end_time - start_time, 2)} s")
    return data


def insert_post_likes(cur, likes, batch_size):
    n = len(likes)
    log(f"Inserting {n} post likes in batches of {batch_size}...")
    start_time = time.time()
    for i in range(0, n, batch_size):
        cur.executemany(
            """INSERT INTO posts_likes (post_id, user_id, type) VALUES (LOWER(?), LOWER(?), ?)""",
            likes[i : i + batch_size],
        )
    end_time = time.time()
    log(f"Inserted {n} post likes in {round(end_time - start_time, 2)} s")


def insert_comment_likes(cur, likes, batch_size):
    n = len(likes)
    log(f"Inserting {n} comment likes in batches of {batch_size}...")
    start_time = time.time()
    for i in range(0, n, batch_size):
        cur.executemany(
            """INSERT INTO posts_comments_likes (posts_comment_id, user_id, type) VALUES (LOWER(?), LOWER(?), ?)""",
            likes[i : i + batch_size],
        )
    end_time = time.time()
    log(f"Inserted {n} comment likes in {round(end_time - start_time, 2)} s")


users = generate_users(USER_COUNT)

con = db.get_connection()
cur = con.cursor()

insert_users(cur, users, USERS_BATCH_SIZE)
user_ids = get_user_ids(cur, users)

posts = generate_posts(POST_COUNT, user_ids)
insert_posts(cur, posts, POSTS_BATCH_SIZE)
post_ids = get_post_ids(cur, posts)

posts_likes = generate_likes(POST_LIKES_COUNT, post_ids, user_ids)
insert_post_likes(cur, posts_likes, POST_LIKES_BATCH_SIZE)

comments = generate_comments(COMMENT_COUNT, post_ids, user_ids)
insert_comments(cur, comments, COMMENT_BATCH_SIZE)
comment_ids = get_comment_ids(cur, comments)

posts_comments_likes = generate_likes(
    COMMENT_LIKES_COUNT, comment_ids, user_ids
)
insert_comment_likes(cur, posts_comments_likes, COMMENT_LIKES_BATCH_SIZE)

log("Committing and closing the database connection...")
start_time = time.time()
con.commit()
con.close()
end_time = time.time()
log(
    f"Time spent committing and closing the database connection: {round(end_time - start_time, 2)} s"
)
