DROP TABLE IF EXISTS movies_list;
DROP TABLE IF EXISTS movies_list_info;
DROP TABLE IF EXISTS movies     CASCADE;
DROP TABLE IF EXISTS test_user  CASCADE;



/* test_user:
--------------
  * should probably rename at some point
  * on user creation:
    - create a "general" movies list
    - cannot be deleted
    - special rules where any movie added to any other list is added to this one
  * add a trigger to create the general list on user creation
  * add rule to delete lists on user deletion
    - maybe transfer ownership to the oldest editorID if any
*/
CREATE TABLE test_user (
  id            serial 	  PRIMARY KEY,
  username      TEXT      UNIQUE NOT NULL,
  password      TEXT      NOT NULL,
  privileges    int       DEFAULT             0,
  date_joined   timestamp DEFAULT             CURRENT_TIMESTAMP,
  style_mode    int       DEFAULT             0
);



/* movies:
-----------
    Possible Additions:
      * total_score
        - (allows for average site-wide score)
        - after popularity, could add "total_score"
        - when somebody inserts the movie to their list, add the rating they give it
        - allows for site-wide movie average scores
      * average_score
        - could probably just calculate this on the fly whenever a movie is added
*/
CREATE TABLE movies (
    id 		      int     PRIMARY KEY,
    title 	    TEXT,
    poster      TEXT,
    popularity  int     DEFAULT 1
);



/* movies_list_info:
---------------------
    Future Functionality:
      * each user has a "general" list
        - automatically created
        - cant be deleted
        - when a movie is added to any other list, it is automatically added to this one as well
        - (if doing this, then the statistics data is only needed for lists, not users, since user stats would be equal to their general list)

    Possible Additions:
      * background image
        - select a movie from the list for which picture to use
        - defaults to white for empty lists
        - defaults to first movie added for other
      * various statistic
        - total watch time
        - genre counts
        - average release date
        - etc...

    AUTOMATICALLY UPDATED:
      * list length
      * watch counts
        - plan to watch
        - currently watching
        - finished
      * average rating
      * average release date
  
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
  finished          INTEGER       DEFAULT 0
);



/* movies_list:
----------------
    Possible Additions:
      * date_added to list
*/
CREATE TABLE movies_list (
  movie_id 	int references movies(id),
  list_id 	int references movies_list_info(id),
  status 	  int DEFAULT    0,
  rating 	  int DEFAULT    -1,
  constraint pk_movies_list primary key (movie_id, list_id)
);




/* genres: (automatically updated)
----------------------------------- 
CREATE TABLE genres (
  genre_id    INT   PRIMARY KEY,
  genre_name  TEXT  NOT NULL,
  popularity  INT   DEFAULT       0
);
*/


/* genre counts: (automatically updated)
----------------------------------------- 
CREATE TABLE genre_counts (
  list_id   INT REFERENCES  movies_list_info(id),
  genre_id  INT REFERENCES  genres(genre_id),
  count     INT DEFAULT     0
);
*/







/* TESTING DATA 
------------------------ */
INSERT INTO test_user (username, password, privileges)  VALUES ('admin',    'password', 1);
INSERT INTO test_user (username, password)              VALUES ('Andrew',   'password');
INSERT INTO test_user (username, password)              VALUES ('Calvin',   'password');
INSERT INTO test_user (username, password)              VALUES ('Joseph',   'password');
INSERT INTO test_user (username, password)              VALUES ('Brendan',  'password');
INSERT INTO test_user (username, password)              VALUES ('Derrick',  'password');
INSERT INTO test_user (username, password)              VALUES ('Benas',    'password');


/* NEW MOVIE LIST DATA 
------------------------ */
INSERT INTO movies_list_info (owner_id, list_name, list_description) VALUES (1, 'test list', 'testing movie list');

INSERT INTO movies (id, title, poster) VALUES (100, 'testing100', 'none') ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;
INSERT INTO movies (id, title, poster) VALUES (200, 'testing200', 'none') ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;

INSERT INTO movies_list (movie_id, list_id, status, rating) VALUES (100, 1, 1, 5);
INSERT INTO movies_list (movie_id, list_id, status, rating) VALUES (200, 1, 0, 2);

