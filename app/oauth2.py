from fastapi    import Depends, HTTPException, status
from fastapi.security.oauth2    import OAuth2PasswordBearer
from jose   import jwt, JWTError
from datetime   import datetime, timedelta
from typing     import Annotated
from sqlalchemy.orm     import Session
from .  import schemas, models, database
from .config    import settings


# A "bearer" token is not the only option.

SECRET_KEY = settings.secrete_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='login')    
# tokenUrl 조건 확인 
# https://fastapi.tiangolo.com/tutorial/security/first-steps/#fastapis-oauth2passwordbearer

def token_create(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp':expire})
    jwt_encoded=jwt.encode(claims=to_encode,
                           key=SECRET_KEY,
                           algorithm=ALGORITHM)
    return jwt_encoded


def token_verify(access_token: str, credentials_exception):
    try:
        payload=jwt.decode(token=access_token,
                           key=SECRET_KEY,
                           algorithms = ALGORITHM)
        user_id:str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenInfo(id=user_id)
        # print(user_id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(db:Annotated[Session, Depends(database.get_db)],
                     access_token:str=Depends(oauth2_scheme)):
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f'Could not validate credentails',
                                           headers={'WWW-Authenticate':'Bearer'})
    token = token_verify(access_token, credentials_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    
    return user
    # global dependency VS path operation function
    # 파라미터로 사용해야 사용자 정보 호출 용이(복합사용?)