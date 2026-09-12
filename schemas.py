from pydantic import BaseModel, Field


class Student(BaseModel):
    id: int
    name: str = Field(min_length=2)
    age: int = Field(gt=0, lt=100)
    course: str = Field(min_length=2)

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str

    class Config:
        from_attributes = True
        
class StudentCreateResponse(BaseModel):
    message: str
    student: StudentResponse
       
class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str