from fastapi    import Response, status, HTTPException, APIRouter, Depends
from sqlalchemy import func
from ..     import models, schemas, annotations

router = APIRouter(
    prefix='/posts',
    tags=["Posts"],
    # dependencies=[Depends(oauth2.get_current_user)],    
)

@router.get("/all", 
            status_code=status.HTTP_200_OK,
            response_model=list[schemas.PostInfo])
def all_posts(db:annotations.database,
              limit:int=99,
              offset:int=0,
              search:str|None=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    return posts


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=list[schemas.PostLikey])
def get_posts(db:annotations.database,
            # db:Annotated[Session, Depends(get_db)]
            # db:Session=Depends(get_db),
            whois:annotations.authentication,
            limit:int=99,
            offset:int=0,
            search:str|None=""):
    # posts=db.query(models.Post).filter(models.Post.owner_id==whois.id).offset(offset).all()
    #  = db.query(models.Post).filter(models.Post.owner_id==whois.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()       # 검색어 포함

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('likey')).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()         # with likey
    # result=[{'post':a, 'likey':b} for a,b in posts]
                
    return posts


@router.get("/{id}",  
            status_code=status.HTTP_200_OK,
            response_model=schemas.PostLikey)
def get_post(id:int,
             db:annotations.database):
    # post = db.query(models.Post).filter(models.Post.id==id).first()   # first() > more efficient

    post = db.query(models.Post, func.count(models.Vote.post_id).label('likey')).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()  # with likey
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")

    return post   # Fstring -> object 


@router.post("/", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.PostInfo)
def creat_post(post:schemas.PostBase, 
               db:annotations.database,
               whois:annotations.authentication):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    # not good
    new_post = models.Post(owner_id=whois.id, **post.dict())    # better
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # show the new post
    return new_post


@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, 
                db:annotations.database,
                whois:annotations.authentication):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")
    if post.owner_id != whois.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized")

    post_query.delete(synchronize_session=False)  # without query evaluation
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", 
            response_model=schemas.PostInfo)
def update_post(id:int, 
                updating: schemas.PostBase,
                db: annotations.database,
                whois:annotations.authentication):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")
    elif post.owner_id != whois.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized")
    post_query.update(updating.dict(),
                      synchronize_session=False)
    db.commit()

    return post