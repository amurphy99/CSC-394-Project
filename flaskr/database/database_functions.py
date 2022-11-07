from flaskr.db import get_db, close_db

'''
    Contains:
    ----------
        get_general_user_statistics(user_ids)
            * Function to get a the general statistics for a list of given users.

        get_general_movie_list(user_ids)
            * Function to get a list of all movies in the "general" list of given users.

'''


def get_general_user_statistics(user_ids):
    '''
    Function to get a the general statistics for a list of given users.
        input:
            * user_ids is a list of userIDs
            * example: [1, 2]
        
        returns:
            * dict of movie_list_info 
                - key   = a userID 
                - value = movie_list_info row corresponding to that userID
            * example: { 1: [...],  2: [...] }


            movie_list_info row is one row if this:
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
    '''
    # create return dict
    user_statistics_dict = {}

    # open db connection
    db = get_db()
    cur = db.cursor()

    for userID in user_ids:
        # make sure the user exists
        # --------------------------
        # select * from all_users where id = userID, cur.fetchall()[0] != None, etc etc
        # idk man i dont feel like doing this rn, just dont call it with random userIDs

        # get the users "general" movies_list_info
        # -------------------------------------------
        cur.execute( f"SELECT * FROM movies_list_info WHERE id = '{userID}' AND list_name = 'general';" )
        general_list_info = cur.fetchone()

        # add to the return dict
        # -----------------------
        user_statistics_dict[userID] = general_list_info

    # close the cursor and db connection
    cur.close(); db.close()
    close_db()

    # return the dict
    return user_statistics_dict




def get_general_movie_list(user_ids):
    '''
    Function to get a list of all movies in the "general" list of given users.
        input:
            * user_ids is a list of userIDs
            * example: [1, 2]
        
        returns:
            * dict of movie lists
                - key   = a userID 
                - value = list of movies_list rows (each row is also a list)
            * example: { 1: [[...], [...], ...],  2: [[...], [...], ...] }


            movies list row is one row if this:
                CREATE TABLE movies_list (
                    movie_id 	INTEGER   references  movies(id),
                    list_id 	INTEGER   references  movies_list_info(id),
                    status 	    INTEGER   DEFAULT     0,
                    rating 	    INTEGER   DEFAULT     -1,
                    date_added  TIMESTAMP DEFAULT     CURRENT_TIMESTAMP,
                    constraint pk_movies_list primary key (movie_id, list_id)
                );
    '''
    # create return dict
    movie_list_dict = {}

    # open db connection
    db = get_db(); cur = db.cursor()

    for userID in user_ids:
        # make sure the user exists
        # --------------------------
        # select * from all_users where id = userID, cur.fetchall()[0] != None, etc etc
        # idk man i dont feel like doing this rn, just dont call it with random userIDs

        # get the list id of the user's general list
        # -------------------------------------------
        cur.execute( f"SELECT * FROM movies_list_info WHERE id = '{userID}' AND list_name = 'general';" )
        general_list_id = cur.fetchone()[0]

        # get all movies from the general list
        # -------------------------------------
        cur.execute( f"SELECT * FROM movies_list WHERE list_id = '{general_list_id}';" )
        general_list_movies = cur.fetchall()

        # add to the return dict
        # -----------------------
        movie_list_dict[userID] = general_list_movies

    # close the cursor and db connection
    cur.close(); db.close()
    close_db()

    # return the dict
    return movie_list_dict



