get_posts = """SELECT * FROM posts WHERE unlisted = FALSE"""
get_users = """SELECT id, username, display_name FROM users"""

get_user = """SELECT id, username, display_name, password_hash FROM users WHERE username = LOWER(?)"""
get_user_id = """SELECT id FROM users WHERE username = LOWER(?)"""

create_user = """INSERT INTO users (username, display_name, password_hash) VALUES (LOWER(?), ?, ?)"""
