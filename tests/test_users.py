
from jose   import jwt
from pytest import mark

from app    import schemas
from app.config     import settings_test

# app.dependency_overrides[get_db] = get_db_test      #override annotation for test
# client = TestClient(app)      # replaced by using pytest.fixture

# @fixture
# def sesison():
#     pass

# @fixture
# def client(session):            # session > client
#     # return TestClient(app)
#     yield TestClient(app)       # yield를 기준으로 테스트 실행 전/후에 필요한 동작을 정의할 수 있다. 


def test_create(client):
    res = client.post('/users/signup/',
                      json={'email':'user01@test.com', 'password':'teststring'})
    print('=========',res.json())

    # new_user = schemas.UserInfo(**res.json())     # pydantic을 활용해 유효성 검사 가능. 그러나 response_model 설정에 따라 불가능 할 수 있슴.
    # assert new_user.email == 'user01@test.com'
    assert res.json().get('email') == 'user01@test.com'


def test_login(client, test_user):     # test_user에서 client를 이미 사용하지만, client를 직접 사용하기위해 가져와야함.
    res = client.post('/login/',
                    #   data = {'username':'user19@test.com',
                    #           'password':'teststring'})
                      data = {'username':test_user['email'],
                              'password':test_user['password']})    # check data format(json, form-data, ...)
    
    res_token =  schemas.Token(**res.json())        # token validation.
    payload=jwt.decode(token=res_token.access_token,
                    key=settings_test.secrete_key,
                    algorithms = settings_test.algorithm)
    id = payload.get('user_id')
    
    assert id == test_user['id']
    assert res_token.token_type == 'bearer'
    assert res.status_code == 200

@mark.parametrize('email, password, status_code', 
                  [('wrong1@mail.com', 'wrongpwd', 403),
                   ('user24@mail.com', 'wrongpwd', 403),
                   (None, 'wrongpwd', 422),
                   ('wrong3@mail.com', None, 422)])
def test_login_fail(client, test_user, email, password, status_code):
    res = client.post('/login/',
                        # data = {'username':test_user['email'],        # single test using test_user fixture.
                        #         'password':"incorrect password"})
                        data = {'username':email,       # mutiple tests using Parameterize.
                                'password':password})
    
    # assert res.status_code == 403
    # assert res.json().get('detail') == 'Invalid Credentials'
    assert res.status_code == status_code
