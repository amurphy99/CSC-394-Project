from flask import Flask, render_template, g, request, flash
from flaskr.db import get_db
from flaskr.movieDBapi import api_home
from flaskr.movieDBapi import api_query
from flaskr.movieDBapi import home_search
# from flaskr.movieDBapi import home_genres



#@app.route('/', methods=('GET', 'POST'))
def home_page():
    '''
        later on will be using g.user to display friends list
        when g.user is None, load something else in that area
    '''
    # Poster url 
    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w500"


    # api call to get trending movies
    if request.method == "POST":
        trending = home_search()["results"][:9]
        
    else:
        trending = api_home()["results"][:9]


    #select genre
   #  genre_list = home_genres()
   #  print(genre_list)
        
    # prepare movie data for display
    movieDisplay = []
    for movie in trending:
        temp = {    "title"     : movie["title"],
                    "poster"    : BASE_URL + POSTER_SIZE + movie["poster_path"],
                    "id"        : movie["id"] }

        movieDisplay.append(temp)

    # prepare movie data dor display IF SEARCHED
    

    # prepare friends list for display [id, username]
    user_friends = [    ["admin",   1], 
                        ["Andrew",  2],
                        ["Calvin",  3],
                        ["Joseph",  4],
                        ["Brenden", 5],
                        ["Derrick", 6],
                        ["Benas",   7]  ]


    # print(movieDisplay)

    
    # display page
    return render_template('home_page/home_page.html', movieDisplay=movieDisplay, user_friends=user_friends)
    



#/home_page/home_page_search
def home_filter_tags():
    if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

    tags = request.form.getlist("myCheckbox")
   #  print(tags)
    
    test = "Searching for "
    for tag in tags:
        test += str(tag) + ", "

    genres = [
      {
         "id":28,
         "name":"Action"
      },
      {
         "id":12,
         "name":"Adventure"
      },
      {
         "id":16,
         "name":"Animation"
      },
      {
         "id":35,
         "name":"Comedy"
      },
      {
         "id":80,
         "name":"Crime"
      },
      {
         "id":99,
         "name":"Documentary"
      },
      {
         "id":18,
         "name":"Drama"
      },
      {
         "id":10751,
         "name":"Family"
      },
      {
         "id":14,
         "name":"Fantasy"
      },
      {
         "id":36,
         "name":"History"
      },
      {
         "id":27,
         "name":"Horror"
      },
      {
         "id":10402,
         "name":"Music"
      },
      {
         "id":9648,
         "name":"Mystery"
      },
      {
         "id":10749,
         "name":"Romance"
      },
      {
         "id":878,
         "name":"Science Fiction"
      },
      {
         "id":10770,
         "name":"TV Movie"
      },
      {
         "id":53,
         "name":"Thriller"
      },
      {
         "id":10752,
         "name":"War"
      },
      {
         "id":37,
         "name":"Western"
      }
   ]

    genre_ids = []
    for e in genres:
      genre_ids.append(e['id'])

    list_genres = [str(x) for x in genre_ids]

    selected_genre = []
    for e in tags:
      if e in list_genres:
         selected_genre.append(e)

    api_key = "api_key=f059b4ab8738e8777362529e74ffb62a"
    api_url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&' + api_key
    x = ",".join(selected_genre)

    genre_key = api_url + '&with_genres=' + x


   # print(genre_ids)
   # print(int_tags)
   #  print(genres)
   #  print('---------')
    print(genre_key)

    # selected_genre = endpoint key

    return render_template("home_page/filter_tags_htmx.html", tags=tags, placeholder=test, selected_genre = selected_genre)


def new_trending_list():

   BASE_URL    = "http://image.tmdb.org/t/p/"
   POSTER_SIZE = "w500"

   if request.method != 'POST': return "<h1> non-POST request to 'get_move_cards()' </h1>"

   tags = request.form.getlist("genre-tag")
   query = request.form["searched"]

   if query != None or len(query) > 1:
      results1 = api_query(query)
      print(results1)
      results = results1["result"]
      matches = []
      for movie in results:
         match = True
         for id in tags:
            if int(id) not in movie['genre_ids']:
               match = False
         if match:
            matches.append(movie)
   else:
      results = api_home()["result"]
      matches = []
      for movie in results:
         match = True
         for id in tags:
            if int(id) not in movie['genre_ids']:
               match = False
         if match:
            matches.append(movie)


   # matches = []
   # for movie in results:
   #    match = True
   #    for id in tags:
   #       if int(id) not in movie['genre_ids']:
   #          match = False
   #    if match:
   #       matches.append(movie)



   movieDisplay = []
   for movie in matches:
      temp = {    "title"     : movie["title"],
                  "poster"    : BASE_URL + POSTER_SIZE + movie["poster_path"],
                  "id"        : movie["id"] }

      movieDisplay.append(temp)
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

   return render_template('home_page/new_trending_list_htmx.html')



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



