from fastapi import FastAPI, Query, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
import psycopg2
import time
from .routers import post, user

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)


@app.get('/')
def root():
    msg = {"this is": "my template"}
    return "my template"

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