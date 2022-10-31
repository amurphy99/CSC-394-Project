DROP TABLE IF EXISTS testing_movies_list;
DROP TABLE IF EXISTS testing_movies_list_info;
DROP TABLE IF EXISTS testing_movies     CASCADE;
DROP TABLE IF EXISTS testing_test_user  CASCADE;



CREATE TABLE testing_test_user (
  id            serial 	  PRIMARY KEY,
  username      TEXT      UNIQUE NOT NULL,
  password      TEXT      NOT NULL,
  privileges    int       DEFAULT             0,
  date_joined   timestamp DEFAULT             CURRENT_TIMESTAMP,
  style_mode    int       DEFAULT             0
);


CREATE TABLE testing_movies (
    id 		      int     PRIMARY KEY,
    title 	    TEXT,
    poster      TEXT,
    popularity  int     DEFAULT 1
);


CREATE TABLE testing_movies_list_info (
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
  finished          INTEGER       DEFAULT 0
)

CREATE TABLE testing_movies_list (
  movie_id 	int references testing_movies(id),
  list_id 	int references testing_movies_list_info(id),
  status 	  int DEFAULT    0,
  rating 	  int DEFAULT    -1,
  constraint pk_testing_movies_list primary key (movie_id, list_id)
);




/* TESTING DATA 
------------------------ */
INSERT INTO testing_test_user (username, password, privileges)  VALUES ('admin',    'password', 1);
INSERT INTO testing_test_user (username, password)              VALUES ('Andrew',   'password');


/* NEW MOVIE LIST DATA 
------------------------ */
INSERT INTO testing_movies_list_info (owner_id, list_name, list_description) VALUES (1, 'test list', 'testing movie list');

INSERT INTO testing_movies (id, title, poster) VALUES (100, 'testing100', 'none') ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;
INSERT INTO testing_movies (id, title, poster) VALUES (200, 'testing200', 'none') ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;

INSERT INTO testing_movies_list (movie_id, list_id, status, rating) VALUES (100, 1, 1, 5);
INSERT INTO testing_movies_list (movie_id, list_id, status, rating) VALUES (200, 1, 0, 2);

