# simple_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from database import db, engine
import bcrypt
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")

class Simple(BaseModel):
    name: str = Field(..., example="Sam Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")

@app.post("/signup")
def signUp(input: Simple):
    try:
        # Check for existing user
        duplicate_query = text("SELECT * FROM users WHERE email = :email")
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(input.password.encode("utf-8"), salt)

        # Insert user
        insert_query = text("""
            INSERT INTO users (name, email, password)
            VALUES (:name, :email, :password)
        """)
        db.execute(insert_query, {
            "name": input.name,
            "email": input.email,
            "password": hashed_password.decode("utf-8")
        })
        db.commit()

        return {"message": "User created successfully", "data": {"name": input.name, "email": input.email}}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    engine.dispose()
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
