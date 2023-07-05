from pprint     import pprint
from pytest import mark

from app    import schemas

''' RETRIEVE related
notes
'''
def test_get_all_posts(client_authorized, test_posts):
    res = client_authorized.get('/posts/')
    # pprint(res.json())
    assert res.status_code == 200  

    # def validate(post):       
    #     return schemas.PostInfo(**post)    # schema를 활용한 유효성 검사.

    # posts_mapped = map(validate, res.json())
    # posts_list = list(posts_mapped)

    # assert posts_list[0].id == test_posts[0].id   # 데이터 순서 문제 해결 필요.  

def test_get_all_posts_unauthorized(client, test_posts):  
    res = client.get('/posts/')
    assert res.status_code == 401


def test_get_one_post_unauthorized(client, test_posts):  
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401 


def test_get_one_post_not_exist(client_authorized, test_posts):  
    res = client_authorized.get('/posts/99999999')
    assert res.status_code == 404


def test_get_one_post(client_authorized, test_posts):  
    res = client_authorized.get(f'/posts/{test_posts[0].id}')
    post =  schemas.PostLikey(**res.json())
    pprint(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

''' CREATE related tests
notes
'''
@mark.parametrize("title, content, published,",
                  [('some title','some content',True),
                   ('other title','other content',False),
                   ('another title','another content',True)])
def test_create_post(client_authorized, test_user, title, content, published):
    res = client_authorized.post('/posts/',
                                 json={'title':title,
                                       'content':content,
                                       'published':published})
    post_created = schemas.PostInfo(**res.json())
    
    assert res.status_code == 201
    assert post_created.title == title
    assert post_created.content == content
    assert post_created.published == published
    assert post_created.owner_id == test_user['id']


def test_create_post_default_published(client_authorized, test_user, test_posts):
    res = client_authorized.post('/posts/',
                                 json={'title':'some title',
                                       'content':'some content'})
    post_created = schemas.PostInfo(**res.json())
    
    assert res.status_code == 201
    assert post_created.title == 'some title'
    assert post_created.content == 'some content'
    assert post_created.published == True
    assert post_created.owner_id == test_user['id']


def test_create_post_unauthorized(client, test_user, test_posts):  
    res = client.post('/posts/',
                     json={'title':'some title',
                           'content':'some content'})
    assert res.status_code == 401

''' DELETE ralated
notes
'''
def test_delete_post_unauthorized(client, test_posts):  
    res = client.delete(f'/posts/{test_posts[0].id}')
    
    assert res.status_code == 401


def test_delete_post(client_authorized, test_posts):  
    res = client_authorized.delete(f'/posts/{test_posts[0].id}')
    
    assert res.status_code == 204


def test_delete_post_not_exist(client_authorized):  
    res = client_authorized.delete('/posts/99999999')
    
    assert res.status_code == 404


def test_delete_post_not_mine(client_authorized, test_posts):  
    res = client_authorized.delete(f'/posts/{test_posts[2].id}')
    
    assert res.status_code == 403

''' UPDATE related
notes
'''
def test_update_post(client_authorized, test_posts):
    data = {'title':'updated title',
            'content':'updated content'}
    res = client_authorized.put(f'/posts/{test_posts[0].id}',
                                json=data)
    post_updated = schemas.PostBase(**res.json())

    assert res.status_code == 200
    assert post_updated.title == data['title'] 
    assert post_updated.content == data['content'] 


def test_update_post_unauthorized(client, test_posts):
    data = {'title':'updated title',
            'content':'updated content'}
    res = client.put(f'/posts/{test_posts[0].id}',
                                json=data)

    assert res.status_code == 401


def test_update_post_not_exist(client_authorized, test_posts):
    data = {'title':'updated title',
            'content':'updated content'}
    res = client_authorized.put('/posts/999999999',
                                json=data)

    assert res.status_code == 404


def test_update_post_not_mine(client_authorized, test_posts):
    data = {'title':'updated title',
            'content':'updated content'}
    res = client_authorized.put(f'/posts/{test_posts[2].id}',
                                json=data)

    assert res.status_code == 403