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

CREATE TABLE movies (
  id 		serial      PRIMARY KEY,
  name 	varchar(30)
);

CREATE TABLE movies_list_info (
  id                serial 	PRIMARY KEY,
  owner_id          int,
  editor_ids        TEXT,
  list_name         TEXT,
  list_description  TEXT,
  date_created      timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movies_list (
  movie_id 	int references movies(id),
  list_id 	int references movies_list_info(id),
  status 	  int DEFAULT    0,
  constraint pk_movies_list primary key (movie_id, list_id)
);



INSERT INTO test_user (username, password, privileges)
VALUES ('admin', 'password', 1);

INSERT INTO test_user (username, password)
VALUES ('Andrew', 'password');

INSERT INTO test_user (username, password)
VALUES ('Calvin', 'password');

INSERT INTO test_user (username, password)
VALUES ('Joseph', 'password');

INSERT INTO test_user (username, password)
VALUES ('Brendan', 'password');

INSERT INTO test_user (username, password)
VALUES ('Derrick', 'password');

INSERT INTO test_user (username, password)
VALUES ('Benas', 'password');


INSERT INTO movies (name) VALUES ('Star Wars');
INSERT INTO movies (name) VALUES ('Spongebob');
INSERT INTO movies (name) VALUES ('Batman');
INSERT INTO movies (name) VALUES ('James Bond');
INSERT INTO movies (name) VALUES ('Jurassic Park');



INSERT INTO movies_list_info (owner_id, list_name, list_description)
VALUES (1, 'test list', 'testing movie list');


INSERT INTO movies_list(movie_id, list_id)
VALUES (1, 1);

INSERT INTO movies_list(movie_id, list_id)
VALUES (2, 1);

INSERT INTO movies_list(movie_id, list_id)
VALUES (4, 1);















