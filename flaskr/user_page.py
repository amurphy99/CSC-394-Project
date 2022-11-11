from flask import Flask, render_template, g, request, flash, session

from flaskr.db import get_db, close_db
from flaskr.database.database_functions import get_general_user_statistics, get_general_movie_list

def format_time(time):
    days    = int(time // (24*60))
    hours   = int((time-(days*24)) // 60)
    minutes = int(time-((days*24*60)+(hours*60)))

    formatted_time = ""
    if days > 0: 
        formatted_time += f"{days:2}d "
        formatted_time += f"{hours:2}h "
        formatted_time += f"{minutes:2}m"
        return formatted_time

    elif hours > 0:
        formatted_time += f"{hours:2}h "
        formatted_time += f"{minutes:2}m"
        return formatted_time

    else:
        formatted_time += f"{minutes:2}m"
        return formatted_time




#@app.route('/user/<userID>', methods=('GET', 'POST'))
def user_page(userID):
    '''
    GET request only

    takes:
        * userID

    returns:
        * user_info
        * statistics
        * user_lists
    
    '''
    # get info from database
    # -----------------------
    db = get_db(); cur = db.cursor()

    cur.execute( f"SELECT * FROM all_users WHERE id = '{userID}';" )
    this_user = cur.fetchone()

    cur.execute( f"SELECT * FROM movies_list_info WHERE owner_id = '{userID}';" )
    user_lists = cur.fetchall()

    cur.close(); db.close()
    close_db()


    # get general list for stats
    # ---------------------------
    general_lists           = get_general_user_statistics([ this_user[0] ])
    general_list_info       = general_lists[this_user[0]][0]
    general_list_statistics = general_lists[this_user[0]][1]

    plan_to_watch       = general_list_info[10]   
    currently_watching  = (general_list_info[9] - (general_list_info[10] + general_list_info[11]))
    finished            = general_list_info[11]  
    user_bio            = general_list_info[4]
    total_movies        = int(general_list_statistics[1])
    total_watch_time    = format_time(general_list_statistics[2])
    total_budget        = f"${general_list_statistics[3]:,}"

    if total_movies == 0:
        average_watch_time  = "--"
        average_budget      = "--"
    else:
        average_watch_time  = format_time((round((general_list_statistics[2]/total_movies),2)))
        average_budget      = f"${round((general_list_statistics[3]/total_movies),2):,}"

    # prepare stats
    # --------------
    statistics = [  ("Joined:",             str(this_user[4])[:10]  ),
                    ("Total Movies Added:", total_movies            ),
                    ("Total Runtime:",      total_watch_time        ), 
                    ("Average Runtime:",    average_watch_time      ),
                    ("Total Budget:",       total_budget            ), 
                    ("Average Budget:",     average_budget          ),  
                    ("Movies Completed:",   finished                ), 
                    ("Currently Watching:", currently_watching      ), 
                    ("Plan to Watch:",      plan_to_watch           )   ] 



    # -------------------------------------------------------------------------------
    # area for the comparison code
    # -------------------------------------------------------------------------------

    '''
    statistics comparison notes:
    -----------------------------
    (just ideas, dont have to do exacly this)

        if not signed in:
            return "sign in to compare your watch histories!"

        if signed in:
            num movies in common
            num movies youve seen that they havent
            num movies theyve seen that you havent
            % match, out of total unique movies between the two of you, % that u both have seen

        if movies in common >= 6:
            top 3 closest agreement in rating + their raitng + your rating 
            top 3 biggest disagreement in rating + their raitng + your rating 
    
    '''

    # checks if the current user is logged in
    if g.user != None:
        # look in database/database_functions.py for more info on what this gives
        movie_lists = get_general_movie_list([userID, g.user[0]])



    # prepare the user comparison data for the page
    user_comparison = [ ("Similar Movies",      10),
                        ("Different Movies",    10) ]


    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------


    # return the template with all of the information we assembled for display
    return render_template( 'user_page/user_page.html', 
                            this_user       = this_user, 
                            user_bio        = user_bio,
                            user_lists      = user_lists, 
                            statistics      = statistics, 
                            user_comparison = user_comparison   )














#@app.route('/new_list_modal', methods=('POST'))
def new_list_modal():
    return render_template('user_page/new_list_modal.html')



# app.add_url_rule('/user/create_new_list', methods=('GET', 'POST'), view_func=user_page.create_new_list)
def create_new_list():

    # make sure to double check the user is logged in
    if g.user == None:
        error = 'Error: not logged in'
        flash(error)
        return

    # create the new watch list
    if request.method == 'POST':
        new_title   = str(request.form["new-list-title"])
        new_desc    = str(request.form["new-list-description"])
        userID      = int(request.form["userID"])


        db = get_db(); cur = db.cursor()

        cur.execute( f"INSERT INTO movies_list_info (owner_id, list_name, list_description) VALUES ({userID}, '{new_title}', '{new_desc}') RETURNING *;" )
        db.commit()
        new_list = cur.fetchone()
        
        cur.close(); db.close()


        return render_template('user_page/list_created_htmx.html', new_list=new_list)


    return



'''      
sample api output:
-------------------
{
   "adult":false,
   "backdrop_path":"/yzqaKAhglTrkeOfuIXYYArf0WnA.jpg",
   "belongs_to_collection":{
      "id":137697,
      "name":"Finding Nemo Collection",
      "poster_path":"/ucM59odfzLdQlmtNVAkmiB9Qw3J.jpg",
      "backdrop_path":"/2hC8HHRUvwRljYKIcQDMyMbLlxz.jpg"
   },
   "budget":94000000,
   "genres":[
      {
         "id":16,
         "name":"Animation"
      },
      {
         "id":10751,
         "name":"Family"
      }
   ],
   "homepage":"http://movies.disney.com/finding-nemo",
   "id":12,
   "imdb_id":"tt0266543",
   "original_language":"en",
   "original_title":"Finding Nemo",
   "overview":"Nemo, an adventurous young clownfish, is unexpectedly taken from his Great Barrier Reef home to a dentist's office aquarium. It's up to his worrisome father Marlin and a friendly but forgetful fish Dory to bring Nemo home -- meeting vegetarian sharks, surfer dude turtles, hypnotic jellyfish, hungry seagulls, and more along the way.",
   "popularity":144.729,
   "poster_path":"/eHuGQ10FUzK1mdOY69wF5pGgEf5.jpg",
   "production_companies":[
      {
         "id":3,
         "logo_path":"/1TjvGVDMYsj6JBxOAkUHpPEwLf7.png",
         "name":"Pixar",
         "origin_country":"US"
      }
   ],
   "production_countries":[
      {
         "iso_3166_1":"US",
         "name":"United States of America"
      }
   ],
   "release_date":"2003-05-30",
   "revenue":940335536,
   "runtime":100,
   "spoken_languages":[
      {
         "english_name":"English",
         "iso_639_1":"en",
         "name":"English"
      }
   ],
   "status":"Released",
   "tagline":"There are 3.7 trillion fish in the ocean. They're looking for one.",
   "title":"Finding Nemo",
   "video":false,
   "vote_average":7.826,
   "vote_count":16963
}
'''