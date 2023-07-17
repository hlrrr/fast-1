from fastapi    import FastAPI 
from fastapi.middleware.cors    import CORSMiddleware
from starlette_admin.contrib.sqla.admin import Admin
from starlette_admin.contrib.sqla.view  import ModelView


from .  import models as m
from .database  import engine
from .routers   import post, user, auth, vote
from .config   import settings

# models.Base.metadata.create_all(bind=engine)      # create tables / replaced by alembic

app = FastAPI(
    swagger_ui_parameters={"defaultModelsExpandDepth": 0}       # shrink schema section
    )      


@app.get(path='/', 
         summary='root path for health check')
def root():
    '''
    `Radio Check`
    '''
    return "welcome to my brain storage"

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
                #    dependencies=[Depends(oauth2.get_current_user)]
app.include_router(vote.router)

origins = [""]
''' middlewares
 리퀘스트들이 정의한 미들웨어들을 역순으로 타고 들어옴.
'''
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