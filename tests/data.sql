

/* TESTING DATA 
------------------------ 
new branch test
*/

/*
INSERT INTO test_user (username, password, privileges)  VALUES ('admin',    'password', 1);
INSERT INTO test_user (username, password) VALUES ('testing user', 'password');
INSERT INTO test_user (username, password) VALUES ('other'       , 'password123');
*/

/* NEW MOVIE LIST DATA 
------------------------ */
/*
INSERT INTO movies_list_info (owner_id, list_name, list_description) VALUES (1, 'test list', 'testing movie list');

INSERT INTO movies (id, title, poster) VALUES (100, 'testing100', 'none') ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;
INSERT INTO movies (id, title, poster) VALUES (200, 'testing200', 'none') ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;

INSERT INTO movies_list (movie_id, list_id, status, rating) VALUES (100, 1, 1, 5);
INSERT INTO movies_list (movie_id, list_id, status, rating) VALUES (200, 1, 0, 2);
*/





DROP TABLE IF EXISTS all_users;
DROP TABLE IF EXISTS post;

CREATE TABLE all_users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES all_users (id)
);




INSERT INTO all_users (username, password)
VALUES
  ('test', 'test'),
  ('test1', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
