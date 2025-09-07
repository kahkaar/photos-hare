get_posts = """SELECT * FROM posts WHERE unlisted = FALSE"""
get_users = """SELECT id, username FROM users"""
get_password_hash = """SELECT password_hash FROM users WHERE username = ?"""
get_user_id = """SELECT id FROM users WHERE username = ?"""
get_user = """SELECT id, password_hash FROM users WHERE username = ?"""

create_user = """INSERT INTO users (username, password_hash) VALUES (?, ?)"""
