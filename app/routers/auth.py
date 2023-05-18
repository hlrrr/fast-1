from typing import Optional
from fastapi    import status, HTTPException, Depends, APIRouter
from fastapi.param_functions import Form
from fastapi.security.oauth2    import OAuth2PasswordRequestForm
from ..     import models, utils, oauth2, schemas
from ..annotations  import annotation_db

router = APIRouter(
    # prefix='/auth',
    tags=['Authentication'],
    )

@router.post('/token', 
             status_code=status.HTTP_200_OK,
             response_model=schemas.Token)
def token():
    access_token = oauth2.token_create(data={'user_id':3})
    return {'access_token':access_token, 'token_type':'bearer'}

    
@router.post('/login', 
             status_code=status.HTTP_200_OK,
             response_model=schemas.Token)
def login(db:annotation_db,
          user_credentials:OAuth2PasswordRequestForm=Depends()):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()     # fields of OAuth2PasswordRequestForm  -> username, password

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    elif not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    
    access_token = oauth2.token_create(data={'user_id':user.id})
    return {'access_token':access_token, 'token_type':'bearer'}
