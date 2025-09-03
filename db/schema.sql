DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS post_comments;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS posts_tags;

-- Triggers associated with 'table' are dropped on DROP TABLE [IF EXISTS] 'table'.

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  updated_at INTEGER
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  image BLOB, -- Add NOT NULL
  unlisted BOOLEAN NOT NULL DEFAULT FALSE,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  updated_at INTEGER,
  user_id INTEGER REFERENCES users
);

CREATE TABLE post_comments (
  id INTEGER PRIMARY KEY,
  text TEXT NOT NULL,
  likes INTEGER NOT NULL DEFAULT 0,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  user_id INTEGER REFERENCES users,
  post_id INTEGER REFERENCES posts
);

CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now'))
);

CREATE TABLE posts_tags (
  post_id INTEGER REFERENCES posts,
  tag_id INTEGER REFERENCES tags
);

CREATE TRIGGER posts_update_timestamp_trigger AFTER UPDATE ON posts
  BEGIN
    UPDATE posts
    SET updated_at = UNIXEPOCH('now')
    WHERE old.id = new.id;
  END;
