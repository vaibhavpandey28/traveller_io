from sqlalchemy.orm import Session # type: ignore
from app.models.user import User

def get_user_by_email(db:Session, email:str)->User:
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session,name : str, username:str, email:str, password:str, profile_picture:str=None)->User:
    user = User(
        name=name,
        username=username,
        email=email,
        password=password,
        profile_picture=profile_picture
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db:Session):
    return db.query(User).all()