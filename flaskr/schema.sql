DROP TABLE IF EXISTS movies_list;
DROP TABLE IF EXISTS movies_list_info;

DROP TABLE IF EXISTS movies     CASCADE;
DROP TABLE IF EXISTS test_user  CASCADE;


CREATE TABLE test_user (
  id            serial 	  PRIMARY KEY,
  username      TEXT      UNIQUE NOT NULL,
  password      TEXT      NOT NULL,
  privileges    int       DEFAULT             0,
  date_joined   timestamp DEFAULT             CURRENT_TIMESTAMP,
  style_mode    int       DEFAULT             0
);


/*
movies
-------
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


/* 
movies_list_info
-----------------
    Future Functionality:
        * each user has a "general" list
            - automatically created
            - cant be deleted
            - when a movie is added to any other list, it is automatically added to this one as well
            - (if doing this, then the statistics data is only needed for lists, not users, since user stats would be equal to their general list)

    Possible Additions:
        * various statistics
          - total watch time
          - genre counts
          - average rating
          - etc...
*/
CREATE TABLE movies_list_info (
  id                serial 	PRIMARY KEY,
  owner_id          int,
  editor_ids        TEXT,
  list_name         TEXT,
  list_description  TEXT,
  date_created      timestamp DEFAULT CURRENT_TIMESTAMP
);


/* 
movies_list
------------
    Possible Additions:
        * date_added
*/
CREATE TABLE movies_list (
  movie_id 	int references movies(id),
  list_id 	int references movies_list_info(id),
  status 	  int DEFAULT    0,
  rating 	  int DEFAULT    -1,
  constraint pk_movies_list primary key (movie_id, list_id)
);





/* TESTING DATA 
------------------------ */
INSERT INTO test_user (username, password, privileges) VALUES ('admin', 'password', 1);

INSERT INTO test_user (username, password) VALUES ('Andrew', 'password');

INSERT INTO test_user (username, password) VALUES ('Calvin', 'password');

INSERT INTO test_user (username, password) VALUES ('Joseph', 'password');

INSERT INTO test_user (username, password) VALUES ('Brendan', 'password');

INSERT INTO test_user (username, password) VALUES ('Derrick', 'password');

INSERT INTO test_user (username, password) VALUES ('Benas', 'password');


/* NEW MOVIE LIST DATA 
------------------------ */
INSERT INTO movies_list_info (owner_id, list_name, list_description) VALUES (1, 'test list', 'testing movie list');
















