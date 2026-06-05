from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from fastapi import Form, File, UploadFile, Depends


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, title="Name", description="The user's real name")
    username: str = Field(..., min_length=3, max_length=20,title="Username", pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., max_length=100,title="Password", description="Must be at least 8 characters long and include uppercase, lowercase, digit, and special character.") 
    @field_validator("name", "username", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v

    # 2. Strict Custom Password Complexity Rules
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_+-]", v):
            raise ValueError("Password must contain at least one special character.")
        return v


class UpdateProfile(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr



class UpdateProfileForm(UpdateProfile):
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        username: str = Form(...),
        email: EmailStr = Form(...)
    ):
        return cls(
            name=name,
            username=username,
            email=email
        )


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    profile_picture: str | None = None
    model_config = {
        "from_attributes": True
    }
    
    
class UserLoginResponse(BaseModel):
        email :str 
        access_token: str
        context: str = "Login successful!"
        model_config = {
            "from_attributes": True
        }
