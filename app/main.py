from random import randrange
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Annotated
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn=psycopg2.connect(
            host='211.117.18.86',
            port='15432',
            user='lima',
            password='1q2w3e4r5t',
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print(f"Db conn: Done")
        break

    except Exception as error:  
        print("DB conn: Failed")
        print("Error: ", error)
        time.sleep(3)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int|None

testpost = [
    {
    "id":1,
    "title":"testtitle1",
    "content":"testcontest1",
    },
    {
    "id":2,
    "title":"testtitle2",
    "content":"testcontest2",
    }
    ]

# @app.get("/")
# async def root(q:Annotated[str,"this is metadata",Query(max_length=1)]):
#     return {"hihihi"}


# @app.post("/creatpost")
# async def createpost(payload:dict = Body(...)):
#     print(payload)
#     return {"msg": f"title:{payload['first']}, content:{payload['second']}"}


# @app.post("/create")
# async def create(post:Post):
#     # print(post.title)
#     print(post.dict())
#     testpost.append(post.dict())
#     return {"data":post}

@app.get("/posts")
async def posts():
    return testpost

@app.post("/posts",
          status_code=status.HTTP_201_CREATED)
async def creatPost(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,999)
    testpost.append(post_dict)
    return {"data":post_dict}

# @app.post("/posts/{id}")
# async def get(id:int, response: Response):
    # response.status_code=status.HTTP_404_NOT_FOUND
    # return {f'post no.{id}'}

@app.post("/posts/{id}") # path param ID as str
async def get(id:int): # converted into int, need to be converted into str again in code processing
    raise HTTPException(
        status_code=status.HTTP_302_FOUND,
        detail=f"this is detail, no.{id}",
        )


@app.delete("/posts/{id}",
            status_code=status.HTTP_204_NO_CONTENT)
async def deletePost(id:int):
    return

@app.put("/posts/{id}",
         status_code=status.HTTP_200_OK)
async def putPost(id:int,post:Post):
    return


@app.get("/sqlacm")
def db_test(db: Session = Depends(get_db)):
    return {
        'ststus':'succsess'
    }