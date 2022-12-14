from flaskr.db import get_db, close_db
from flaskr.movieDBapi import api_movie_page


'''
Contains:
    
    Retrive Information:
    ---------------------
        def get_poster(movie_id)
            * Function to get the movie poster source for a movie id.

        get_watch_list_statistics(list_id)
            * Function to get all statistics for a watch list id.

        get_general_user_statistics(user_ids)
            * Function to get a the general statistics for a list of given users.

        get_general_movie_list(user_ids)
            * Function to get a list of all movies in the "general" list of given users.


    Modifying the Database:
    ------------------------
        add_movie_to_list(movie_dictionary)
            * Function to add a movie to the movies_list table, returns None.

        
    Friends List Utility:
    ----------------------
        send_friend_request(sender_id, receiver_id)
            * Function to send a friend request from one user to another, returns None.
        
        resolve_friend_request(sender_id, receiver_id, answer)
            * Function to accept or deny an active friend request, returns None.

'''


def get_poster(movie_id):
    '''
    Function to get the movie poster source for a movie id.

    '''
    # open db connection
    db = get_db(); cur = db.cursor()

    # get the users "general" movies_list_info
    # -------------------------------------------
    cur.execute( f"SELECT poster FROM movies WHERE id = '{movie_id}';" )
    poster_path = cur.fetchone()

    # close the cursor and db connection
    cur.close()#; db.close()
    

    if len(poster_path) == 0: return ""

    return poster_path[0]



def get_watch_list_statistics(list_id):
    '''
    Function to get all statistics for a watch list id.

    '''
    # open db connection
    db = get_db(); cur = db.cursor()

    # get the users "general" movies_list_info
    # -------------------------------------------
    cur.execute( f"SELECT * FROM movies_list_info WHERE id = '{list_id}';" )
    general_list_info = cur.fetchone()

    # get the users "general" movies_list_statstics
    # ----------------------------------------------
    cur.execute( f"SELECT * FROM movies_list_statistics WHERE list_id = '{list_id}';" )
    general_list_statistics = cur.fetchone()

    # close the cursor and db connection
    cur.close()#; db.close()
    
    
    return [general_list_info, general_list_statistics]


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

    '''
    # create return dict
    user_statistics_dict = {}

    # open db connection
    db = get_db(); cur = db.cursor()

    for userID in user_ids:
        # make sure the user exists
        # --------------------------
        # select * from all_users where id = userID, cur.fetchall()[0] != None, etc etc
        # idk man i dont feel like doing this rn, just dont call it with random userIDs

        # get the users "general" movies_list_info
        # -------------------------------------------
        cur.execute( f"SELECT * FROM movies_list_info WHERE owner_id = '{userID}' AND list_name = 'general';" )
        general_list_info = cur.fetchone()
        #print(general_list_info)

        # get the users "general" movies_list_statstics
        # ----------------------------------------------
        cur.execute( f"SELECT * FROM movies_list_statistics WHERE list_id = '{general_list_info[0]}';" )
        general_list_statistics = cur.fetchone()

        # add to the return dict
        # -----------------------
        user_statistics_dict[userID] = [general_list_info, general_list_statistics]

    # close the cursor and db connection
    cur.close()#; db.close()
    

    # return the dict
    return user_statistics_dict


def get_general_list_id(user_id):

    # open db connection
    db = get_db(); cur = db.cursor()

    cur.execute( f"SELECT id FROM movies_list_info WHERE owner_id = '{user_id}' AND list_name = 'general';" )
    general_list_id = cur.fetchone()[0]

    # close the cursor and db connection
    cur.close()#; db.close()

    return general_list_id




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
            * example: { 1: [[...], [...], ...],  
                         2: [[...], [...], ...]  }

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
        cur.execute( f"SELECT * FROM movies_list_info WHERE owner_id = '{userID}' AND list_name = 'general';" )
        general_list_id = cur.fetchone()[0]

        # get all movies from the general list
        # -------------------------------------
        cur.execute( f"SELECT * FROM movies_list WHERE list_id = '{general_list_id}';" )
        general_list_movies = cur.fetchall()

        # add to the return dict
        # -----------------------
        movie_list_dict[userID] = general_list_movies

    # close the cursor and db connection
    cur.close()#; db.close()
    

    # return the dict
    return movie_list_dict









def add_movie_to_list(movie_dictionary):
    '''
    Function to add a movie to the movies_list table, returns None.

    receive (as a dictionary):
    ---------------------------
            - list_id
            - rating
            - watch_status
            - movie_id

            - movie_title title
            - movie_poster poster_path
            - runtime runtime
            - budget  budget
            - genres genres

        * later possibilities
            release_date
            revenue

    things to do:
    -------------
        * already have:
            - add movie to movies table (check if already in)
            - add movie and entry data to movies_list table
        
        * new:
            - recalc total movies, runtime, and budget
    
    '''
    # prepare data for sql statements
    # --------------------------------
    f_movie_id      = int (movie_dictionary["movie_id"])
    f_list_id       = int (movie_dictionary["list_id"])
    f_watch_status  = int (movie_dictionary["watch_status"])
    f_rating        = int (movie_dictionary["rating"])

    movie_response = api_movie_page(f_movie_id)
    f_movie_title   = str (movie_response["title"])
    f_movie_source  = str (movie_response["poster_path"])
    f_movie_budget  = int (movie_response["budget"])
    f_movie_runtime = int (movie_response["runtime"])
    movie_genres    = movie_response["genres"]

    f_movie_title = f_movie_title.replace("'", "''")


    # open db connection
    db = get_db(); cur = db.cursor()

    # check if being added to general list
    cur.execute(f"SELECT list_name FROM movies_list_info WHERE id = {f_list_id};")
    list_name = cur.fetchone()[0]
    if list_name == "general":  general_list = True
    else:                       general_list = False

    # get the users id
    cur.execute(f"SELECT owner_id FROM movies_list_info WHERE id = {f_list_id};")
    user_id = cur.fetchone()[0]


    # check if the movie is already in the movies_list table
    cur.execute(f"SELECT * FROM movies_list WHERE list_id = {f_list_id} AND movie_id = {f_movie_id};")
    already_in = cur.fetchall()

    if len(already_in) == 0:
        # add movie to movies table
        cur.execute(  f"INSERT INTO movies (id, title, poster) \
                        VALUES ('{f_movie_id}', '{f_movie_title}', '{f_movie_source}') \
                        ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity + 1;" )

        # add to movies_list table
        cur.execute(  f"INSERT INTO movies_list (movie_id, list_id, status, rating) \
                        VALUES ('{f_movie_id}', '{f_list_id}', '{f_watch_status}', '{f_rating}');")

        # now do statistics:
        # -------------------
        cur.execute(f"SELECT * FROM movies_list_statistics WHERE list_id = {f_list_id};")
        current_list_statistics = cur.fetchone()
        new_total_movies    = current_list_statistics[1] + 1
        new_total_runtime   = current_list_statistics[2] + f_movie_runtime
        new_total_budget    = current_list_statistics[3] + f_movie_budget # should do something for if it is 0

        cur.execute(  f"UPDATE movies_list_statistics \
                        SET total_movies = {new_total_movies}, total_runtime = {new_total_runtime}, total_budget = {new_total_budget} \
                        WHERE list_id = {f_list_id};")

        # genre changes - receive a list of genres

        for genre in movie_genres:
            genre_id    = int(genre["id"])
            genre_name  = str(genre["name"])

            # get the genres info
            cur.execute(f"SELECT * FROM genres WHERE genre_id = {genre_id};")
            genre_info = cur.fetchall()

            # if the genre is not already in the database
            if len(genre_info) == 0:
                cur.execute(f"INSERT INTO genres (genre_id, genre_name) VALUES ({genre_id}, '{genre_name}');")
            else:
                cur.execute(f"UPDATE genres SET popularity = popularity + 1 WHERE genre_id = {genre_id} AND genre_name = '{genre_name}';")
            
            # now insert into table bc we know it is in
            cur.execute(  f"INSERT INTO genre_counts (list_id, genre_id, count) \
                            VALUES ('{f_list_id}', '{genre_id}', {1}) \
                            ON CONFLICT (list_id, genre_id) DO UPDATE SET count = EXCLUDED.count + 1;" )

        # commit changes
        db.commit()

    # close the cursor and db connection
    cur.close()#; db.close()



    # add to general list if not already being added to general list
    if not general_list:
        general_list_id = get_general_list_id(user_id)
        new_movie_dictionary = movie_dictionary
        new_movie_dictionary["list_id"] = general_list_id
        add_movie_to_list(new_movie_dictionary)


    # maybe add a success/failure feedback message
    return None







def send_friend_request(sender_id, receiver_id):
    '''
    Function to send a friend request from one user to another, returns None.

    if there is a friend request already open between the two
        - (this would be from the other way around)
        - accept it

    '''
    # open db connection
    db = get_db(); cur = db.cursor()

    # check for any existing requests the other way around for these 2 users
    cur.execute(f"SELECT * FROM friend_requests WHERE sender_id = {receiver_id} AND receiver_id = {sender_id};")
    existing_request = cur.fetchall()

    if len(existing_request) == 0:
        # send friend request
        cur.execute(f"INSERT INTO friend_requests (sender_id, receiver_id) VALUES ({sender_id}, {receiver_id});")
        db.commit()

    else:
        # this might cause problems because of the database open and close issue
        resolve_friend_request(receiver_id, sender_id, 1)

    # close the cursor and db connection
    cur.close()#; db.close()
    

    # maybe add a success/failure feedback message
    return None



def resolve_friend_request(sender_id, receiver_id, answer):
    '''
    Function to accept or deny an active friend request, returns None.

    remove the friend request from the requests table
    if accepted, also add it to the friends table

    answer:
        0 = denied
        1 = accepted

    '''
    # open db connection
    db = get_db(); cur = db.cursor()

    # remove the old friend request
    cur.execute(f"DELETE FROM friend_requests WHERE sender_id = {sender_id} AND receiver_id = {receiver_id};")

    # if accepted, also add it to the friends table
    if answer == 1:
        cur.execute(f"INSERT INTO friends (friend_1_id, friend_2_id) VALUES ({sender_id}, {receiver_id});")

    # commit changes
    db.commit()

    # close the cursor and db connection
    cur.close()#; db.close()
    

    # maybe add a success/failure feedback message
    return None




def remove_friend(user_id, other_id):
    # open db connection
    db = get_db(); cur = db.cursor()

    cur.execute(  f"DELETE FROM friends WHERE \
                    (friend_1_id = { user_id} AND friend_2_id = {other_id}) OR \
                    (friend_1_id = {other_id} AND friend_2_id = { user_id});")
    db.commit()

    # close the cursor and db connection
    cur.close()#; db.close()








def get_friends_list(user_id):
    # return list
    friends_list = []
    
    # open db connection
    db = get_db(); cur = db.cursor()

    # check if the movie is already in the movies_list table
    cur.execute(f"SELECT * FROM friends WHERE friend_1_id = {user_id} OR friend_2_id = {user_id};")
    user_friends = cur.fetchall()

    for friend in user_friends:
        if friend[0] != user_id:
            cur.execute(f"SELECT * FROM all_users WHERE id = {friend[0]};")
            friend_row = cur.fetchone()
            friends_list.append( [friend_row[1], friend[0]] )
        else:
            cur.execute(f"SELECT * FROM all_users WHERE id = {friend[1]};")
            friend_row = cur.fetchone()
            friends_list.append( [ friend_row[1], friend[1]] )

    # close the cursor and db connection
    cur.close()#; db.close()

    return friends_list


def get_relationship(user_id, other_id):
    '''
    0 = not friends, no requests
    1 = friends
    2 = outgoing friend request
    3 = incoming friend request
    '''
    # open db connection
    db = get_db(); cur = db.cursor()

    # check if already friends
    # -------------------------
    cur.execute(f"SELECT * FROM friends WHERE friend_1_id = {user_id} AND friend_2_id = {other_id};")
    user_friends = cur.fetchall()

    cur.execute(f"SELECT * FROM friends WHERE friend_1_id = {other_id} AND friend_2_id = {user_id};")
    user_friends_2 = cur.fetchall()

    if len(user_friends) > 0 or len(user_friends_2) > 0:
        cur.close()
        return 1


    # check if pending friend request 
    # --------------------------------
    cur.execute(f"SELECT * FROM friend_requests WHERE sender_id = {user_id} AND receiver_id = {other_id};")
    user_friends = cur.fetchall()
    if len(user_friends) > 0:
        cur.close()
        return 2

    cur.execute(f"SELECT * FROM friend_requests WHERE sender_id = {other_id} AND receiver_id = {user_id};")
    user_friends = cur.fetchall()
    if len(user_friends) > 0:
        cur.close()
        return 3


    # close the cursor and db connection
    cur.close()

    return 0


def update_bio(new_bio, user_id):
    # open db connection
    db = get_db(); cur = db.cursor()
    
    cur.execute(  f"UPDATE movies_list_info SET list_description = '{new_bio}' \
                    WHERE owner_id = {user_id} AND list_name = 'general';"      )
    db.commit()

    # close the cursor and db connection
    cur.close()



def get_friend_requests(user_id):
    incoming = []
    outgoing = []

    # open db connection
    db = get_db(); cur = db.cursor()

    cur.execute(f"SELECT * FROM friend_requests WHERE receiver_id = {user_id};")
    incoming_requests = cur.fetchall()
    for request in incoming_requests:
        cur.execute(f"SELECT username FROM all_users WHERE id = {request[0]};")
        sender_username = cur.fetchone()
        formatted_date  = request[2].strftime("%Y-%m-%d %H:%M:%S")

        incoming.append( (request[0], request[1], request[2], sender_username[0], formatted_date) )


    cur.execute(f"SELECT * FROM friend_requests WHERE sender_id = {user_id};")
    outgoing_requests = cur.fetchall()
    for request in outgoing_requests: 
        cur.execute(f"SELECT username FROM all_users WHERE id = {request[1]};")
        receiver_username = cur.fetchone()
        formatted_date    = request[2].strftime("%Y-%m-%d %H:%M:%S")

        outgoing.append( (request[0], request[1], request[2], receiver_username[0], formatted_date) )

    # close the cursor and db connection
    cur.close()

    friend_requests = { "incoming_requests" : incoming, 
                        "outgoing_requests" : outgoing     }

    return friend_requests


def genres_string(list_id):
    # prep for return
    genre_string = ""

    # open db connection
    db = get_db(); cur = db.cursor()
    
    cur.execute( f"SELECT * FROM genre_counts WHERE list_id = {list_id};" )
    results = cur.fetchall()

    if len(results) == 0:
        cur.close()
        return ""

    for entry in results:
        cur.execute( f"SELECT genre_name FROM genres WHERE genre_id = {entry[1]};" )
        name = cur.fetchone()
        genre_string += f"{name[0]}:{entry[2]}, "

    # close the cursor and db connection
    cur.close()
    #print(genre_string)

    return genre_string[:-2]
