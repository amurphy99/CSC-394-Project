import pytest
from flaskr.db import get_db


def test_movie_page(client, auth):
    response = client.get('/movie_page/228165')
    assert b"Log In" in response.data
    assert b"Register" in response.data
    assert b'Add Movie' not in response.data
    
    auth.login()
    response = client.get('/movie_page/228165')
    assert b'Log Out' in response.data
    assert b'Add Movie' in response.data
    

def test_movie_page_add_button(client, auth):
    auth.login()
    response = client.get('/movie_page/228165')
    assert b'Add Movie' in response.data


    response = client.post('/modal_form_add_movie', data={'movie_id': '228165'})
    assert b'Add Movie' in response.data
    assert b'Choose a list to add this movie to:' in response.data


    response = client.post('/modal_form_add_movie_receive', data={  'movie_id'      : '228165', 
                                                                    'watch-list'    : '1', 
                                                                    'watch-status'  : '2',  
                                                                    'rating'        : '5'       })
    assert b'Movie Added!' in response.data


''''


    movie_id        = int(request.form["movie_id"])
    list_id         = int(request.form["watch-list"])
    watch_status    = int(request.form["watch-status"])
    rating          = int(request.form["rating"])


'''