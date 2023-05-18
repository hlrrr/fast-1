from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..annotations import annotation_db

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    )


@router.post("/signup",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserInfo)
def create_user(user: schemas.UserBase,
                db:annotation_db):
    query = db.query(models.User).filter(models.User.email == user.email)
    if query.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"already exists, email={user.email}")
    
    hashed_pswd = utils.hash(user.password)
    user.password = hashed_pswd
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    # show the new post
    return new_user


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=schemas.UserInfo)
def get_user(id: int,
             db:annotation_db):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"not exists, user_id = {id}")
    return user