from flask import Flask, render_template, g, request, flash
from flaskr.db import get_db
from flaskr.movieDBapi import api_home
from flaskr.movieDBapi import api_movie_page
from flaskr.movieDBapi import api_query
from flaskr.movieDBapi import api_movie_cast



#@app.route('/home_page/<userID>', methods=('GET', 'POST'))
def movie_page(movieID):
    
    # Poster url 
    BASE_URL    = "http://image.tmdb.org/t/p/"
    POSTER_SIZE = "w500"


    # Backdrop url
    BACKDROP_SIZE = "w500"

    # api call to get trending movies
    result_movie = api_movie_page(movieID)
    result_cast = api_movie_cast(movieID)["cast"][:6]

    # print(result_cast)

    poster_movie = BASE_URL + POSTER_SIZE + result_movie['poster_path']
    backdrop_movie = BASE_URL + BACKDROP_SIZE + result_movie['backdrop_path']
    
    #  Create genre list
    genre_list = []
    for key in result_movie['genres']:
        genre_list.append(key['name'])
    # Turn list into string to print in template
    genre_string = ', '.join(genre_list)



    #conditional if there is no budget provided
    if result_movie['budget'] == 0:
        newBudget = '-'
    else:
        newBudget = result_movie['budget']



    #conditional if there is no revenue provided
    if result_movie['revenue'] == 0:
        newRevenue = '-'
    else:
        newRevenue = result_movie['revenue']


    movieCast = []
    for cast in result_cast:
        movieCast.append(cast['name'])
        movieCast.append(cast['profile_path'])
    
    movieCharacter = []
    for cast in result_cast:
        movieCharacter.append(cast['character'])
    
    # print(movieCharacter)

    character1 = movieCharacter[0]
    character2 = movieCharacter[1]
    character3 = movieCharacter[2]
    character4 = movieCharacter[3]
    character5 = movieCharacter[4]
    character6 = movieCharacter[5]
        
    print(character1)

    cast_profile_1 = BASE_URL + POSTER_SIZE + movieCast[1]
    cast_profile_2 = BASE_URL + POSTER_SIZE + movieCast[3]
    cast_profile_3 = BASE_URL + POSTER_SIZE + movieCast[5]
    cast_profile_4 = BASE_URL + POSTER_SIZE + movieCast[7]
    cast_profile_5 = BASE_URL + POSTER_SIZE + movieCast[9]
    cast_profile_6 = BASE_URL + POSTER_SIZE + movieCast[11]
    

    # prepare movie data for display
    movieDisplay = [] 
    movieDisplay.append(result_movie['title'])
    movieDisplay.append(poster_movie)
    movieDisplay.append(result_movie['overview'])
    movieDisplay.append(result_movie['release_date'])
    movieDisplay.append(result_movie['runtime'])
    movieDisplay.append(genre_string)
    movieDisplay.append(result_movie['tagline'])
    movieDisplay.append(result_movie['status'])
    movieDisplay.append(newBudget)
    movieDisplay.append(newRevenue)
    movieDisplay.append(result_movie['original_language'])
    movieDisplay.append(backdrop_movie)
    movieDisplay.append(movieCast)
    movieDisplay.append(cast_profile_1)
    movieDisplay.append(cast_profile_2)
    movieDisplay.append(cast_profile_3)
    movieDisplay.append(cast_profile_4)
    movieDisplay.append(cast_profile_5)
    movieDisplay.append(cast_profile_6)
    movieDisplay.append(character1)
    movieDisplay.append(character2)
    movieDisplay.append(character3)
    movieDisplay.append(character4)
    movieDisplay.append(character5)
    movieDisplay.append(character6)


    # print(movieDisplay[12])


    #for testing    
    # print(result_movie['budget'])
    '''
    movieDisplay[0] = title
    movieDisplay[1] = poster
    movieDisplay[2] = overview
    movieDisplay[3] = release date
    movieDisplay[4] = runtime
    movieDisplay[5] = genres (creates a list of genres)
    movieDisplay[6] = tagline
    movieDisplay[7] = status
    movieDisplay[8] = budget
    movieDisplay[9] = revenue
    movieDisplay[10] = original language
    movieDisplay[11] = backdrop
    movieDisplay[12] = cast
    movieDisplay[13] = cast_profile_1
    movieDisplay[14] = cast_profile_2
    movieDisplay[15] = cast_profile_3
    movieDisplay[16] = cast_profile_4
    movieDisplay[17] = cast_profile_5
    movieDisplay[18] = cast_profile_6
    movieDisplay[19] = character1
    movieDisplay[20] = character2
    movieDisplay[21] = character3
    movieDisplay[22] = character4
    movieDisplay[23] = character5
    movieDisplay[24] = character6
    
    '''
    # print(result_movie['genres'][0]['name'])

    # display page
    return render_template('home_page/movie_page.html', movieID = movieID, movieDisplay = movieDisplay)



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


 --------credits----------
  CAST

"id":505642,
   "cast":[
      {
         "adult":false,
         "gender":1,
         "id":1083010,
         "known_for_department":"Acting",
         "name":"Letitia Wright",
         "original_name":"Letitia Wright",
         "popularity":94.957,
         "profile_path":"/i6fbYNn5jWA6swWtaqgzaj02RMc.jpg",
         "cast_id":4,
         "character":"Shuri",
         "credit_id":"5a95b93292514154f7004c22",
         "order":0
      },
      {
         "adult":false,
         "gender":1,
         "id":1267329,
         "known_for_department":"Acting",
         "name":"Lupita Nyong'o",
         "original_name":"Lupita Nyong'o",
         "popularity":20.105,
         "profile_path":"/mJMpsADPpt0bmXEzs3ywrUiCkpD.jpg",
         "cast_id":3,
         "character":"Nakia",
         "credit_id":"5a95b9070e0a262f07004ee6",
         "order":1
      },
      {
         "adult":false,
         "gender":1,
         "id":82104,
         "known_for_department":"Acting",
         "name":"Danai Gurira",
         "original_name":"Danai Gurira",
         "popularity":20.792,
         "profile_path":"/bCjz32aVpyufnPjzLPOtV5DEXKK.jpg",
         "cast_id":5,
         "character":"Okoye",
         "credit_id":"5b7f0ffc92514104e901b8e6",
         "order":2
      },
      {
         "adult":false,
         "gender":2,
         "id":1447932,
         "known_for_department":"Acting",
         "name":"Winston Duke",
         "original_name":"Winston Duke",
         "popularity":18.751,
         "profile_path":"/MhBiZbryibwuoEtPL9Ns8pYHC1.jpg",
         "cast_id":6,
         "character":"M'Baku",
         "credit_id":"5b7f103bc3a368341a01e88a",
         "order":3
      },
      {
         "adult":false,
         "gender":1,
         "id":2133996,
         "known_for_department":"Acting",
         "name":"Dominique Thorne",
         "original_name":"Dominique Thorne",
         "popularity":34.808,
         "profile_path":"/tuLlp79SfYc4mLzzjdC2ekLI7qd.jpg",
         "cast_id":35,
         "character":"Riri Williams / Ironheart",
         "credit_id":"611eb56ccca7de005b2e8269",
         "order":4
      },
      {
         "adult":false,
         "gender":2,
         "id":87265,
         "known_for_department":"Acting",
         "name":"Tenoch Huerta",
         "original_name":"Tenoch Huerta",
         "popularity":52.121,
         "profile_path":"/gkGEBRqwDvaBiBWbNYRh942kHfG.jpg",
         "cast_id":32,
         "character":"Namor",
         "credit_id":"60e4e46c8805510074e1eec3",
         "order":5
      },
      {
         "adult":false,
         "gender":1,
         "id":9780,
         "known_for_department":"Acting",
         "name":"Angela Bassett",
         "original_name":"Angela Bassett",
         "popularity":69.601,
         "profile_path":"/7Oz53NKdglRzAzI2MKjM3eQXwn.jpg",
         "cast_id":7,
         "character":"Ramonda",
         "credit_id":"5b7f10a892514104e601cf8d",
         "order":6
      },
      {
         "adult":false,
         "gender":1,
         "id":139900,
         "known_for_department":"Acting",
         "name":"Florence Kasumba",
         "original_name":"Florence Kasumba",
         "popularity":8.729,
         "profile_path":"/vivJLQhtwca5hupqoRRgL8BRs6o.jpg",
         "cast_id":40,
         "character":"Ayo",
         "credit_id":"618df4035f2b8d002663b94d",
         "order":7
      },
      {
         "adult":false,
         "gender":1,
         "id":1368012,
         "known_for_department":"Acting",
         "name":"Michaela Coel",
         "original_name":"Michaela Coel",
         "popularity":8.538,
         "profile_path":"/rbN1F0R8DMUh6IYwl0owyD8LukN.jpg",
         "cast_id":34,
         "character":"Aneka",
         "credit_id":"60f8948d39a1a60030b45966",
         "order":8
      },
      {
         "adult":false,
         "gender":1,
         "id":2213811,
         "known_for_department":"Acting",
         "name":"Mabel Cadena",
         "original_name":"Mabel Cadena",
         "popularity":35.462,
         "profile_path":"/i7JL6cnvaLywKXN5rMCODztYKT4.jpg",
         "cast_id":55,
         "character":"Namora",
         "credit_id":"629cf5d99661fc00aadd3121",
         "order":9
      },

      CREW

"crew":[
      {
         "adult":false,
         "gender":1,
         "id":7232,
         "known_for_department":"Production",
         "name":"Sarah Halley Finn",
         "original_name":"Sarah Halley Finn",
         "popularity":10.99,
         "profile_path":"/pI3OhmnHhXLEwuv0Vq6qJHivCJA.jpg",
         "credit_id":"60326570befb09003e8ff17d",
         "department":"Production",
         "job":"Casting"
      },
      {
         "adult":false,
         "gender":0,
         "id":7537,
         "known_for_department":"Sound",
         "name":"Steve Boeddeker",
         "original_name":"Steve Boeddeker",
         "popularity":1.4,
         "profile_path":"None",
         "credit_id":"636d10fdf14dad007b25f993",
         "department":"Sound",
         "job":"Supervising Sound Editor"
      },
      {
         "adult":false,
         "gender":0,
         "id":7537,
         "known_for_department":"Sound",
         "name":"Steve Boeddeker",
         "original_name":"Steve Boeddeker",
         "popularity":1.4,
         "profile_path":"None",
         "credit_id":"636d110421621b009111a36c",
         "department":"Sound",
         "job":"Sound Re-Recording Mixer"
      },
      {
         "adult":false,
         "gender":2,
         "id":7624,
         "known_for_department":"Writing",
         "name":"Stan Lee",
         "original_name":"Stan Lee",
         "popularity":17.858,
         "profile_path":"/kKeyWoFtTqOPsbmwylNHmuB3En9.jpg",
         "credit_id":"637042af8138310080854e83",
         "department":"Writing",
         "job":"Characters"
      },
      {
         "adult":false,
         "gender":2,
         "id":10850,
         "known_for_department":"Production",
         "name":"Kevin Feige",
         "original_name":"Kevin Feige",
         "popularity":16.337,
         "profile_path":"/kCBqXZ5PT5udYGEj2wfTSFbLMvT.jpg",
         "credit_id":"5a8784259251417599044b4d",
         "department":"Production",
         "job":"Producer"
      },
      {
         "adult":false,
         "gender":0,
         "id":10122,
         "known_for_department":"Production",
         "name":"Barry H. Waldman",
         "original_name":"Barry H. Waldman",
         "popularity":1.96,
         "profile_path":"None",
         "credit_id":"62ddc6765ca7040b29905b1f",
         "department":"Production",
         "job":"Executive Producer"
      },
      {
         "adult":false,
         "gender":0,
         "id":13306,
         "known_for_department":"Costume & Make-Up",
         "name":"Richard Alonzo",
         "original_name":"Richard Alonzo",
         "popularity":1.615,
         "profile_path":"None",
         "credit_id":"636d0f04d7fbda0088752826",
         "department":"Costume & Make-Up",
         "job":"Makeup Artist"
      },
      {
         "adult":false,
         "gender":1,
         "id":15524,
         "known_for_department":"Costume & Make-Up",
         "name":"Ruth E. Carter",
         "original_name":"Ruth E. Carter",
         "popularity":3.94,
         "profile_path":"/b1CtSVekrYuEmCYt9K3JxWfcJjt.jpg",
         "credit_id":"6333a27541eee10086e6d518",
         "department":"Costume & Make-Up",
         "job":"Costume Design"
      },
      {
         "adult":false,
         "gender":2,
         "id":18866,
         "known_for_department":"Writing",
         "name":"Jack Kirby",
         "original_name":"Jack Kirby",
         "popularity":5.902,
         "profile_path":"/ihhR019gL1WrXdSQNJITAY6dont.jpg",
         "credit_id":"637042b9172d7f007a5ce50a",
         "department":"Writing",
         "job":"Characters"
      },
      {
         "adult":false,
         "gender":2,
         "id":24192,
         "known_for_department":"Sound",
         "name":"Dave Jordan",
         "original_name":"Dave Jordan",
         "popularity":1.4,
         "profile_path":"None",
         "credit_id":"6333a247076ce80084c27ab3",
         "department":"Sound",
         "job":"Music Supervisor"
      },
      {
         "adult":false,
         "gender":2,
         "id":57027,
         "known_for_department":"Production",
         "name":"Louis D'Esposito",
         "original_name":"Louis D'Esposito",
         "popularity":20.371,
         "profile_path":"/k9k3WWYdD3uDnrtwM60QirzG9cH.jpg",
         "credit_id":"6137e4a2e93e950065ed68e5",
         "department":"Production",
         "job":"Executive Producer"
      },
      {
         "adult":false,
         "gender":1,
         "id":113674,
         "known_for_department":"Production",
         "name":"Victoria Alonso",
         "original_name":"Victoria Alonso",
         "popularity":6.149,
         "profile_path":"/xF7Qe1tqgk9KtY8kThKHBWhMqxc.jpg",
         "credit_id":"6137e4842cde98002b6c4052",
         "department":"Production",
         "job":"Executive Producer"
      },

'''