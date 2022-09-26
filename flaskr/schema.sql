DROP TABLE IF EXISTS test_user;
DROP TABLE IF EXISTS books;


CREATE TABLE test_user (
  id            serial  PRIMARY KEY,
  username      TEXT    UNIQUE NOT NULL,
  password      TEXT    NOT NULL,
  privelages    integer DEFAULT             0
);

INSERT INTO test_user (username, password, privelages)
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



CREATE TABLE books (id          serial      PRIMARY KEY,
                    title       varchar     (150) NOT NULL,
                    author      varchar     (50) NOT NULL,
                    pages_num   integer     NOT NULL,
                    review      text,
                    date_added  date        DEFAULT CURRENT_TIMESTAMP);

INSERT INTO books (title, author, pages_num, review)
VALUES ('A Tale of Two Cities',
        'Charles Dickens',
        489,
        'A great classic!');

INSERT INTO books (title, author, pages_num, review)
VALUES ('Anna Karenina',
        'Leo Tolstoy',
        864,
        'Another great classic!');