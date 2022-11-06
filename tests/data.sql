

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





DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
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
  FOREIGN KEY (author_id) REFERENCES user (id)
);


