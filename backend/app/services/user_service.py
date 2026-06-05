from sqlalchemy.orm import Session # type: ignore
from app.models.user import User
from app.schemas.user import UserCreate

def get_user_by_email(db:Session, email:str)->User:
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session,user:UserCreate)->User:
    user = User( **user.model_dump() )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db:Session):
    return db.query(User).all()