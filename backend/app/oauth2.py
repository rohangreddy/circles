from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# token needs 3 pieces of information:

# SECRET_KEY
SECRET_KEY = settings.secret_key
# Algorithm
ALGORITHM = settings.algorithm
# Expiration Time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    toEncode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})
    
    encJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)

    return encJwt

def verify_access_token(token: str, credential_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id = payload.get("user_id", None)
        
        if not id:
            raise credential_exception

        token_data = schemas.TokenData(id=id)
    except JWTError as e: 
        raise credential_exception
    
    return token_data

# take token from request
# verify correct token using verify_access_token()
# extract id from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail=f"Could not validate credentials", 
                                         headers = {"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

