from sqlalchemy import Boolean,Integer,String,Column,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=False)
    email=Column(String,unique=True,index=True)
    username=Column(String, unique=True,index=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    is_active=Column(Boolean,default=True)

    recipe=relationship("Recipe",back_populates="owner")

class Recipe(Base):
    __tablename__="recipe"
    id=Column(Integer,primary_key=True,index=False)
    name=Column(String)
    description=Column(String)
    owner_id=Column(Integer,ForeignKey("users.id"))
    owner=relationship("Users",back_populates="recipe")
    ingredients=relationship("Ingredients",back_populates="owner2")

class Ingredients(Base):
    __tablename__="ingredients"
    id=Column(Integer,primary_key=True,index=False)
    ingredients1=Column(String)
    ingredients2=Column(String)
    foreign_key=Column(Integer,ForeignKey("recipe.id"))
    owner2=relationship("Recipe",back_populates="ingredients")