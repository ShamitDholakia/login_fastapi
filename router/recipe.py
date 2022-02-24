from typing import Optional
from fastapi import APIRouter, Depends,Request,Depends,HTTPException
import models
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel,Field

from models import Recipe
models.Base.metadata.create_all(bind=engine)

router=APIRouter()

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()
class Recipe(BaseModel):
    name:str
    description:Optional[str]


@router.get("/")
async def read_all_recipe(db:Session = Depends(get_db)):
    recipe=db.query(models.Recipe).all()
    return recipe

@router.get("/recipe/{recipe_id}")
async def read_recipe(recipe_id:int,db:Session = Depends(get_db)):
    recipe_model=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if recipe_model is not None:
       return recipe_model
    return http_exception()

@router.post("/")
async def create_recipe(recipe:Recipe,db:Session=Depends(get_db)):
    recipe_model=models.Recipe()
    recipe_model.name=recipe.name
    recipe_model.description=recipe.description
    recipe_model.owner_id=recipe.owner_id

    db.add(recipe_model)
    db.commit()

    return succesful_response(200)
@router.put("/{recipe_id}")
async def edit_recipe(recipe_id:int,recipe:Recipe,db:Session = Depends(get_db)):
    recipe_model=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if recipe_model is None:
        raise http_exception()
    recipe_model.name=recipe.name
    recipe_model.description=recipe.description
    recipe_model.owner_id=recipe.owner_id

    db.add(recipe_model)
    db.commit()
    return succesful_response(200)
@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id:int,db:Session = Depends(get_db)):
    recipe_model=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if recipe_model is None:
        raise http_exception()

    db.query(models.Recipe).filter(models.Recipe.id==recipe_id).delete()
    db.commit()

    return succesful_response(200)

def succesful_response(status_code:int):
    return {
            'status':status_code,
            'transaction':'Succesful'
            }
def http_exception():
     raise HTTPException(status_code=404,detail="item not found")

