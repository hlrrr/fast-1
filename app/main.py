from enum import auto
from typing_extensions import deprecated
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
import psycopg2
import time


# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# db connection
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


@app.get("/posts", status_code=status.HTTP_200_OK, response_model=list[schemas.PostInfo])
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.PostInfo)
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()   # first() > more efficient

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no post, id={id}")
    return post   # Fstring > object 


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostInfo)
def creat_post(post:schemas.PostBase, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    # not good
    new_post = models.Post(**post.dict())    # better

    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # show the new post
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no post, id={id}"
            )
    query.delete(synchronize_session=False)  # without query evaluation
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostInfo)
def update_post(id:int, updating: schemas.PostBase, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    # post = query.first()

    if query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no post, id={id}"
            )
    query.update(updating.dict(), synchronize_session=False)
    # print(updating.dict())
    db.commit()

    return query.first()

@app.post("/user/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserInfo)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == user.email)
    if query.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"already exixst, email={user.email}"
            )
    
    hashed_pswd = utils.hash(user.password)
    user.password = hashed_pswd
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    # show the new post
    return new_user


@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserInfo)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"not exists, user_id = {id}")
    return user
