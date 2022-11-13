from flask import Flask, render_template, g, request, flash
from flaskr.db import get_db
from flaskr.movieDBapi import trending_movies, popular_movies, api_query, filtered_search



#@app.route('/', methods=('GET', 'POST'))
def home_page():
    '''
        later on will be using g.user to display friends list
        when g.user is None, load something else in that area
    '''
    # Poster url 
    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w500"

    trending = trending_movies()["results"][:9]

    # prepare movie data for display
    movieDisplay = []
    for movie in trending:
        temp = {    "title"     : movie["title"],
                    "poster"    : BASE_URL + POSTER_SIZE + movie["poster_path"],
                    "id"        : movie["id"] }
        movieDisplay.append(temp)

    # prepare friends list for display [id, username]
    user_friends = [    ["admin",   1], 
                        ["Andrew",  2],
                        ["Calvin",  3],
                        ["Joseph",  4],
                        ["Brenden", 5],
                        ["Derrick", 6],
                        ["Benas",   7]  ]

    # display page
    return render_template('home_page/home_page.html', movieDisplay=movieDisplay, user_friends=user_friends)
    



#/home_page/home_page_search
def home_filter_tags():
    if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

    tags = request.form.getlist("myCheckbox")

    test = "Searching for "
    for tag in tags:
        test += str(tag) + ", "

    return render_template("home_page/filter_tags_htmx.html", tags=tags, placeholder=test)




def new_trending_list():
    if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

    # constants:
    # -----------
    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w500"


    # user inputs:
    # -------------
    tags    = request.form.getlist("genre-tag")
    method  = int(request.form["sort-by"])
    query   = request.form["searched"]

    # get results:
    # -------------
    results = filtered_search(tags, method, query, num_results=9)
    matches = results["matches"]

    keys = list(results.keys())
    for key in keys[1:]:
        print(f"{key} : {results[key]}")


    # prepare movies for display
    # ---------------------------
    movieDisplay = []
    for movie in matches:
        temp = {    "title"     : movie["title"],
                    "poster"    : BASE_URL + POSTER_SIZE + movie["poster_path"],
                    "id"        : movie["id"] }
        movieDisplay.append(temp)

    # return
    return render_template('home_page/new_trending_list_htmx.html', movieDisplay = movieDisplay)













   # genre_ids = []
   # for e in genres:
   #    genre_ids.append(e['id'])

   # list_genres = [str(x) for x in genre_ids]

   # selected_genre = []
   # for e in tags:
   #    if e in list_genres:
   #       selected_genre.append(e)

   # api_key = "api_key=f059b4ab8738e8777362529e74ffb62a"
   # api_url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&' + api_key
   # x = ",".join(selected_genre)

   # genre_key = api_url + '&with_genres=' + x



















'''      
sample api output:
-------------------
    "adult":false,
    "backdrop_path":"/mqsPyyeDCBAghXyjbw4TfEYwljw.jpg",
    "id":49046,
    "title":"All Quiet on the Western Front",
    "original_language":"de",
    "original_title":"Im Westen nichts Neues",
    "overview":"Paul Baumer and his friends Albert and Muller, egged on by romantic dreams of heroism, voluntarily enlist in the German army. Full of excitement and patriotic fervour, the boys enthusiastically march into a war they believe in. But once on the Western Front, they discover the soul-destroying horror of World War I.",
    "poster_path":"/glZfjVEzZCJ7oTHWa3m6KefcoRN.jpg",
    "media_type":"movie",
    "genre_ids":[ 28, 18, 36, 10752 ],
    "popularity":160.416,
    "release_date":"2022-10-07",
    "video":false,
    "vote_average":8.145,
    "vote_count":190


sample search output:
    {
   "page":1,
   "results":[
      {
         "adult":false,
         "backdrop_path":"/2I90eTdWu1yQPXtvuMxGW4kgswP.jpg",
         "genre_ids":[
            16,
            10749,
            878
         ],
         "id":604605,
         "original_language":"ja",
         "original_title":"HELLO WORLD",
         "overview":"Year 2027, The city of Kyoto has undergone tremendous advancement. Within the city lives Naomi Katagaki, an introvert and Ruri Ichigyō, a girl with a cold personality. Both share a love for reading books. Despite having similar interests, Naomi is afraid to approach Ruri due to her unfriendly nature.  One day, as Naomi goes out for a walk, a crimson aurora pierces through the sky for a brief moment. Shortly after, he sees a three-legged crow and a mysterious man who reveals himself to be Naomi from 10 years in the future, explaining that he has come to change a tragic event that happens to Ruri shortly after they start dating. Naomi follows his future self's instructions and starts getting closer to Ruri, determined to save her.  With the help of his future self, Naomi begins his preparations to save Ruri. Will he be able to change the future?",
         "popularity":36.619,
         "poster_path":"/r6BWky420eJQ0KbtUTlY06ZzFwU.jpg",
         "release_date":"2019-09-20",
         "title":"Hello World",
         "video":false,
         "vote_average":7.3,
         "vote_count":242
      },
      {
         "adult":false,
         "backdrop_path":"/8vn4eis4xk6cnOnAuAcyzPbqVb0.jpg",
         "genre_ids":[
            10749,
            18
         ],
         "id":745376,
         "original_language":"en",
         "original_title":"Hello, Goodbye, and Everything in Between",
         "overview":"Clare and Aidan, who after making a pact that they would break up before college, find themselves retracing the steps of their relationship on their last evening as a couple. The epic date leads them to familiar landmarks, unexpected places, and causes them to question whether high school love is meant to last.",
         "popularity":45.353,
         "poster_path":"/xyGsnp4Ld5PmJYYWnfuYYoENhHt.jpg",
         "release_date":"2022-07-06",
         "title":"Hello, Goodbye, and Everything in Between",
         "video":false,
         "vote_average":6.3,
         "vote_count":139
      },
'''



