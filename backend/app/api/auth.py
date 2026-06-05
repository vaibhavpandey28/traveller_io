from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.core.logger import get_logger
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session

from app.services.user.service import get_user_by_email, create_user


logger = get_logger(__name__)
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # create_user can be implemented to persist the user; call if available
    try:
        create_user(db, user)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return {"detail": "User registered successfully"}
