from fastapi import FastAPI

from database import Base, engine
from routers import auth, students


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(auth.router)
app.include_router(students.router)


@app.get("/")
def home():
    return {
        "message": "Student Management API is working!"
    }