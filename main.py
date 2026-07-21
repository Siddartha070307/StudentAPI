from fastapi import FastAPI

from routers.students import router as student_router
from routers.teachers import router as teacher_router

app = FastAPI()

app.include_router(student_router)
app.include_router(teacher_router)


@app.get("/")
def home():
    return {
        "message":"Welcome to Student API"
    }


@app.get("/about")
def about():
    return {
        "course":"Backend Bootcamp",
        "name":"Sid"
    }


@app.get("/college")
def college():
    return {
        "college":"LBRCE",
        "branch":"CSE"
    }


@app.get("/contact")
def contact():
    return {
        "email":"sid@example.com"
    }