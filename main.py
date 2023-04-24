from fastapi import FastAPI, Query
from fastapi.params import Body
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int|None

testpost = [{
    "id":1,
    "title":"testtitle1",
    "content":"testcontest1",
    },
    {
    "id":2,
    "title":"testtitle2",
    "content":"testcontest2",
    }]

@app.get("/")
async def root(q:Annotated[str,"thi is metadata",Query(max_length=1)]):
    return {"hihihi"}

@app.get("/posts")
async def posts():
    return testpost

@app.post("/creatpost")
async def createpost(payload:dict = Body(...)):
    print(payload)
    return {"msg": f"title:{payload['first']}, content:{payload['second']}"}

@app.post("/create")
async def create(post:Post):
    # print(post.title)
    print(post.dict())
    testpost.append(post.dict())
    return {"data":post}