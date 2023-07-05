''' Fixtures defined in a conftest.py can be used by any test in that package without needing to import them (pytest will automatically discover them). 
https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
'''

''' fixture 활용
fixture scope를 통해 fixture 실행 빈도(?) 설정가능.
https://docs.pytest.org/en/6.2.x/fixture.html#fixture-scopes
'''

''' Quests
테스트 서버 없이 테스트용 인증 로직으로 우회하는 방법은?
dataclass 내에서 base model로 맵핑하는 방법? 어떻게 사용하는게 효율적인가?
'''
from fastapi.testclient     import TestClient
from pytest     import fixture, mark
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses    import dataclass, field, asdict
from pprint     import pprint

from app.config import settings
from app.main   import app
from app.database   import get_db, Base
from app.oauth2     import token_create
from app    import models as m


# app.dependency_overrides[get_db] = get_db_test      # override DB annotation 
# client = TestClient(app)  


engine_test = create_engine(
    settings.database_url,
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

# def test_root(client, session):      # session > client > test func.
#     res = client.get('/')
#     # session.query(models.Post)      
#     # # 필요 시, session을 받아서 활용 가능.
#     print('=========',res.json().get('msg'))
#     assert res.status_code == 200
#     assert res.json().get('msg') == 'my template'


# @fixture(scope='session')
@fixture()
def session():
    print("[session check]")
    # Base.metadata.clear()
    Base.metadata.drop_all(bind=engine_test)      
    Base.metadata.create_all(bind=engine_test)    # 테스트 수행 전 필요 한 테이블 관련 명령.   
    db = SessionLocal_test()
    try:
        yield db
    finally:
        db.close()


@fixture()
def client(session):     
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_db_test
    yield TestClient(app)       # yield를 기준으로 테스트 실행 전/후에 필요한 동작을 정의.
    # return TestClient(app)


@fixture()
def test_user(client):
    data = {'email':'user00@test.com',
            'password':'teststring'}
    
    res =client.post('/users/signup/',
                     json=data)
    # print(res.json())

    user = res.json()
    user['password']=data['password']
    return user    
    # 해당 fixture 사용 시, test_user['email'], test_user['password'] 접근 가능.

@fixture()
def test_user_another(client):
    data = {'email':'user02@test.com',
            'password':'teststring'}
    
    res =client.post('/users/signup/',
                     json=data)
    # print(res.json())

    user = res.json()
    user['password']=data['password']
    return user    


@fixture()
def token(test_user):
    return token_create({'user_id':test_user['id']})

@fixture()  
def client_authorized(client, token):
    client.headers = {
        **client.headers,
        "authorization": f'Bearer {token}'}
    return client


# @dataclass(order=True)
# class Post:
#     # index: int= field(init=False, repr=False)     # orm model로 넘어가는 과정에서 에러
#     title: str
#     content: str
#     owner_id: int

#     # def __post_init__(self):
#     #     self.index = self.owner_id

@fixture
def test_posts(test_user,test_user_another,session):

    # # WITHOUT DATACLASS
    # posts_data = [{
    #     "title": "first title",
    #     "content": "first content",
    #     "owner_id": test_user['id']
    # }, {
    #     "title": "2nd title",
    #     "content": "2nd content",
    #     "owner_id": test_user['id']
    # },
    #     {
    #     "title": "3rd title",
    #     "content": "3rd content",
    #     "owner_id": test_user['id']
    # }]                                                 

    # post_1 = Post("first title", "first content", 1)
    # post_2 = Post("second title", "second content", 1)
    # post_3 = Post("thid title", "third content", 1)
    # posts = [post_1, post_2, post_3]

    # def create_post_data(posts):
    #     return m.Post(**asdict(posts))
    
    # # post_mapped = map(create_post_data, posts_data)
    # posts_mapped = list(map(create_post_data, posts))
  
    # session.add_all(posts_mapped)
    # session.commit()
 
    post1=m.Post(**{'title':"1 title", 'content':"1 content",'owner_id':test_user['id']})
    post2=m.Post(**{'title':"2 title", 'content':"2 content",'owner_id':test_user['id']})
    post3=m.Post(**{'title':"3 title", 'content':"3 content",'owner_id':test_user_another['id']})

    posts = [post1, post2, post3]

    session.add_all(posts)
    session.commit()
    posts = session.query(m.Post).all()

    return posts