from fastapi    import FastAPI, Depends
from fastapi.middleware.cors    import CORSMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from .          import models as m
from .database      import engine
from .routers   import post, user, auth, vote
from .config   import settings

# models.Base.metadata.create_all(bind=engine)      # create tables / replaced by alembic

app = FastAPI(
    swagger_ui_parameters={"defaultModelsExpandDepth": 0}       # shrink schema section
    )      


@app.get('/')
def root():
    return {'msg':"my template"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
                #    dependencies=[Depends(oauth2.get_current_user)]
app.include_router(vote.router)

origins = [""]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

''' for starlette_admin
'''
admin = Admin(engine)

admin.add_view(ModelView(m.User))
admin.add_view(ModelView(m.Post))

admin.mount_to(app)