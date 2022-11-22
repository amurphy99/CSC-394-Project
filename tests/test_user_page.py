import pytest
from flaskr.db import get_db


def test_user(client, auth):
    response = client.get('/user/1')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    # buttons don't appear while not logged in
    assert b'Create New Watch List' not in response.data
    assert b'Edit Bio' not in response.data

    


    # after logging in
    # ------------------
    auth.login()
    response = client.get('/user/1')
    assert b'Log Out' in response.data

    # buttons appear once logged in
    assert b'Create New Watch List' in response.data
    assert b'Edit Bio' in response.data

    # test edit bio
    response = client.post('/user/modal_form_edit_bio', data={'current_bio': 'example current bio'})
    assert b'Edit Bio' in response.data
    assert b'example current bio' in response.data

    response = client.post('/user/modal_form_edit_bio_receive', data={'new_bio': 'example NEW bio'})
    assert b'New Bio:' in response.data
    assert b'example NEW bio' in response.data

    response = client.get('/user/1')
    assert b'example NEW bio' in response.data



def test_user_page_friends_button(client, auth):
    response = client.get('/user/2')
    assert b'Add Friend' not in response.data

    auth.login()
    response = client.get('/user/2')
    assert b'Add Friend' in response.data

    response = client.post('/user/friend_request_button', data={'relationship': '0', 'user1': '1', 'user2': '2'})
    assert b'<input type="hidden" name="relationship"    value="2">' in response.data
    assert b'Friend Request Sent' in response.data



def test_user_page_accept_remove_friends(client, auth):
    response = client.post('/user/friend_request_button', data={'relationship': '0', 'user1': '2', 'user2': '1'})
    assert b'<input type="hidden" name="relationship"    value="2">' in response.data
    assert b'Friend Request Sent' in response.data

    auth.login()
    response = client.get('/user/2')
    assert b'Accept Incoming Friend Request' in response.data

    response = client.post('/user/friend_request_button', data={'relationship': '3', 'user1': '1', 'user2': '2'})
    assert b'Remove Friend' in response.data

    response = client.post('/user/friend_request_button', data={'relationship': '1', 'user1': '1', 'user2': '2'})
    assert b'Add Friend' in response.data



'''
        <input type="hidden" name="relationship"    value="{ relationship }">
        <input type="hidden" name="user1"           value="{ user1 }">
        <input type="hidden" name="user2"           value="{ user2 }">

    app.add_url_rule('/user/friend_request_button',         methods=['POST'], view_func=user_page.friend_request_button)

    app.add_url_rule('/user/modal_form_edit_bio',           methods=['POST'], view_func=user_page.modal_form_edit_bio)
    app.add_url_rule('/user/modal_form_edit_bio_receive',   methods=['POST'], view_func=user_page.modal_form_edit_bio_receive)

    client.post('/create', data={'title': 'created', 'body': ''})

'''
