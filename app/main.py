# app/main.py
from fastapi import FastAPI, Depends
from app.database import engine
from app import models, services, schemas
from sqlalchemy.orm import Session
from app.utils import get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Bitespeed Contact Service"}

@app.post("/identify", response_model=schemas.IdentifyResponse)
def identify(data: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    return services.identify_user(data, db)