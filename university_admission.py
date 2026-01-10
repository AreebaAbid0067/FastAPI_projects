from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()

@app.get("/")
def university_welcome():
    return {
        "message" : "Welcome to Riphah University!"
    }

@app.get("/university")
def get_university_info():
    return {
        "university_name":"This is Riphah International University Portal",
        "Programs" : ["BSCS","MLT","BCA","BSE"]
    }

@app.get("/admissions")
def get_info():
    return {
        "admission_open" : True,
        "deadline" : "2025-12-31",
        "contact_email" : "admissions@harvard.edu.pk"
    }

#student registration
class StudentSignup(BaseModel):
    name : str
    email: str
    password : str = Field(..., min_length=8, description="Password must be atleast of 8 characters") # here the ... means required field
    age : Optional[int] = Field(None, ge=16, le=60, description="age must be between 16 and 60")

@app.post("/auth/signup")
def signup(student:StudentSignup):
    try:
        if len(student.password) < 8:
            raise ValueError("password must be atleast 8 characters long")
        
        return{
            "message" : f"Welcome {student.name}, your account has been created successfully!",
            "status" : "success",
            "data" :
            {
                "name" : student.name,
                "email": student.email,
                "age" : student.age
            }
        }

    except Exception as e:
        return{
            "message" : str(e),
            "status" : "error",
            "data" : None
        }
    

# now applying for admission 
class AdmissionApplication(BaseModel):
    student_id: int
    program_name: str
    highschool_marks: float = Field(...,ge=0, le=100, description="marks should be between 0 and 100")


@app.post("/admissions/apply")
def apply_for_admission(application: AdmissionApplication):
    try:
        if application.highschool_marks < 50:
            raise ValueError("sorry your marks are below 50%. admission request rejected")
        
        return{
            "status" : "success",
            "message" : "application submitted successfully",
            "data" : {
                "student_id" : application.student_id,
                "program" : application.program_name,
                "marks" : application.highschool_marks
            }
        }
    
    except Exception as e:
        return{
            "message" : str(e),
            "status" : "error",
            "data" : None
        }
    
students = {
    1: {"id" : 1, "name":"Areeba", "email" : "arebz@gmail.com","marks":87},
    2: {"id": 2, "name": "Ali Khan", "email": "ali@example.com", "marks": 72},
    3: {"id": 3, "name": "Sara Ahmed", "email": "sara@example.com", "marks": 90}

}

programs = {
    "BSCS": {"id": "BSCS", "name": "BS Computer Science"},
    "BBA": {"id": "BBA", "name": "Bachelor of Business Administration"}
}


# GET program id
@app.get("/programs/{program_id}")
def get_program(program_id: str):
    try:
        program = programs.get(program_id.upper())
        if not program:
            return{
                "status" : "error",
                "message" : "program not found",
                "data" : None
            }
        
        return {
            "status" : "success",
            "data": program
        }
        
    except Exception as e:
        return {"status ": "error",
                "message" : str(e),
                "data": None}
    
# now doing query parameters
@app.get("/students/filter")
def filter_students(min_marks:int=0):
    try:
        filtered = [s for s in students.values()  if s["marks"] >= min_marks]
        return {"status":"success", "count":len(filtered), "data": filtered}
    
    except Exception as e:
        return {"status":"error", "data": None, "message": str(e)}
    
