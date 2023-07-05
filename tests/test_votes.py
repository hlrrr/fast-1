from pprint     import pprint
from pytest import mark, fixture

from app    import schemas, models

@fixture()
def vote_add(test_posts, session, test_user):
    vote = models.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(vote)
    session.commit()


def test_vote(client_authorized, test_posts):
    res = client_authorized.post('/vote/',
                                 json={'post_id':test_posts[2].id,
                                       'direction':1})
    assert res.status_code == 201


def test_vote_not_exist(client_authorized, test_posts):
    res = client_authorized.post('/vote/',
                                 json={'post_id':999999,
                                       'direction':1})
    assert res.status_code == 404

def test_vote_unauthorized(client, test_posts):
    res = client.post('/vote/',
                      json={'post_id':test_posts[2].id,
                            'direction':1})
    assert res.status_code == 401


def test_vote_again(client_authorized, test_posts, vote_add):
    res = client_authorized.post('/vote/',
                                 json={'post_id':test_posts[0].id,
                                       'direction':1})
    assert res.status_code == 409


def test_vote_delete(client_authorized, test_posts, vote_add):
    res = client_authorized.post('/vote/',
                                 json={'post_id':test_posts[0].id,
                                       'direction':0})
    assert res.status_code == 201


def test_vote_delete_not_exist(client_authorized, test_posts, vote_add):
    res = client_authorized.post('/vote/',
                                 json={'post_id':test_posts[2].id,
                                       'direction':0})
    assert res.status_code == 404

