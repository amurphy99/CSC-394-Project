
/* OLD STUFF THAT NEEDS TO BE DROPPED
------------------------ */
DROP TABLE IF EXISTS testing_movies_list;
DROP TABLE IF EXISTS testing_movies_list_info;
DROP TABLE IF EXISTS testing_movies     CASCADE;
DROP TABLE IF EXISTS testing_test_user  CASCADE;

DROP FUNCTION IF EXISTS testing_movies_list_trigger();
DROP TRIGGER IF EXISTS testing_movies_list_trigger ON testing_movies_list;



/* USER DATA 
------------------------ */
INSERT INTO all_users (username, password, privileges)
VALUES 
    ('admin',    'password', 1);

INSERT INTO all_users (username, password)
VALUES 
    ('Andrew',   'password'),
    ('Calvin',   'password'),
    ('Joseph',   'password'),
    ('Brendan',  'password'),
    ('Derrick',  'password'),
    ('Benas',    'password');



/* MOVIES
------------------------ */
INSERT INTO movies (id, title, poster) 
VALUES (11836, 'The SpongeBob SquarePants Movie', '/gjZD811kfY1ideNuBukcuCy8ocA.jpg') 
ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;

INSERT INTO movies (id, title, poster)
VALUES (400160, 'The SpongeBob Movie: Sponge on the Run', '/jlJ8nDhMhCYJuzOw3f52CP1W8MW.jpg') 
ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;

INSERT INTO movies (id, title, poster) 
VALUES (228165, 'The SpongeBob Movie: Sponge Out of Water', '/2WDmjUlSAPlA27i2OwEC7sRTFw3.jpg') 
ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;



/* MOVIES LIST INFO 
------------------------ */
INSERT INTO movies_list_info (owner_id, list_name, list_description) 
VALUES 
    (1, 'test list 1', 'testing movie list 1'),
    (2, 'test list 2', 'testing movie list 2');


/* MOVIES LIST
------------------------ */
INSERT INTO movies_list (movie_id, list_id, status, rating) 
VALUES 
    -- list 1
    (11836,  8, 0, 5),
    (400160, 8, 1, 5),
    (228165, 8, 2, 2),
    -- list 2
    (11836,  9, 0, 0),
    (400160, 9, 1, 5);








