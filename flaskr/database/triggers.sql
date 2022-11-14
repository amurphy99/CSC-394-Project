/* OTHER TRIGGERS NEEDED:
--------------------------
    * finish update_general_movies_list()

    * dont allow users to make a new movie list with the name "general"
    * dont allow addition of the same movie to a list twice

*/




/* movie_list_info statistics update trigger:
----------------------------------------------
    * can probably be done a little more efficiently
        - i think you need some if-else stuff to know if the variable is NEW or OLD though
    * could also define a function which takes a variable? of list_id
        - trigger then just calls that function

    * for updating the recenly added image in the DELETED case
        - if movies had a "date added to list" stat, then you could easily find the most recent movie that way

*/
DROP FUNCTION IF EXISTS update_movies_list_statistics();

CREATE OR REPLACE FUNCTION update_movies_list_statistics() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            UPDATE movies_list_info SET 
                average_rating  = ( SELECT AVG(rating)::numeric(10,2) FROM movies_list WHERE rating > 0 AND list_id = OLD.list_id),
                total_movies    = ( SELECT COUNT(*) FROM movies_list WHERE list_id = OLD.list_id),
                plan_to_watch   = ( SELECT COUNT(*) FROM movies_list WHERE status = 0 AND list_id = OLD.list_id),
                finished        = ( SELECT COUNT(*) FROM movies_list WHERE status = 2 AND list_id = OLD.list_id),
                last_updated    = ( now() ) -- recently added is not changed like in the others, would need to figure this out
                WHERE id = OLD.list_id; 

            IF NOT FOUND THEN RETURN NULL; END IF;
            RETURN OLD;

        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE movies_list_info SET 
                average_rating  = ( SELECT AVG(rating)::numeric(10,2) FROM movies_list WHERE rating > 0 AND list_id = NEW.list_id),
                total_movies    = ( SELECT COUNT(*) FROM movies_list WHERE list_id = NEW.list_id),
                plan_to_watch   = ( SELECT COUNT(*) FROM movies_list WHERE status = 0 AND list_id = NEW.list_id),
                finished        = ( SELECT COUNT(*) FROM movies_list WHERE status = 2 AND list_id = NEW.list_id),
                last_updated    = ( now() ),
                recently_added  = ( NEW.movie_id )
                WHERE id = NEW.list_id; 

            IF NOT FOUND THEN RETURN NULL; END IF;
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
            UPDATE movies_list_info SET 
                average_rating  = ( SELECT AVG(rating)::numeric(10,2) FROM movies_list WHERE rating > 0 AND list_id = NEW.list_id),
                total_movies    = ( SELECT COUNT(*) FROM movies_list WHERE list_id = NEW.list_id),
                plan_to_watch   = ( SELECT COUNT(*) FROM movies_list WHERE status = 0 AND list_id = NEW.list_id),
                finished        = ( SELECT COUNT(*) FROM movies_list WHERE status = 2 AND list_id = NEW.list_id),
                last_updated    = ( now() ),
                recently_added  = ( NEW.movie_id )
                WHERE id = NEW.list_id; 

            RETURN NEW;
            
        END IF;
    END;
$$ LANGUAGE plpgsql;


/* Create the trigger (drop it if it already exists too)
--------------------------------------------------------- */
DROP TRIGGER IF EXISTS movies_list_statistics_trigger ON movies_list;

CREATE TRIGGER movies_list_statistics_trigger
    AFTER INSERT OR UPDATE OR DELETE
    ON movies_list
    FOR EACH ROW -- could you do ROW.id instead ? "postgresql create trigger for each row value of a specific column"
    EXECUTE PROCEDURE update_movies_list_statistics();









/* general movie list creation and deletion:
----------------------------------------------
    * create "general" movie list when any new user is created
    * delete "general" movie list when any user is deleted
        - transfer ownership of other lists or delete them
        - delete both movie_list_info and movie_list table entries

    general_movies_list_control()
    general_movies_list_control_trigger

*/
DROP FUNCTION IF EXISTS general_movies_list_control();

CREATE OR REPLACE FUNCTION general_movies_list_control() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            -- delete all of the movies from their movie lists
            -- on user deletion delete their general movies list
            -- later on do something about their other lists: if there were other editors than give one ownership
            DELETE FROM movies_list WHERE list_id = (SELECT id FROM movies_list_info WHERE id = OLD.id);
            DELETE FROM movies_list_info WHERE id = OLD.id;
            RETURN OLD;

        ELSIF (TG_OP = 'INSERT') THEN
            -- on user creation create a new general movies list
            INSERT INTO movies_list_info (owner_id, list_name, list_description)
            VALUES (NEW.id, 'general', CONCAT(NEW.username, '''s general movie list.'));
            RETURN NEW;
            
        END IF;
    END;
$$ LANGUAGE plpgsql;


/* Create the trigger (drop it if it already exists too)
--------------------------------------------------------- */
DROP TRIGGER IF EXISTS general_movies_list_control_trigger ON all_users;

CREATE TRIGGER general_movies_list_control_trigger
    AFTER INSERT OR DELETE
    ON all_users
    FOR EACH ROW -- could you do ROW.id instead ? "postgresql create trigger for each row value of a specific column"
    EXECUTE PROCEDURE general_movies_list_control();











/* trigger for updating general list
----------------------------------------------
    * if a user adds a movie to another list and it isn't in their general list yet, add it to their general list

    update_general_movies_list()
    update_general_movies_list_trigger

*/
DROP FUNCTION IF EXISTS update_general_movies_list();

CREATE OR REPLACE FUNCTION update_general_movies_list() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            RETURN OLD;

        ELSIF (TG_OP = 'UPDATE') THEN
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
            -- check if the name of the list is general
            IF NOT ((SELECT list_name FROM movies_list_info WHERE id = NEW.list_id) = 'general') THEN

                INSERT INTO movies_list (movie_id, list_id, status, rating) 
                VALUES (
                    NEW.movie_id, 
                    (SELECT id FROM movies_list_info WHERE 
                        list_name = 'general' AND 
                        owner_id = (SELECT owner_id FROM movies_list_info WHERE id = NEW.list_id)), 
                    NEW.status, 
                    NEW.rating);

            END IF;
            RETURN NEW;
            
        END IF;
    END;
$$ LANGUAGE plpgsql;


/* Create the trigger (drop it if it already exists too)
--------------------------------------------------------- */
DROP TRIGGER IF EXISTS update_general_movies_list_trigger ON movies_list;

CREATE TRIGGER update_general_movies_list_trigger
    AFTER INSERT OR UPDATE OR DELETE
    ON movies_list
    FOR EACH ROW -- could you do ROW.id instead ? "postgresql create trigger for each row value of a specific column"
    EXECUTE PROCEDURE update_general_movies_list();




/* trigger for creating movies_list_statistics
----------------------------------------------
    * if a user adds a movie to another list and it isn't in their general list yet, add it to their general list

    create_movies_list_statistics()
    create_movies_list_statistics_trigger

*/
DROP FUNCTION IF EXISTS create_movies_list_statistics();

CREATE OR REPLACE FUNCTION create_movies_list_statistics() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            DELETE FROM movies_list_statistics WHERE list_id = NEW.id;
            IF NOT FOUND THEN RETURN NULL; END IF;
            RETURN OLD;

        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO movies_list_statistics (list_id) VALUES (NEW.id);
            RETURN NEW;
            
        END IF;
    END;
$$ LANGUAGE plpgsql;


/* Create the trigger (drop it if it already exists too)
--------------------------------------------------------- */
DROP TRIGGER IF EXISTS create_movies_list_statistics_trigger ON movies_list_info;

CREATE TRIGGER create_movies_list_statistics_trigger
    AFTER INSERT OR DELETE
    ON movies_list_info
    FOR EACH ROW -- could you do ROW.id instead ? "postgresql create trigger for each row value of a specific column"
    EXECUTE PROCEDURE create_movies_list_statistics();