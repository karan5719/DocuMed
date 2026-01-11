from fastapi import Request, HTTPException, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database_simple import Doctor, get_db
import hashlib
import re
import os
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, field_validator
from jose import JWTError, jwt

# Simple password hashing using SHA-256 + salt (more compatible)
SECRET_KEY = os.getenv("SECRET_KEY", "medical_certificate_secret_key_2024")
SALT = os.getenv("SALT", "medical_salt_2024")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    medical_registration_number: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        errors = []
        
        # Length requirements
        if len(v) < 8:
            errors.append("Password must be at least 8 characters long")
        if len(v) > 72:
            errors.append("Password cannot exceed 72 characters")
        
        # Complexity requirements
        if not re.search(r'[A-Z]', v):
            errors.append("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            errors.append("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            errors.append("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            errors.append("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)")
        
        # Medical-specific suggestions
        medical_suggestions = [
            "Consider using: Medical2024!",
            "Example: Doctor@2024",
            "Strong: Med!cal#2024",
            "Secure: Dr.Cert#2024"
        ]
        
        if errors:
            error_msg = "Password requirements not met:\n" + "\n".join(f"• {error}" for error in errors)
            error_msg += f"\n\nSuggestions:\n" + "\n".join(f"• {suggestion}" for suggestion in medical_suggestions)
            raise ValueError(error_msg)
        
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        # Additional email validation for medical professionals
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError("Please enter a valid email address")
        
        # Check for professional email patterns
        professional_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        domain = v.split('@')[-1] if '@' in v else ''
        
        if domain in professional_domains:
            return v  # Allow common professional emails
        
        # Suggest professional email if not using common provider
        if not any(prof in v.lower() for prof in ['dr.', 'doctor', 'medical']):
            raise ValueError("Consider using a professional email (e.g., dr.name@hospital.com)")
        
        return v

def verify_password(plain_password, hashed_password):
    # Hash the plain password with the same salt
    salted_password = plain_password + SALT
    hashed_input = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_input == hashed_password

def get_password_hash(password):
    # Hash password with salt
    if len(password) > 72:
        password = password[:72]
    salted_password = password + SALT
    return hashlib.sha256(salted_password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user_password(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        doctor_id: str = payload.get("sub")
        if doctor_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=401, detail="Doctor not found")
    
    return doctor

async def authenticate_doctor(email: str, password: str, db: Session):
    doctor = db.query(Doctor).filter(Doctor.email == email).first()
    if not doctor:
        return False
    if not verify_password(password, doctor.password_hash):
        return False
    return doctor
