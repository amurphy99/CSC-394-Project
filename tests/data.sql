

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

*/





DROP TABLE IF EXISTS genre_counts           ;
DROP TABLE IF EXISTS genres                 ;

DROP TABLE IF EXISTS movies_list_statistics ;
DROP TABLE IF EXISTS movies_list_info       ;
DROP TABLE IF EXISTS movies_list            ;
DROP TABLE IF EXISTS movies                 ;

DROP TABLE IF EXISTS friend_requests        ;
DROP TABLE IF EXISTS friends                ;

DROP TABLE IF EXISTS all_users              ;


/* all_users:
--------------
    * add rule to delete lists on user deletion
        - maybe transfer ownership to the oldest editorID if any
*/
CREATE TABLE all_users (
  id            SERIAL 	  PRIMARY KEY,
  username      TEXT      UNIQUE NOT NULL,
  password      TEXT      NOT NULL,
  privileges    INTEGER   DEFAULT             0,
  date_joined   TIMESTAMP DEFAULT             CURRENT_TIMESTAMP,
  style_mode    INTEGER   DEFAULT             0
);



/* movies:
----------- */
CREATE TABLE movies (
    id 		    INTEGER PRIMARY KEY,
    title 	    TEXT,
    poster      TEXT,
    popularity  INTEGER DEFAULT 1
);



/* movies_list_info:
---------------------
    UPDATED BY TRIGGERS:
      * list length
      * watch counts (plan to watch, finished)
      * average rating

*/
CREATE TABLE movies_list_info (
  id                SERIAL        PRIMARY KEY,
  owner_id          INTEGER,
  editor_ids        TEXT,
  list_name         TEXT,
  list_description  TEXT,
  recently_added    INTEGER,
  /* statistics: (leaving out "currently watching" for now as it can be calculated from the total)
  --------------- */
  date_created      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
  last_updated      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
  average_rating    NUMERIC(10,2) DEFAULT 0.00,
  total_movies      INTEGER       DEFAULT 0,
  plan_to_watch     INTEGER       DEFAULT 0,
  finished          INTEGER       DEFAULT 0,
  UNIQUE(owner_id, list_name)
);



/* statistics table:
-----------------------------------  
    UPDATED BY PYTHON:
        * all

*/
CREATE TABLE movies_list_statistics (
  list_id         INTEGER       REFERENCES  movies_list_info(id),
  total_movies    INTEGER       DEFAULT     0,
  total_runtime   INTEGER       DEFAULT     0,
  total_budget    INTEGER       DEFAULT     0,
  CONSTRAINT pk_movies_list_statistics PRIMARY KEY (list_id)
);



/* movies_list:
---------------- */
CREATE TABLE movies_list (
  movie_id 	    INTEGER   REFERENCES  movies(id),
  list_id 	    INTEGER   REFERENCES  movies_list_info(id),
  status 	    INTEGER   DEFAULT     0,
  rating        INTEGER   DEFAULT     -1,
  date_added    TIMESTAMP DEFAULT     CURRENT_TIMESTAMP,
  UNIQUE(movie_id, list_id),
  CONSTRAINT pk_movies_list PRIMARY KEY (movie_id, list_id)
);



/* genres: (automatically updated)
----------------------------------- */
CREATE TABLE genres (
  genre_id    INT   PRIMARY KEY,
  genre_name  TEXT  NOT NULL,
  popularity  INT   DEFAULT       0
);
/* genre counts: (automatically updated)
----------------------------------------- */
CREATE TABLE genre_counts (
  list_id   INT REFERENCES  movies_list_info(id),
  genre_id  INT REFERENCES  genres(genre_id),
  count     INT DEFAULT     1,
  UNIQUE(list_id, genre_id),
  CONSTRAINT pk_genre_counts PRIMARY KEY (list_id, genre_id)
);




/* friend requests table:
-----------------------------------  */
CREATE TABLE friend_requests (
  sender_id     INTEGER   REFERENCES  all_users(id),
  receiver_id   INTEGER   REFERENCES  all_users(id),
  date_created  TIMESTAMP DEFAULT     CURRENT_TIMESTAMP,
  CHECK (sender_id <> receiver_id),
  CONSTRAINT pk_friend_requests PRIMARY KEY (sender_id, receiver_id)
);
/* friends table:
-----------------------------------  */
CREATE TABLE friends (
  friend_1_id   INTEGER   REFERENCES  all_users(id),
  friend_2_id   INTEGER   REFERENCES  all_users(id),
  date_created  TIMESTAMP DEFAULT     CURRENT_TIMESTAMP,
  CHECK (friend_1_id <> friend_2_id),
  CONSTRAINT pk_friends PRIMARY KEY (friend_1_id, friend_2_id)
);













INSERT INTO all_users (id, username, password)
VALUES
  (1, 'test', 'test'),
  (2, 'test1', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  (3, 'other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');
--INSERT INTO all_users (id, username, password, privileges) VALUES (4, 'test2', 'pass2', 1)


INSERT INTO movies_list_info (id, owner_id, list_name, list_description)
VALUES
    (1, 1, 'general', 'test general list'),
    (2, 2, 'general', 'test general list'),
    (3, 3, 'general', 'test general list');


INSERT INTO movies_list_statistics (list_id)
VALUES
    (1),
    (2),
    (3);



/* MOVIES
------------------------ 
INSERT INTO movies (id, title, poster) 
VALUES (11836, 'The SpongeBob SquarePants Movie', '/gjZD811kfY1ideNuBukcuCy8ocA.jpg') 
ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;

INSERT INTO movies (id, title, poster)
VALUES (400160, 'The SpongeBob Movie: Sponge on the Run', '/jlJ8nDhMhCYJuzOw3f52CP1W8MW.jpg') 
ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;

INSERT INTO movies (id, title, poster) 
VALUES (228165, 'The SpongeBob Movie: Sponge Out of Water', '/2WDmjUlSAPlA27i2OwEC7sRTFw3.jpg') 
ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;
*/

/* GENRES
------------- */
INSERT INTO genres (genre_id, genre_name)
VALUES
    (28, 'Action'), 
    (12, 'Adventure'), 
    (16, 'Animation'), 
    (35, 'Comedy'), 
    (80, 'Crime'), 
    (99, 'Documentary'), 
    (18, 'Drama'), 
    (10751, 'Family'), 
    (14, 'Fantasy'), 
    (36, 'History'), 
    (27, 'Horror'), 
    (10402, 'Music'), 
    (9648, 'Mystery'), 
    (10749, 'Romance'), 
    (878, 'Science Fiction'), 
    (10770, 'TV Movie'), 
    (53, 'Thriller'), 
    (10752, 'War'), 
    (37, 'Western');