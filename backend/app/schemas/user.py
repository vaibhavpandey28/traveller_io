from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name:str
    username:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    username:str
    email:str
    profile_picture:str = None

    class Config:
        from_attributes = True