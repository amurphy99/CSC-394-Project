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
    

