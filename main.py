from functools import lru_cache
from typing import List

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.importer.FileImporter import FileImporter
from app.core.settings import Settings
from app.core.database import SessionLocal
from app.users import models, schemas, crud

app = FastAPI()

@lru_cache
def get_settings():
    return Settings()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/info/")
def info():
    return get_settings().DATABASE_URL


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = crud.get_users(db, skip, limit)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/importfile/", status_code=status.HTTP_201_CREATED)
async def import_file(force_insert: bool = False, file: UploadFile = File(...), db: Session = Depends(get_db)):
    list_valid_rows, list_invalid_rows = FileImporter.file_import(file, row_validator_method=models.User.validate_dict)
    if force_insert or len(list_invalid_rows) == 0:
        try:
            crud.bulk_create_user(db, list_valid_rows)
        except IntegrityError as ex:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ex)) from ex
            
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=list_invalid_rows)

    return {
        "invalid_rows":list_invalid_rows
    }
