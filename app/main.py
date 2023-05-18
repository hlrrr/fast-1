from fastapi    import FastAPI, Depends
from psycopg2.extras    import RealDictCursor
import psycopg2
import time
from .  import models, oauth2, database
from .database      import engine
from .routers   import post, user, auth

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
     swagger_ui_parameters={"defaultModelsExpandDepth": 0}      # shrink schema section
)

# @app.get('/')
# def root():
#     return "my template"

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
                #    dependencies=[Depends(oauth2.get_current_user)]


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