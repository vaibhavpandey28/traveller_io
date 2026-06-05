from sqlalchemy.orm import Session # type: ignore
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def get_user_by_email(db:Session, email:str)->User:
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session,user:UserCreate)->User:

    user_data = user
    hashed_password = hash_password(user.password)
    user_data.password = hashed_password
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db:Session):
    return db.query(User).all()