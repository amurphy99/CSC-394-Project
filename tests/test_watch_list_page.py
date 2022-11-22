import pytest
from flaskr.db import get_db


def test_watch_list(client, auth):
    response = client.get('/watch_list/1')
    assert b"Log In" in response.data
    assert b"Register" in response.data
    assert b'Add Movie' not in response.data

    auth.login()
    response = client.get('watch_list/1')
    assert b'Log Out' in response.data
    assert b'Add Movie' in response.data


def test_watch_list_add_movies(client, auth):
    auth.login()
    response = client.post('/watch_list/modal', data={'listID': '1'})
    assert b'Enter movie query' in response.data
    
    response = client.post('/watch_list/get_movie_cards', data={'listID': '1', 'api_query': 'spongebob'})
    assert b'Results:' in response.data
    
    response = client.post('/watch_list/movie_added_htmx', data={   'movie_info'    : '{"info":[0, [0, 11836]] }',
                                                                    'listID'        : '1', 
                                                                    'userID'        : '1',
                                                                    'watch-status'  : '2',
                                                                    'rating'        : '5'   })
    assert b'Status:' in response.data




'''

    app.add_url_rule('/watch_list/<listID>',                methods=('GET', 'POST'), view_func=watch_list.watch_list)
    app.add_url_rule('/watch_list/modal',                   methods=('GET', 'POST'), view_func=watch_list.add_movie_modal)
    app.add_url_rule('/watch_list/get_movie_cards',         methods=('GET', 'POST'), view_func=watch_list.get_movie_cards)
    app.add_url_rule('/watch_list/movie_added_htmx',        methods=('GET', 'POST'), view_func=watch_list.movie_added2)



    app.add_url_rule('/watch_list/show_user_input_form',    methods=('GET', 'POST'), view_func=watch_list.show_user_input_form)
    
'''