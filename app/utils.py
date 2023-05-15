from passlib.context    import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],
                           deprecated='auto')

def hash(password:str):
    return pwd_context.hash(secret=password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(secret=plain_password,
                              hash=hashed_password)