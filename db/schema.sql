BEGIN;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS post_comments;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS posts_tags;

-- N.B. Triggers associated with 'table' are dropped on `DROP TABLE [IF EXISTS] 'table'`.

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
  image_path TEXT NOT NULL, -- Store images inside a directory, instead of the database itself.
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
  updated_at INTEGER,
  post_id INTEGER REFERENCES posts,
  user_id INTEGER REFERENCES users
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

CREATE TRIGGER users_updated_at_trigger AFTER UPDATE ON users
  BEGIN
    UPDATE users
    SET updated_at = UNIXEPOCH('now')
    WHERE id = old.id;
  END;

CREATE TRIGGER posts_updated_at_trigger AFTER UPDATE ON posts
  BEGIN
    UPDATE posts
    SET updated_at = UNIXEPOCH('now')
    WHERE id = old.id;
  END;

CREATE TRIGGER post_comments_updated_at_trigger AFTER UPDATE ON post_comments
  BEGIN
    UPDATE post_comments
    SET updated_at = UNIXEPOCH('now')
    WHERE id = old.id;
  END;
END;
