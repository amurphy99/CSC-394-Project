/* OTHER TRIGGERS NEEDED:
--------------------------
    * create "general" movie list when any new user is created
    * delete "general" movie list when any user is deleted
        - transfer ownership of other lists or delete them
        - delete both movie_list_info and movie_list table entries

    * if a user adds a movie to another list and it isn't in their general list yet, add it to their general list

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


