DROP TABLE IF EXISTS genre_counts           CASCADE;
DROP TABLE IF EXISTS genres                 CASCADE;

DROP TABLE IF EXISTS friend_requests        CASCADE;
DROP TABLE IF EXISTS friends                CASCADE;

DROP TABLE IF EXISTS movies_list            CASCADE;
DROP TABLE IF EXISTS movies_list_statistics CASCADE;
DROP TABLE IF EXISTS movies_list_info       CASCADE;
DROP TABLE IF EXISTS movies                 CASCADE;

DROP TABLE IF EXISTS all_users              CASCADE;


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

