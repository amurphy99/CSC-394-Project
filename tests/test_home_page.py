import pytest
from flaskr.db import get_db


def test_home_page(client, auth):
    response = client.get('/')
    assert b"Log in or create an account to add friends!" in response.data
    assert b'Add Friends' not in response.data
    
    auth.login()
    response = client.get('/')
    assert b"Log in or create an account to add friends!" not in response.data
    assert b'Add Friends' in response.data



def test_home_page_filter_movies(client, auth):
    auth.login()
    response = client.post('/home_page_search', data={'myCheckbox': ['28', '12']})
    assert b'<input type="hidden" name="genre-tag"  value="28">' in response.data
    assert b'<input type="hidden" name="genre-tag"  value="12">' in response.data
    
    response = client.post('/new_trending_list', data={'genre-tag': ['28', '12'], 'sort-by': '1', 'searched': ''})
    assert response.status_code == 200

    response = client.post('/new_trending_list', data={'genre-tag': ['28', '12'], 'sort-by': '2', 'searched': ''})
    assert response.status_code == 200

    response = client.post('/new_trending_list', data={'genre-tag': ['28', '12'], 'sort-by': '0', 'searched': 'avengers'})
    assert response.status_code == 200



'''
    tags    = request.form.getlist("genre-tag")
    method  = int(request.form["sort-by"])
    query   = request.form["searched"]

from . import home_page
app.add_url_rule('/',                   methods=('GET', 'POST'), view_func=home_page.home_page)
app.add_url_rule('/home_page_search',   methods=('GET', 'POST'), view_func=home_page.home_filter_tags)
app.add_url_rule('/new_trending_list',  methods=('GET', 'POST'), view_func=home_page.new_trending_list)

'''