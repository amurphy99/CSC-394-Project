from flask import Flask, render_template, g, request, flash, session

from flaskr.db import get_db, close_db
from flaskr.database.database_functions import get_general_user_statistics, get_general_movie_list



def preview_database():

    # get info from database
    # -----------------------
    db = get_db(); cur = db.cursor()

    cur.execute( f"SELECT * FROM movies_list_info;" )
    movies_list_infos = cur.fetchall()
    
    cur.execute( f"SELECT * FROM movies_list_statistics;" )
    movies_list_statistics = cur.fetchall()
    
    cur.execute( f"SELECT * FROM genres;" )
    genres = cur.fetchall()

    cur.execute( f"SELECT * FROM genre_counts;" )
    genre_counts = cur.fetchall()

    cur.execute( f"SELECT * FROM friend_requests;" )
    friend_requests = cur.fetchall()

    cur.execute( f"SELECT * FROM friends;" )
    friends = cur.fetchall()

    cur.close(); db.close()
    close_db()


    headers = { "movies_list_info"       : ["id", "owner_id", "list_name", "recently_added", "average_rating", "total_movies"],
                "movies_list_statistics" : ["list_id", "total_movies", "total_runtime", "total_budget"],
                "genres"                 : ["genre_id", "genre_name", "popularity"],
                "genre_counts"           : ["list_id", "genre_id", "count"],
                "friend_requests"        : ["sender_id", "receiver_id", "date_created"],
                "friends"                : ["friend_1_id", "friend_2_id", "date_created"] }

    movies_list_info_reduced = [0,1,3,5,8,9]


    # return the template with all of the information we assembled for display
    return render_template( 'api_testing/preview_database.html', 
                            headers                     = headers, 
                            movies_list_infos           = movies_list_infos, 
                            movies_list_info_reduced    = movies_list_info_reduced,
                            movies_list_statistics      = movies_list_statistics,
                            genres                      = genres,
                            genre_counts                = genre_counts,
                            friend_requests             = friend_requests,
                            friends                     = friends                    ) 

