
import requests
import json
import time

from flask import Flask, render_template, g, request, flash


'''
page only shows 5 responses for now, doesnt live search, only on button click


Configuration information for poster sizes:
https://developers.themoviedb.org/3/configuration/get-api-configuration

'''

def api_query(query):
    # build api request url
    base        = "https://api.themoviedb.org/3/search/movie?api_key="
    api_key     = "f059b4ab8738e8777362529e74ffb62a"
    lang        = "&language=en-US&query="
    optionals   = "&page=1&include_adult=false"

    endpoint = base + api_key + lang + query + optionals

    # returns a dictionary
    first_response  = requests.get(endpoint)
    response_list   = first_response.json()

    #print(f'query of "{query}" sent to the api')

    return response_list



def genre_query():

    endpoint = "https://api.themoviedb.org/3/genre/movie/list?api_key=f059b4ab8738e8777362529e74ffb62a&language=en-US"

    # returns a dictionary
    first_response  = requests.get(endpoint)
    response_list   = first_response.json()

    return response_list





#@app.route('/api_testing', methods=('GET', 'POST'))
def api_testing():

    return render_template('api_testing/api_testing.html')


#@app.route('/send_query_htmx', methods=('GET', 'POST'))
def get_results():

    if request.method == 'POST':
        query = request.form["api_query"]
        
        results = api_query(query)
        
        first_movie = results["results"][0]

        results_tuples = []
        for key in first_movie.keys():
            temp = [key, first_movie[key]]
            results_tuples.append(temp)

        return render_template('api_testing/results_table_htmx.html', results = results_tuples)


    return "<h1> this shouldnt be returned </h1>"

 




def api_home():
    # build api request url
    base        = "https://api.themoviedb.org/3/trending"
    optionals   = "/movie/day?api_key="
    api_key     = "f059b4ab8738e8777362529e74ffb62a"

    endpoint = base + optionals + api_key

    # returns a dictionary
    first_response  = requests.get(endpoint)
    response_list   = first_response.json()

    #print(response_list)

    return response_list




def trending_movies(time_window = "day", page_number = 1):
    # constant api args:
    # -------------------
    API_KEY     = "f059b4ab8738e8777362529e74ffb62a"
    LANG        = "en-US"

    # build api request url:
    # -----------------------
    base =  "https://api.themoviedb.org/3/trending/movie"
    time = f"/{time_window}?api_key={API_KEY}"
    lang = f"&language={LANG}"
    page = f"&page={page_number}"

    endpoint = base + time + lang + page

    # returns a dictionary:
    # ----------------------
    first_response  = requests.get(endpoint)
    response_list   = first_response.json()

    # return results:
    # ----------------
    return response_list



def popular_movies(page_number=1):
    # constant api args:
    # -------------------
    API_KEY = "f059b4ab8738e8777362529e74ffb62a"
    LANG    = "en-US"

    # build api request url:
    # -----------------------
    base = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}"
    lang = f"&language={LANG}"
    page = f"&page={page_number}"

    endpoint = base + lang + page

    # returns a dictionary:
    # ----------------------
    first_response  = requests.get(endpoint)
    response_list   = first_response.json()

    # return results:
    # ----------------
    return response_list



def filtered_search(tags, method, query="", num_results=9, range=None):
    # constants:
    # -----------
    MAX_SEARCH_TIME = 10

    # api_feedback:
    # --------------
    total_pages         = 1
    total_results       = -1
    pages_searched      = 0
    results_searched    = 0
    matches             = []
    start_time          = time.time()
    
    # filter movies and get the number requested:
    # --------------------------------------------
    while len(matches) < num_results and pages_searched < total_pages and (time.time()-start_time) < MAX_SEARCH_TIME:
        pages_searched += 1

        # get the results here
        # ---------------------
        if   len(query)  > 0: response = api_query(query)             
        elif method     == 0: response = trending_movies(page_number=pages_searched, time_window="day"  )
        elif method     == 1: response = trending_movies(page_number=pages_searched, time_window="week" )
        elif method     == 2: response = popular_movies (page_number=pages_searched                     )
        else: response = {"total_pages": 0, "total_results": 0, "results": []} # something went wrong

        total_pages     = response["total_pages"]
        total_results   = response["total_results"]
        results         = response["results"]

        # filter through the results
        # ---------------------------
        for movie in results:
            if len(matches) >= 9: break
            results_searched += 1

            match = True
            # release year (not implemented)
            # if movie["release_date"] not in range(start date, end date): match = False

            # genres
            for id in tags:
                if int(id) not in movie['genre_ids']: match = False

            # make sure there is a poser
            if movie["poster_path"] == None: match = False

            # if the movie made it through each check, then approve it
            if match: matches.append(movie)


    # return dict with matches and api feedback
    api_feedback = {
        "matches"           : matches,
        "total_pages"       : total_pages, 
        "total_results"     : total_results,
        "pages_searched"    : pages_searched, 
        "results_searched"  : results_searched,
        "matches_found"     : len(matches), 
        "time_taken"        : (time.time()-start_time)
    }

    return api_feedback















def api_movie_page(movieID):

    base = "https://api.themoviedb.org/3/movie/"
    api_key = "?api_key=f059b4ab8738e8777362529e74ffb62a"
    lang = "&language=en-US"

    endpoint = base + str(movieID) + api_key + lang

    first_response = requests.get(endpoint)
    response_list = first_response.json()

    return response_list


def api_movie_cast(movieID):

    base = "https://api.themoviedb.org/3/movie/"
    api_key = "?api_key=f059b4ab8738e8777362529e74ffb62a"
    lang = "&language=en-US"

    endpoint = base + str(movieID)+"/credits" + api_key + lang

    first_response = requests.get(endpoint)
    response_list = first_response.json()

    return response_list

def home_search():

    if request.method == "POST":
        
        search_term = request.form["searched"]

        base        = "https://api.themoviedb.org/3/search/movie?api_key="
        api_key     = "f059b4ab8738e8777362529e74ffb62a"
        search_url  = base + api_key

        endpoint = search_url + '&query=' + search_term

        first_response = requests.get(endpoint)
        response_list = first_response.json()

        return response_list


