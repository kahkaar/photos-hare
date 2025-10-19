BEGIN;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS posts_likes;
DROP TABLE IF EXISTS posts_comments;
DROP TABLE IF EXISTS posts_comments_likes;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS posts_tags;

-- N.B. Triggers and indices associated with 'table' are dropped on `DROP TABLE [IF EXISTS] 'table'`.

CREATE TABLE users (
  id BLOB PRIMARY KEY DEFAULT (LOWER(HEX(RANDOMBLOB(16)))), -- UUID
  username TEXT NOT NULL UNIQUE, -- Should always be lowercase
  display_name TEXT UNIQUE, -- Allows username capitalization to be changed; LOWER(display_name) = username
  password_hash TEXT NOT NULL,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  updated_at INTEGER -- This and every other `updated_at` column is updated by a trigger; do not update
);

CREATE TABLE posts (
  id BLOB PRIMARY KEY DEFAULT (LOWER(HEX(RANDOMBLOB(16)))),
  title TEXT,
  description TEXT,
  filename TEXT, -- Store images inside a directory, instead of the database-file itself.
  unlisted BOOLEAN NOT NULL DEFAULT FALSE,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  updated_at INTEGER,
  user_id BLOB REFERENCES users ON DELETE CASCADE
);

CREATE TABLE posts_likes (
  post_id BLOB REFERENCES posts ON DELETE CASCADE,
  user_id BLOG REFERENCES users ON DELETE CASCADE,
  type BOOLEAN NOT NULL
);

CREATE TABLE posts_comments (
  id BLOB PRIMARY KEY DEFAULT (LOWER(HEX(RANDOMBLOB(16)))),
  text TEXT NOT NULL,
  created_at INTEGER NOT NULL DEFAULT (UNIXEPOCH('now')),
  updated_at INTEGER,
  post_id BLOB REFERENCES posts ON DELETE CASCADE,
  user_id BLOB REFERENCES users ON DELETE CASCADE
);

CREATE TABLE posts_comments_likes (
  posts_comment_id BLOB REFERENCES posts_comments ON DELETE CASCADE,
  user_id BLOB REFERENCES users ON DELETE CASCADE,
  type BOOLEAN NOT NULL
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

CREATE TRIGGER posts_comments_updated_at_trigger AFTER UPDATE ON posts_comments
  BEGIN
    UPDATE posts_comments
    SET updated_at = UNIXEPOCH('now')
    WHERE id = old.id;
  END;

CREATE UNIQUE INDEX idx_username ON users (username);
CREATE INDEX idx_posts_tags_tag_id ON posts_tags (tag_id);
CREATE INDEX idx_posts_tags_post_id ON posts_tags (post_id);
CREATE INDEX idx_posts_title ON posts (title);
CREATE INDEX idx_posts_user_id ON posts (user_id);
CREATE INDEX idx_posts_likes_post_id ON posts_likes (post_id);
CREATE INDEX idx_posts_comments_likes_posts_comment_id ON posts_comments_likes (posts_comment_id);
CREATE INDEX idx_posts_unlisted_user_id ON posts (unlisted, user_id);
CREATE INDEX idx_posts_comments_post_id ON posts_comments (post_id);

END;
