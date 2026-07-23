from fastapi import APIRouter, HTTPException, status

from db import users
from models import User,Login
from utils import pwd_context
from jose import jwt
from jose import JWTError
from datetime import datetime,timedelta
from config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: User):
    existing_user = users.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)

    users.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    })

    return {
        "message": "User registered successfully"
    }


@router.post("/login",status_code=status.HTTP_200_OK)
def login(login:Login):
    existing_user = users.find_one({"email":login.email})
    if not existing_user:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not pwd_context.verify(login.password,existing_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token = create_access(
        {
            "email":existing_user["email"]
        }
    )
    return{
        "access token" : access_token,
        "token-type" : "bearer"
    }

def create_access(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(
        to_encode,SECRET_KEY,algorithm=ALGORITHM
    )
    return encoded_jwt
def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token : str=Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload
    
@router.get("/profile")
def profile(current_user = Depends(get_current_user)):
    return current_user
