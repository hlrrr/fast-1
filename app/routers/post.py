from fastapi    import Depends, Response, status, HTTPException, APIRouter
from ..     import models, schemas, oauth2
from ..annotations    import annotation_db


router = APIRouter(
    prefix='/posts',
    tags=["Posts"],
    # dependencies=[Depends(oauth2.get_current_user)],    
)

@router.get("/", 
            status_code=status.HTTP_200_OK,
            response_model=list[schemas.PostInfo])
def get_posts(db:annotation_db,
              whois:int=Depends(oauth2.get_current_user)):
            # db:Session=Depends(get_db)
            # db:Annotated[Session, Depends(get_db)]
    print(whois.email)
    posts=db.query(models.Post).all()
    return posts


@router.get("/{id}",  
            status_code=status.HTTP_200_OK,
            response_model=schemas.PostInfo)
def get_post(id:int,
            db:annotation_db,
            whois=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()   # first() > more efficient
    print(whois.email)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")
    return post   # Fstring > object 


@router.post("/", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.PostInfo)
def creat_post(post:schemas.PostBase, 
               db:annotation_db):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    # not good
    new_post = models.Post(**post.dict())    # better

    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # show the new post
    return new_post


@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, 
                db:annotation_db):
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")
    query.delete(synchronize_session=False)  # without query evaluation
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", 
            response_model=schemas.PostInfo)
def update_post(id:int, 
                updating: schemas.PostBase,
                db: annotation_db):
    query = db.query(models.Post).filter(models.Post.id == id)
    # post = query.first()

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")
    query.update(updating.dict(), 
                 synchronize_session=False)
    db.commit()

    return query.first()