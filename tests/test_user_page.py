import pytest
from flaskr.db import get_db


def test_user(client, auth):
    response = client.get('/user/1')
    assert b"Log In" in response.data
    assert b"Register" in response.data
    assert b'Create New Watch List' not in response.data

    auth.login()
    response = client.get('/user/1')
    assert b'Log Out' in response.data
    assert b'Create New Watch List' in response.data
    
    #assert b'test title' in response.data
    #assert b'by test on 2018-01-01' in response.data
    #assert b'test\nbody' in response.data
    #assert b'href="/1/update"' in response.data
