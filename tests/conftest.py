''' Fixtures defined in a conftest.py can be used by any test in that package without needing to import them (pytest will automatically discover them). 
https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
'''
''' fixture 활용
fixture scope를 통해 fixture 실행 빈도(?) 설정가능.
https://docs.pytest.org/en/6.2.x/fixture.html#fixture-scopes
'''

from fastapi.testclient     import TestClient
from pytest     import fixture, mark

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.config   import settings_test
from app.main   import app
from app.database   import get_db, Base
from app    import models

# app.dependency_overrides[get_db] = get_db_test      # override DB annotation 
# client = TestClient(app)  


engine_test = create_engine(
    settings_test.database_url_test,
    # connect_args={"check_same_thread": False}
)
SessionLocal_test = sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine_test)

# database session for prod
def get_db_test():
    db = SessionLocal_test()
    try:
        yield db
    finally:
        db.close()


@fixture(scope='module')
def session():
    print("session check")
    # Base.metadata.drop_all(bind=engine_test)      
    # Base.metadata.create_all(bind=engine_test)    # 테스트 수행 전 필요 한 테이블 관련 명령.   
    db = SessionLocal_test()
    try:
        yield db
    finally:
        db.close()


@fixture(scope='module')
def client(session):     
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_db_test
    yield TestClient(app)       # yield를 기준으로 테스트 실행 전/후에 필요한 동작을 정의할 수 있다.
    # return TestClient(app)



# def test_root(client, session):      # session > client > test func.
#     res = client.get('/')
#     # session.query(models.Post)      
#     # # 필요 시, session을 받아서 활용 가능.
#     print('=========',res.json().get('msg'))
#     assert res.status_code == 200
#     assert res.json().get('msg') == 'my template'


@fixture
def test_user(client):
    data = {'email':'user11@test.com',
            'password':'teststring'}
    res =client.post('/users/signup/',
                     json=data)
    
    print(res.json())
    user = res.json()
    user['password']=data['password']
    return user    
    # 해당 fixture 사용 시, test_user['email'], test_user['password'] 접근 가능