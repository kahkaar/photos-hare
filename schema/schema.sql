BEGIN;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS post_comments;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS posts_tags;

-- N.B. Triggers associated with 'table' are dropped on `DROP TABLE [IF EXISTS] 'table'`.

CREATE TABLE users (
  id BLOB PRIMARY KEY DEFAULT (LOWER(HEX(RANDOMBLOB(16)))),
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  updated_at INTEGER,
  CHECK(LENGTH(username) >= 4)
);

CREATE TABLE posts (
  id BLOB PRIMARY KEY DEFAULT (LOWER(HEX(RANDOMBLOB(16)))),
  title TEXT,
  description TEXT,
  image_path TEXT NOT NULL, -- Store images inside a directory, instead of the database itself.
  unlisted BOOLEAN NOT NULL DEFAULT FALSE,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  updated_at INTEGER,
  user_id BLOB REFERENCES users ON DELETE CASCADE
);

CREATE TABLE post_comments (
  id BLOB PRIMARY KEY DEFAULT (LOWER(HEX(RANDOMBLOB(16)))),
  text TEXT NOT NULL,
  likes INTEGER NOT NULL DEFAULT 0,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  updated_at INTEGER,
  post_id BLOB REFERENCES posts ON DELETE CASCADE,
  user_id BLOB REFERENCES users ON DELETE CASCADE
);

CREATE TABLE tags (
  id BLOB PRIMARY KEY DEFAULT (LOWER(HEX(RANDOMBLOB(16)))),
  name TEXT NOT NULL UNIQUE,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now'))
);

CREATE TABLE posts_tags (
  post_id BLOB REFERENCES posts ON DELETE CASCADE,
  tag_id BLOB REFERENCES tags ON DELETE CASCADE
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

CREATE UNIQUE INDEX idx_username ON users (username);
CREATE UNIQUE INDEX idx_posts_title ON posts (title);
CREATE UNIQUE INDEX idx_posts_unlisted_user_id ON posts (unlisted, user_id);

END;
