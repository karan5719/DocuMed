from fastapi import FastAPI, Request, Depends, HTTPException, Form, File, UploadFile, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date, datetime
import os
import uuid
from typing import Optional

from database_simple import get_db, create_tables, Doctor, MedicalCertificate
from models import (
    DoctorCreate, DoctorResponse, MedicalCertificateCreate, 
    MedicalCertificateResponse, CertificateSearch
)
from password_auth import LoginRequest, RegisterRequest, authenticate_doctor, get_current_user_password, get_password_hash
from pdf_generator import generate_certificate_pdf

app = FastAPI(title="DocuMed - Medical Certificate System")

# Add middleware
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SECRET_KEY", "medical_certificate_secret_key_2024")
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_submit(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    
    doctor = await authenticate_doctor(email, password, db)
    if not doctor:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid email or password"
        })
    
    access_token = create_access_token(data={"sub": str(doctor.id)})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_submit(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    name = form.get("name")
    medical_registration_number = form.get("medical_registration_number")
    
    # Validate using Pydantic model
    try:
        register_data = RegisterRequest(
            email=email,
            password=password,
            name=name,
            medical_registration_number=medical_registration_number
        )
    except ValueError as e:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": str(e)
        })
    
    # Check if doctor already exists
    existing_doctor = db.query(Doctor).filter(Doctor.email == email).first()
    if existing_doctor:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Email already registered"
        })
    
    # Create new doctor
    doctor = Doctor(
        email=email,
        name=name,
        password_hash=get_password_hash(password),
        medical_registration_number=medical_registration_number
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    
    access_token = create_access_token(data={"sub": str(doctor.id)})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, doctor: Doctor = Depends(get_current_user_password), db: Session = Depends(get_db)):
    certificates = db.query(MedicalCertificate).filter(MedicalCertificate.doctor_id == doctor.id).all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "certificates": certificates
    })

@app.get("/certificate/new", response_class=HTMLResponse)
async def new_certificate_form(request: Request, doctor: Doctor = Depends(get_current_user_password)):
    return templates.TemplateResponse("certificate_form.html", {
        "request": request,
        "doctor": doctor
    })

@app.post("/certificate/new")
async def create_certificate(
    request: Request,
    doctor: Doctor = Depends(get_current_user_password),
    db: Session = Depends(get_db),
    # Candidate Details
    candidate_name: str = Form(...),
    identification_mark: str = Form(...),
    major_illness_operation: bool = Form(False),
    major_illness_details: Optional[str] = Form(None),
    height_cm: int = Form(...),
    weight_kg: int = Form(...),
    blood_group: str = Form(...),
    # Past History
    mental_illness: bool = Form(False),
    mental_illness_details: Optional[str] = Form(None),
    epileptic_fits: bool = Form(False),
    # Medical Examination - Chest
    chest_inspiration_cm: int = Form(...),
    chest_expiration_cm: int = Form(...),
    # Medical Examination - Hearing
    hearing_status: str = Form(...),
    # Medical Examination - Vision
    vision_right_eye: str = Form(...),
    vision_left_eye: str = Form(...),
    # Medical Examination - Systems Examination
    respiratory_system: str = Form(...),
    nervous_system: str = Form(...),
    # Medical Examination - Heart
    heart_sounds: str = Form(...),
    heart_murmur: str = Form(...),
    # Medical Examination - Abdomen
    liver_status: str = Form(...),
    spleen_status: str = Form(...),
    hydrocele_status: str = Form(...),
    # Medical Examination - Other defects
    other_defects: Optional[str] = Form(None),
    # Certificate of Medical Fitness
    medical_fitness_status: str = Form(...),
    # Date of examination
    examination_date: date = Form(...)
):
    certificate_data = MedicalCertificateCreate(
        candidate_name=candidate_name,
        identification_mark=identification_mark,
        major_illness_operation=major_illness_operation,
        major_illness_details=major_illness_details,
        height_cm=height_cm,
        weight_kg=weight_kg,
        blood_group=blood_group,
        mental_illness=mental_illness,
        mental_illness_details=mental_illness_details,
        epileptic_fits=epileptic_fits,
        chest_inspiration_cm=chest_inspiration_cm,
        chest_expiration_cm=chest_expiration_cm,
        hearing_status=hearing_status,
        vision_right_eye=vision_right_eye,
        vision_left_eye=vision_left_eye,
        respiratory_system=respiratory_system,
        nervous_system=nervous_system,
        heart_sounds=heart_sounds,
        heart_murmur=heart_murmur,
        liver_status=liver_status,
        spleen_status=spleen_status,
        hydrocele_status=hydrocele_status,
        other_defects=other_defects,
        medical_fitness_status=medical_fitness_status,
        examination_date=examination_date
    )
    
    certificate = MedicalCertificate(
        doctor_id=doctor.id,
        **certificate_data.dict()
    )
    
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/certificate/{certificate_id}", response_class=HTMLResponse)
async def view_certificate(
    certificate_id: int,
    request: Request,
    doctor: Doctor = Depends(get_current_user_password),
    db: Session = Depends(get_db)
):
    certificate = db.query(MedicalCertificate).filter(
        MedicalCertificate.id == certificate_id,
        MedicalCertificate.doctor_id == doctor.id
    ).first()
    
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    return templates.TemplateResponse("certificate_view.html", {
        "request": request,
        "doctor": doctor,
        "certificate": certificate
    })

@app.get("/certificate/{certificate_id}/pdf")
async def download_certificate_pdf(
    certificate_id: int,
    doctor: Doctor = Depends(get_current_user_password),
    db: Session = Depends(get_db)
):
    certificate = db.query(MedicalCertificate).filter(
        MedicalCertificate.id == certificate_id,
        MedicalCertificate.doctor_id == doctor.id
    ).first()
    
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    pdf_bytes = generate_certificate_pdf(certificate, doctor)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=certificate_{certificate_id}.pdf"}
    )

@app.post("/search")
async def search_certificates(
    request: Request,
    doctor: Doctor = Depends(get_current_user_password),
    db: Session = Depends(get_db),
    candidate_name: Optional[str] = Form(None),
    examination_date: Optional[str] = Form(None)
):
    query = db.query(MedicalCertificate).filter(MedicalCertificate.doctor_id == doctor.id)
    
    if candidate_name:
        query = query.filter(MedicalCertificate.candidate_name.ilike(f"%{candidate_name}%"))
    
    if examination_date:
        try:
            search_date = datetime.strptime(examination_date, "%Y-%m-%d").date()
            query = query.filter(MedicalCertificate.examination_date == search_date)
        except ValueError:
            pass
    
    certificates = query.all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "doctor": doctor,
        "certificates": certificates,
        "search_candidate_name": candidate_name,
        "search_examination_date": examination_date
    })

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, doctor: Doctor = Depends(get_current_user_password)):
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "doctor": doctor
    })

@app.post("/profile")
async def update_profile(
    request: Request,
    doctor: Doctor = Depends(get_current_user_password),
    db: Session = Depends(get_db),
    name: str = Form(None),
    medical_registration_number: str = Form(None),
    google_id: str = Form(None),
    signature: Optional[UploadFile] = File(None)
):
    # Update editable fields
    if name:
        doctor.name = name
    
    if medical_registration_number:
        doctor.medical_registration_number = medical_registration_number
    
    if google_id:
        doctor.google_id = google_id
    
    if signature and signature.filename:
        # Save signature file
        signature_filename = f"signature_{doctor.id}_{uuid.uuid4()}.png"
        signature_path = f"static/signatures/{signature_filename}"
        
        os.makedirs(os.path.dirname(signature_path), exist_ok=True)
        
        with open(signature_path, "wb") as f:
            content = await signature.read()
            f.write(content)
        
        doctor.signature_path = signature_path
    
    db.commit()
    
    return RedirectResponse(url="/profile", status_code=302)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
