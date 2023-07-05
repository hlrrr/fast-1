from app    import models as m
from app    import schemas as s
from dataclasses    import dataclass, field, asdict
import json

# @dataclass(order=True)
# class Post:
#     index: int= field(init=False, repr=False)
#     title: str
#     content: str
#     owner_id: int

#     def __post_init__(self):
#         self.index = self.owner_id

 
def test_posts():
    # post_1 = Post("first title", "first content", 1)
    # post_2 = Post("second title", "second content", 1)
    # post_3 = Post("thid title", "third content", 1)
    post = m.Post
    post1=post(**{'title':"1 title", 'content':"1 content",'owner_id':1})
    post2=post(**{'title':"2 title", 'content':"2 content",'owner_id':1})
    post3=post(**{'title':"3 title", 'content':"3 content",'owner_id':1})


    posts = [post1, post2, post3]

    print(posts)
    session.add_all(posts)
    session.commit()

    posts = session.query(m.Post).all()
    # def create_post_model(post):
    #    return m.Post(**asdict(post))

    # posts_mapped = (map(create_post_model, posts))
    # print(posts_mapped)

test_posts()



# def user():
#     user = s.UserBase(email='test@gmail.com', password='123')
#     print(type(user))

# user()