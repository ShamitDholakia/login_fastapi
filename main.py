from router import auth,recipe
from fastapi import FastAPI#, Depends,HTTPException,APIRouter
import models
from database import engine #,SessionLocal

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(auth.router)
app.include_router(recipe.router)