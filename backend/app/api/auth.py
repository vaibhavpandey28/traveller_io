from fastapi import APIRouter, Depends, HTTPException,status
from app.core.database import get_db
from app.core.logger import get_logger
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import get_user_by_email,create_user



logger = get_logger(__name__)
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    
    if existing_user:
        logger.warning(f"Registration failed: Email {user.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    try:
        new_user = create_user(db, user)
        logger.info(f"User created successfully with ID: {new_user.id}")
        return new_user
    except Exception as e:
        logger.error(f"Database error during user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to create user"
        )