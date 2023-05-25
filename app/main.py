from fastapi    import FastAPI, Depends
from .  import models
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