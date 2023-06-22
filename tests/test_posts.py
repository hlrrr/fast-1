def test_get_my_posts(client_authorized):
    res = client_authorized.get('/posts/')
    print('===============', res.json())

    assert res.status_code == 200  

def test_create_posts():
    pass    