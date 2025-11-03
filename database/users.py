# simple_app.py
from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
from database import db 
import bcrypt
import os
from dotenv import load_dotenv
import uvicorn
import jwt
from middleware import create_token,verify_token
from datetime import datetime, timedelta
from typing import Annotated, Optional

load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")
token_time=int(os.getenv("token_time"))

# MODELS
class Simple(BaseModel):
    name: str = Field(..., example="Sam Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
    user_type: str = Field(..., example="student")
    # user_id: str = Field(..., example="")


class LoginRequest(BaseModel):
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
    
    
class EnrollmentRequest(BaseModel):
    course_id: Optional[int] = Field(None, example=1)
    course_title: Optional[str] = Field(None, example="Backend Course")
       
# SIGNUP ENDPOINT
@app.post("/signup")
def signUp(input: Simple):
    try:
        # Check if user already exists
        duplicate_query = text("SELECT * FROM users WHERE email = :email")
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        
        if existing:
            print("Email already exists")

        query = text("""
            INSERT INTO users (name, email, password, user_type)
            VALUES (:name, :email, :password, :user_type)
        """)

        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)

        db.execute(query, {"name": input.name, "email": input.email, "password": hashedPassword, "user_type": input.user_type})
        db.commit()

        return {"message": "User created successfully",
                "data": {"name": input.name, "email": input.email, "user_type": input.user_type}}

    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))



# LOGIN ENDPOINT
@app.post("/login")
def login(input: LoginRequest):
    try:
        # Fetch user by email
        query = text("SELECT * FROM users WHERE email = :email")
        result = db.execute(query, {"email": input.email}).fetchone()

        if not result:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Check password
        verified_password = result.password  
        if not bcrypt.checkpw(input.password.encode("utf-8"), verified_password.encode("utf-8")):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        encoded_token= create_token(details={"email":result.email,"user_type": result.user_type}, expiry=token_time)
        return {
            "message":"Login Successful",
            "token": encoded_token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

#COURSE ENDPOINT
class courseRequest(BaseModel):
    title:str = Field(..., example="Backend Course")
    level: str = Field(..., example = "Beginner")

@app.post("/courses")
def addcourses(input: courseRequest, user_data = Depends(verify_token)):
    if user_data['user_type'] != 'admin':
        raise HTTPException(status_code=403, detail="Permission denied. Only admins can add courses.")

    try:
        query = text("""
            INSERT INTO courses (title, level)
            VALUES (:title, :level)
            """)
        db.execute(query, {"title": input.title, "level": input.level})
        db.commit()

        return {"message": "Course added successfully", "course": input.title}
    
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e)) 

    
#ENROLL ENDPOINT       
@app.post("/enroll")
def enroll_course(input: EnrollmentRequest, user_data= Depends(verify_token)):
      try:
            user_query = text("SELECT id FROM users WHERE email = :email")
            user_result = db.execute(user_query, {"email": user_data["email"]}).fetchone()
            
            if not user_result:
                raise HTTPException(status_code=404, detail="User not found.")
            user_id = user_result.id

            if input.course_id:
                course_query = text("SELECT id, title FROM courses WHERE id = :courseId")
                course_result = db.execute(course_query, {"courseId": input.course_id}).fetchone()
                
            elif input.course_title:
                course_query = text("SELECT id, title FROM courses WHERE title = :title")
                course_result = db.execute(course_query, {"title": input.course_title}).fetchone()
            else:
                raise HTTPException(status_code=400, detail="Please provide either course_id or course_title.")

            if not course_result:
                raise HTTPException(status_code=404, detail="Course not found.")

            course_id = course_result.id
            course_title = course_result.title

    
            existing_query = text("""
                SELECT * FROM enrollments 
                WHERE userId = :userId AND courseId = :courseId
            """)
            existing = db.execute(existing_query, {"userId": user_id, "courseId": course_id}).fetchone()

            if existing:
                raise HTTPException(status_code=400, detail=f"Already enrolled in '{course_title}'.")

            enroll_query = text("""
                INSERT INTO enrollments (userId, courseId)
                VALUES (:userId, :courseId)
            """)
            db.execute(enroll_query, {"userId": user_id, "courseId": course_id})
            db.commit()

            return {
                "message": f"Enrollment successful in '{course_title}'",
                "userId": user_id,
                "courseId": course_id
            }

      except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
