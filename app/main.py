from fastapi    import FastAPI
from psycopg2.extras    import RealDictCursor
from .  import models
from .database      import engine
from .routers   import post, user, auth
import psycopg2
import time

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
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