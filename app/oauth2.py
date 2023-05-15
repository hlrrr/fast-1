from fastapi    import Depends, HTTPException, status
from fastapi.security.oauth2    import OAuth2PasswordBearer
from jose   import jwt, JWTError
from datetime   import datetime, timedelta
from .schemas import TokenInfo

SECRET_KEY = "asldkjfl23490asjiodof@#$@#SDFKASDF"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='login')

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
        id:str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        token_data = TokenInfo(id=id)
    
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(access_token:str=Depends(oauth2_scheme)):
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f'Could not validate credentails',
                                           headers={'WWW-Authentocate':'Bearer'})
    return token_verify(access_token, credentials_exception)

