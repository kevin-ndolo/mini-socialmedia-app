from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database, models
import os
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# to get a SECRET_KEY string like this run :
# openssl rand -hex 32
# in the terminal.
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))


print(ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token: str, credentials_exception):
    
    try:

      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      id: str = str(payload.get("user_id"))

      if id is None:
              raise credentials_exception
      
      token_data = schemas.TokenData(id=id)
    
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data =verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    print(type(user))

    return  user