
from flaskr.db import get_db

'''
    This file is for compiling all of the database commands and access into one place
        * in case of database layout or naming changes, can easily be changed here

'''



def add_movie(listID, movie, userID, watch_status, rating):
    # in the future could also include userID in inputs for permission verification
    '''
        movie           = eval(request.form["movie_info"    ])
        listID          = int (request.form["listID"        ])
        userID          = int (request.form["userID"        ])
        watch_status    = int (request.form["watch-status"  ])
        rating          = int (request.form["rating"        ])



        # add to movies_list table
        cur.execute(f"INSERT INTO movies_list (movie_id, list_id, status, rating) VALUES ('{f_movie_id}', '{listID}', '{watch_status}', '{rating}')")
        db.commit()
        
        cur.close(); db.close()
    
    
    '''
    # prepare sql statements
    f_movie_id      = movie["info"][1][1]
    f_movie_title   = movie["info"][0][1]
    f_movie_source  = movie["source"]

    # database commands start
    db = get_db(); cur = db.cursor()

    # first add/update the movie table
    # if it is already in the general movies table, increase its "popularity" by 1
    cur.execute(  f"INSERT INTO movies  (  id,                title,             poster          ) \
                    VALUES              ('{f_movie_id}',    '{f_movie_title}', '{f_movie_source}') \
                    ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;"               )
    db.commit()

    # add to movies_list table
    cur.execute(f"INSERT INTO movies_list (movie_id, list_id, status, rating) VALUES ('{f_movie_id}', '{listID}', '{watch_status}', '{rating}')")
    db.commit()
    

    cur.close(); db.close()


    return






