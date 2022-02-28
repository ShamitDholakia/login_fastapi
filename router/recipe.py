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

class Ingredients(BaseModel):
    ingredients1:str
    ingredients2:Optional[str]

@router.get("/")
async def read_all_recipe(db:Session = Depends(get_db)):
    recipe=db.query(models.Recipe).all()
    return recipe

@router.get("/read_all_ingr")
async def read_all_ingredients(db:Session = Depends(get_db)):
    ingredients=db.query(models.Ingredients).all()
    return ingredients

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

    db.add(recipe_model)
    db.commit()
    return succesful_response(200)

@router.post("/create_ingr")
async def create_ingredients(ingredients:Ingredients,db:Session=Depends(get_db)):
    ingredients_model=models.Ingredients()
    ingredients_model.ingredients1=ingredients.ingredients1
    ingredients_model.ingredients2=ingredients.ingredients2  

    db.add(ingredients_model)
    db.commit()
    return succesful_response(200)

@router.put("/{recipe_id}")
async def edit_recipe(recipe_id:int,recipe:Recipe,db:Session = Depends(get_db)):
    recipe_model=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if recipe_model is None:
        raise http_exception()
    recipe_model.name=recipe.name
    recipe_model.description=recipe.description
    db.add(recipe_model)
    db.commit()
    return succesful_response(200)

@router.put("/create_ingr/{ingredients_id}")
async def edit_ingredients(ingredients_id:int,ingredients:Ingredients,db:Session = Depends(get_db)):
    ingredients_model=db.query(models.Ingredients).filter(models.Ingredients.id==ingredients_id).first()
    if ingredients_model is None:
        raise http_exception()
    # recipe_model.owner_id=recipe.owner_id

    ingredients_model.ingredients1=ingredients.ingredients1
    ingredients_model.ingredients2=ingredients.ingredients2
    db.add(ingredients_model)
    db.commit()
    return succesful_response(200)

@router.delete("/create_ingr/{recipe_id}")
async def delete_recipe(recipe_id:int,db:Session = Depends(get_db)):
    recipe_model=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if recipe_model is None:
        raise http_exception()
    db.query(models.Recipe).filter(models.Recipe.id==recipe_id).delete()
    db.commit()
    return succesful_response(200)

@router.delete("/{ingr_id}")
async def delete_ingredients(ingr_id:int,db:Session = Depends(get_db)):
    recipe_model=db.query(models.Ingredients).filter(models.Ingredients.id==ingr_id).first()
    if recipe_model is None:
        raise http_exception()

    db.query(models.Ingredients).filter(models.Ingredients.id==ingr_id).delete()
    db.commit()
    return succesful_response(200)

def succesful_response(status_code:int):
    return {
            'status':status_code,
            'transaction':'Succesful'
            }
def http_exception():
     raise HTTPException(status_code=404,detail="item not found")