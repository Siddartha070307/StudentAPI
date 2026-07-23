from fastapi import FastAPI

from routes.students import router as student_router
from routes.teachers import router as teacher_router
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Student API"
    }


@app.get("/about")
def about():
    return {
        "course": "Backend Bootcamp",
        "name": "Sid"
    }


@app.get("/college")
def college():
    return {
        "college": "LBRCE",
        "branch": "CSE"
    }


@app.get("/contact")
def contact():
    return {
        "email": "sid@example.com"
    }