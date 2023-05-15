from fastapi    import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2    import OAuth2PasswordRequestForm
from ..     import models, schemas, utils, oauth2
from ..database     import get_db
from sqlalchemy.orm     import Session

router = APIRouter(
    prefix='/auth',
    tags=['Authentication'],
)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()     # fields of OAuth2PasswordRequestForm  -> username, password

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    elif not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentiasl')
    
    access_token = oauth2.token_create(data = {'user_id':user.id})

    return   {'access_token':access_token, 'token_type':'bearer'}
