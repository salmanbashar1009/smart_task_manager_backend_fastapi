import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from .config import settings

#initialize Argon2 password hasher
password_hasher = PasswordHash.recommended()

#verify hashed password
def verify_password(plain_password: str, hashed_password:str):
    try:
        password_hasher.verify(plain_password,hashed_password)
        return True
    except Exception:
        return False
    

#convert plain password into hashed password
def get_hased_password(password:str)->str:
    return password_hasher.hash(password)

# create access token
def create_access_token(data: dict)->str:
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt