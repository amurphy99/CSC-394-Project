DROP TABLE IF EXISTS test_user;


CREATE TABLE test_user (
  id            TEXT  PRIMARY KEY,
  username      TEXT    UNIQUE NOT NULL,
  password      TEXT    NOT NULL,
  privileges    integer DEFAULT             0
);


INSERT INTO test_user (id, username, password, privileges)
VALUES ('T01', 'admin', 'password', 1);

INSERT INTO test_user (id, username, password)
VALUES ('T02', 'Andrew', 'password');

INSERT INTO test_user (id, username, password)
VALUES ('T03', 'Calvin', 'password');

INSERT INTO test_user (id, username, password)
VALUES ('T04', 'Joseph', 'password');

INSERT INTO test_user (id, username, password)
VALUES ('T05', 'Brendan', 'password');

INSERT INTO test_user (id, username, password)
VALUES ('T06', 'Derrick', 'password');

INSERT INTO test_user (id, username, password)
VALUES ('T07', 'Benas', 'password');

CREATE TABLE MOVIES (
  MID     TEXT  PRIMARY KEY,
  Name    TEXT    NOT NULL,
  Rating  integer    NOT NULL
);

INSERT INTO MOVIES (MID, Name, Rating)
VALUES ('M01', 'John Wick', 6);

INSERT INTO MOVIES (MID, Name, Rating)
VALUES ('M02', 'Mission Impossible', 8);

INSERT INTO MOVIES (MID, Name, Rating)
VALUES ('M03','Jumanji', 8);

INSERT INTO MOVIES (MID, Name, Rating)
VALUES ('M04','London has Fallen', 9);

INSERT INTO MOVIES (MID, Name, Rating)
VALUES ('M05','Game of Thrones', 7);


CREATE TABLE MOVIESLIST (
  UserID  TEXT    NOT NULL,
  FOREIGN KEY (UserID) REFERENCES test_user(id),
  MID     TEXT    NOT NULL,
  FOREIGN KEY (MID) REFERENCES MOVIES(MID),
  STATUS  TEXT    NOT NULL,
  PRIMARY KEY(UserID, MID)
);

INSERT INTO MOVIESLIST (userID, MID, STATUS)
VALUES ('T01', 'M01', 'YES');

INSERT INTO MOVIESLIST (userID, MID, STATUS)
VALUES ('T01', 'M02', 'YES');

INSERT INTO MOVIESLIST (userID, MID, STATUS)
VALUES ('T03', 'M01', 'NO');

INSERT INTO MOVIESLIST (userID, MID, STATUS)
VALUES ('T05', 'M05', 'NO');

INSERT INTO MOVIESLIST (userID, MID, STATUS)
VALUES ('T03', 'M02', 'YES');

INSERT INTO MOVIESLIST (userID, MID, STATUS)
VALUES ('T07', 'M05', 'YES');


