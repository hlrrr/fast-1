
from fastapi.testclient     import TestClient
from pytest     import fixture
from app.main   import app
from app    import schemas
from app.database   import get_db, Base


# app.dependency_overrides[get_db] = get_db_test      #override annotation for test
# client = TestClient(app)      # replaced by using pytest.fixture

# @fixture
# def sesison():
#     pass

# @fixture
# def client(session):            # session > client
#     # return TestClient(app)
#     yield TestClient(app)       # yield를 기준으로 테스트 실행 전/후에 필요한 동작을 정의할 수 있다. 



""" trailing slash 관련
*without* trailing slash: api 호출 시, redirection(307)이 발생하여 status_code(201, 등)로 판별 실패.
따라서 테스트 url 작성 시, trailing slash 붙일것.    
"""



def test_create(client):
    res = client.post('/users/signup',
                      json={'email':'user18@test.com', 'password':'teststring'})
    print('=========',res.json())
    assert res.json().get('email') == 'user18@test.com'


def test_login_user(client):
    res = client.post('/login',
                      data = {'username':'user18@test.com','password':'teststring'})    # check data format(json, form-data, ...)
    assert res.status_code == 200


