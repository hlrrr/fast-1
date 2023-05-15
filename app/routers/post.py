from fastapi import Response, status, HTTPException, Depends, APIRouter

from app import oauth2
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/posts',
    tags=["Posts"],
    # dependencies=[Depends(get_token_header)],
)

@router.get("", status_code=status.HTTP_200_OK, response_model=list[schemas.PostInfo])
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.PostInfo)
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()   # first() > more efficient

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")
    return post   # Fstring > object 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostInfo)
def creat_post(post:schemas.PostBase, db: Session = Depends(get_db),
               get_current_user:int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)    # not good
    new_post = models.Post(**post.dict())    # better

    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # show the new post
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")
    query.delete(synchronize_session=False)  # without query evaluation
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostInfo)
def update_post(id:int, updating: schemas.PostBase, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    # post = query.first()

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no post, id={id}")
    query.update(updating.dict(), synchronize_session=False)
    # print(updating.dict())
    db.commit()

    return query.first()