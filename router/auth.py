from http.client import HTTPException
from turtle import update
from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError
from router import recipe

SECRET_KEY="mkjdnskdsslmc"
ALGORITH="HS256"
class CreateUser(BaseModel):
    username:str
    email:Optional[str]
    first_name:str
    last_name:str
    password:str

class ResetPassword(BaseModel):
    reset_password_token:str
    new_password:str
    confirm_password:str

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

router=APIRouter()

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password,hashed_password):
    return bcrypt_context.verify(plain_password,hashed_password)


def authenticate_user(username:str,password:str,db):
    user=db.query(models.Users).filter(models.Users.username==username).first()

    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False 
    return user   

def create_access_token(username:str,user_id:int,expiry_time:Optional[timedelta]=None):
    encode={"sub":username,"id":user_id}

    if expiry_time:
        expire=datetime.utcnow()+expiry_time
    else:
        expire=datetime.utcnow()+timedelta(minutes=45)
    encode.update({"exp":expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITH
    )
def check_reset_password_token(reset_user:ResetPassword,reset_password:str,db:Session = Depends(get_db)):
    reset_user_new=models.Users
    reset_user_new.hashed_password=reset_user.new_password  
    db.add(reset_user_new)
    db.commit()
    return reset_password


@router.post("/create/user")
async def create_new_user(create_user:CreateUser,db:Session = Depends(get_db)):
    create_new_user = models.Users()
    create_new_user.email=create_user.email
    create_new_user.username=create_user.username
    create_new_user.first_name=create_user.first_name
    create_new_user.last_name=create_user.last_name   

    hash_password=get_password_hash(create_user.password)
    create_new_user.hashed_password=hash_password
    create_new_user.is_active=True

    db.add(create_new_user)
    db.commit()

@router.post("/token")
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_expire=timedelta(minutes=20)
    token=create_access_token(user.username,user.id,expiry_time=token_expire)
    return {"token":token}


@router.post("/forget_password")
async def forget_password(username:str,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.username==username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_expire=timedelta(days=1)
    token=create_access_token(user.username,user.id,expiry_time=token_expire)
    return {"token":token}  
    
@router.patch("/reset_password")
async def reset_password(create_password:ResetPassword,db:Session = Depends()):
    check_valid=await recipe.check_reset_password_token()
    create_password_new=models.Users()
    create_password_new.hashed_password=create_password.new_password

    db.add(create_password_new)
    db.commit()


