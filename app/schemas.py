from pydantic   import BaseModel, EmailStr
from datetime   import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    create_at: datetime
    updated_at: datetime|None

    class Config:
        orm_mode = True
    # to support models that map to ORM objects
    # response_model로 설정시 필요. DB에는 들어가지만, response body 표시에 문제.
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    # https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances


class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True