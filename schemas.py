from pydantic import BaseModel, Field, field_validator


class Student(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(gt=0, lt=100)
    course: str = Field(min_length=2, max_length=100)

    @field_validator("name", "course")
    @classmethod
    def must_contain_non_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty or only whitespace")
        return value

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
