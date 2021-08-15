from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(cpf=user.cpf, private=user.private)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def bulk_create_user(db: Session, list_user: list):
    db.bulk_insert_mappings(models.User, list_user)
    db.commit()


def get_users(db: Session, skip: int = 0, limit: int = 100): 
    return db.query(models.User).offset(skip).limit(limit).all()