
/* movie_list_info statistics update trigger:
----------------------------------------------
    * can probably be done a little more efficiently
        - i think you need some if-else stuff to know if the variable is NEW or OLD though
    * could also define a function which takes a variable? of list_id
        - trigger then just calls that function

*/
DROP FUNCTION IF EXISTS testing_movies_list_trigger();

CREATE OR REPLACE FUNCTION testing_movies_list_trigger() RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            UPDATE testing_movies_list_info 
                SET average_rating  = ( SELECT AVG(rating)::numeric(10,2) FROM testing_movies_list WHERE rating > 0 AND list_id = OLD.list_id),
                SET total_movies    = ( SELECT COUNT(*) FROM testing_movies_list WHERE list_id = OLD.list_id),
                SET plan_to_watch   = ( SELECT COUNT(*) FROM testing_movies_list WHERE status = 0 AND list_id = OLD.list_id),
                SET finished        = ( SELECT COUNT(*) FROM testing_movies_list WHERE status = 2 AND list_id = OLD.list_id),
                SET last_updated    = ( now() ) -- recently added is not changed like in the others, would need to figure this out
                WHERE id = OLD.list_id; 

            IF NOT FOUND THEN RETURN NULL; END IF;
            RETURN OLD;

        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE testing_movies_list_info 
                SET average_rating  = ( SELECT AVG(rating)::numeric(10,2) FROM testing_movies_list WHERE rating > 0 AND list_id = NEW.list_id),
                SET total_movies    = ( SELECT COUNT(*) FROM testing_movies_list WHERE list_id = NEW.list_id),
                SET plan_to_watch   = ( SELECT COUNT(*) FROM testing_movies_list WHERE status = 0 AND list_id = NEW.list_id),
                SET finished        = ( SELECT COUNT(*) FROM testing_movies_list WHERE status = 2 AND list_id = NEW.list_id),
                SET last_updated    = ( now() ),
                SET recently_added  = ( NEW.movie_id )
                WHERE id = NEW.list_id; 

            IF NOT FOUND THEN RETURN NULL; END IF;
            RETURN NEW;

        ELSIF (TG_OP = 'INSERT') THEN
            UPDATE testing_movies_list_info 
                SET average_rating  = ( SELECT AVG(rating)::numeric(10,2) FROM testing_movies_list WHERE rating > 0 AND list_id = NEW.list_id),
                SET total_movies    = ( SELECT COUNT(*) FROM testing_movies_list WHERE list_id = NEW.list_id),
                SET plan_to_watch   = ( SELECT COUNT(*) FROM testing_movies_list WHERE status = 0 AND list_id = NEW.list_id),
                SET finished        = ( SELECT COUNT(*) FROM testing_movies_list WHERE status = 2 AND list_id = NEW.list_id),
                SET last_updated    = ( now() ),
                SET recently_added  = ( NEW.movie_id )
                WHERE id = NEW.list_id; 

            RETURN NEW;
            
        END IF;
    END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS testing_movies_list_trigger ON testing_movies_list;


CREATE TRIGGER testing_movies_list_trigger
    AFTER INSERT OR UPDATE OR DELETE
    ON testing_movies_list
    FOR EACH ROW -- could you do ROW.id instead ? "postgresql create trigger for each row value of a specific column"
    EXECUTE PROCEDURE count_testing_movies_list_trigger();


