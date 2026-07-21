from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    roll_no: str
    branch: str


class Teacher(BaseModel):
    name: str
    teacher_id: str
    department: str