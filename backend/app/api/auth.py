from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Request
from app.core.database import get_db
from app.core.logger import get_logger
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse,UserLogin,UserLoginResponse,UpdateProfile,UpdateProfileForm
from app.services.user_service import get_user_by_email,create_user
from app.core.security import verify_password,create_access_token



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
    

@router.post("/login",response_model= UserLoginResponse ,  status_code=status.HTTP_200_OK)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    
    if not existing_user:
        logger.warning(f"Login failed: User with email {user.email} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    check_password = verify_password(user.password, existing_user.password)

    if not check_password:
        logger.warning(f"Login failed: Invalid password for user with email {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": existing_user.email, "user_id": existing_user.id})
    
    return UserLoginResponse(access_token=access_token, email=existing_user.email)


@router.post("/update-profile")
async def update_profile(
    user: UpdateProfile = Depends(UpdateProfileForm.as_form),
    profile_picture: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    
    print(f"Received profile update for user: {user.username}, with profile picture: {profile_picture.filename if profile_picture else 'No file uploaded'}")

    return {
        "user": user.model_dump(),
        "file": profile_picture.filename if profile_picture else None
    }

