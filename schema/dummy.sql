BEGIN;
-- Partly generated using SQL Test Data Generator Tool from https://www.coderstool.com/sql-test-data-generator
INSERT INTO users (username, display_name, password_hash) VALUES ('root', 'root', 'root');
INSERT INTO users (username, display_name, password_hash) VALUES ('root1', 'root1', 'root1');
INSERT INTO users (username, display_name, password_hash) VALUES ('root2', 'root2', 'root2');
INSERT INTO users (username, display_name, password_hash) VALUES ('root3', 'root3', 'root3');
INSERT INTO users (username, display_name, password_hash) VALUES ('root4', 'root4', 'root4');

INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('newton', 'think festival designers antique invitations', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('cfr', 'executive everyone sending client william', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('mild', 'exceptions attitude ld brunette campbell', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('test', 'invention desk bailey adelaide bios', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('treasure', 'tim safari useful whereas missions', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root'));

INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('genesis', 'inspection rap viewed lead rid', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('war', 'hull oval faced rough cope', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('donna', 'hindu boutique homework abc thrown', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('monitoring', 'clearing scoring harassment mauritius video', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('cisco', 'counseling temperatures beings madonna compile', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root'));

INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('theatre', 'urw aimed dave hand jun', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root1'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('advances', 'ocean acrylic brothers lighter beatles', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root1'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('spell', 'efficiently excel shipped bulgarian exceptional', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root1'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('determine', 'infrared contacting cornwall lawyer although', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root1'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('authorities', 'intention attached certificate chose government', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root1'));

INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('successfully', 'mn music publication pos reform', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root1'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('anthony', 'accomplish fold seating ne journalist', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root1'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('names', 'nursing adaptor buy stanley profession', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root1'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('surely', 'mails cheaper sustainable encouraged solar', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root1'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('kb', 'accuracy distributors sapphire allan various', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root1'));

INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('thickness', 'powers heading forward leather modems', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root2'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('northwest', 'stevens molecular voice asks newspapers', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root2'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('senator', 'achievement lucy pleased scenic diesel', '_dummy.jpg', FALSE, (SELECT id FROM users WHERE username = 'root2'));

INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('they', 'typing thin worried profit current', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root2'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('snow', 'smaller strings helping italiano plymouth', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root2'));
INSERT INTO posts (title, description, filename, unlisted, user_id)
VALUES ('mill', 'hurt stereo somehow graham forests', '_dummy.jpg', TRUE, (SELECT id FROM users WHERE username = 'root2'));

INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 1) ,(SELECT id FROM users WHERE username = 'root1'), TRUE);
INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 1) ,(SELECT id FROM users WHERE username = 'root3'), TRUE);
INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 2) ,(SELECT id FROM users WHERE username = 'root2'), FALSE);
INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 3) ,(SELECT id FROM users WHERE username = 'root1'), TRUE);
INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 3) ,(SELECT id FROM users WHERE username = 'root2'), TRUE);
INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 3) ,(SELECT id FROM users WHERE username = 'root3'), FALSE);
INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 4) ,(SELECT id FROM users WHERE username = 'root1'), TRUE);
INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 4) ,(SELECT id FROM users WHERE username = 'root2'), TRUE);
INSERT INTO posts_likes (post_id, user_id, type)
VALUES ((SELECT id FROM posts WHERE rowid = 5) ,(SELECT id FROM users WHERE username = 'root1'), TRUE);


-- Same as init.sql; not generated.
INSERT INTO tags (name) VALUES ('cats');
INSERT INTO tags (name) VALUES ('cs');
INSERT INTO tags (name) VALUES ('dogs');
INSERT INTO tags (name) VALUES ('finland');
INSERT INTO tags (name) VALUES ('pets');
INSERT INTO tags (name) VALUES ('rabbits');
END;
