DROP TABLE IF EXISTS test_user;

DROP TABLE IF EXISTS task_config;
DROP TABLE IF EXISTS task_response;



CREATE TABLE test_user (
  id            serial  PRIMARY KEY,
  username      TEXT    UNIQUE NOT NULL,
  password      TEXT    NOT NULL,
  privileges    integer DEFAULT             0
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



