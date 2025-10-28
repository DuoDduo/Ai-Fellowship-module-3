# simple_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from database import db  # Make sure this exposes a valid SQLAlchemy session
import bcrypt
import os
from dotenv import load_dotenv
import uvicorn
import jwt
from middleware import create_token
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")
token_time=int(os.getenv("token_time"))

# MODELS

class Simple(BaseModel):
    name: str = Field(..., example="Sam Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
    user_type: str = Field(..., examples="student")


class LoginRequest(BaseModel):
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
# SIGNUP ENDPOINT

@app.post("/signup")
def signUp(input: Simple):
    try:
        # Check if user already exists
        duplicate_query = text("SELECT * FROM users WHERE email = :email")
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
        
          # Insert user
        insert_query = text("""
            INSERT INTO users (name, email, password, user_type)
            VALUES (:name, :email, :password, :user_type)
        """)
        
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(input.password.encode("utf-8"), salt)

      
        db.execute(insert_query, {
            "name": input.name,
            "email": input.email,
            "password": hashed_password.decode("utf-8")
        })
        db.commit()

        return {"message": "User created successfully", "data": {"name": input.name, "email": input.email}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



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

class courseRequest(BaseModel):
    title:str = Field(..., example="Backend Course")
    level: str = Field(..., example = "Beginner")

@app.post("/courses")
def addcourses(input:courseRequest):
    try:
        query = text("""
                     
                     """)
       
    
    
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
