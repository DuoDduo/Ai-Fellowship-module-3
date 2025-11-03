import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Load environment variables
load_dotenv()

bearer = HTTPBearer()
secret_key = os.getenv("SECRET_KEY") 

if not secret_key:
    raise ValueError("SECRET_KEY not found in environment variables")

def create_token(details: dict, expiry: int):
    """
    Generate JWT token with expiration.
    """
    expire = datetime.now() + timedelta(minutes=expiry)
    details.update({"exp": expire})
    token = jwt.encode(details, secret_key, algorithm="HS256")  
    return token

def verify_token(request: HTTPAuthorizationCredentials = Security(bearer)):
    """
    Verify and decode JWT token.
    """
    token = request.credentials
    verified_token = jwt.decode(token, secret_key, algorithms=["HS256"])
    return {
        "email":  verified_token.get("email"),
        "user_type":  verified_token.get("user_type")
    }
    