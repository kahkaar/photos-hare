import random
import time

from werkzeug.security import generate_password_hash

import db

# This will take longer to generate users if set to 'True', since generating real password hashes
# Set to 'False' if you do not need to log in as dummy user.
GENERATE_USERS_WITH_PASSWORDS = False

USER_COUNT = 10**4  # Amount of users to be generated
POST_COUNT = 10**6  # Amount of posts to be generated

# In how large of a batch will the items be inserted into the database
USERS_BATCH_SIZE = 5000
POSTS_BATCH_SIZE = 5000


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


users = generate_users(USER_COUNT)

con = db.get_connection()
cur = con.cursor()

insert_users(cur, users, USERS_BATCH_SIZE)
user_ids = get_user_ids(cur, users)

posts = generate_posts(POST_COUNT, user_ids)
insert_posts(cur, posts, POSTS_BATCH_SIZE)


log("Committing and closing the database connection...")
start_time = time.time()
con.commit()
con.close()
end_time = time.time()
log(
    f"Time spent committing and closing the database connection: {round(end_time - start_time, 2)} s"
)
