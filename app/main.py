from random import randrange
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Annotated
from httpx import delete
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

# create tables
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
    # rating: int|None


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {'data':posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def creat_post(post:Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    # not good
    new_post = models.Post(**post.dict())    # better

    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # show the new post
    return {"data":new_post}


@app.get("/posts/{id}")
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()   # first() > more efficient
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no post, id={id}")
    return {'result': post}     # Fstring > object 


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no post, id={id}"
            )
    post.delete(synchronize_session=False)  # without query evaluation
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)