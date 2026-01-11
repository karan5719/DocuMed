from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://username:password@localhost/medical_certificates")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    password_hash = Column(String(255), nullable=True)
    medical_registration_number = Column(String(255))
    signature_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    certificates = relationship("MedicalCertificate", back_populates="doctor")

class MedicalCertificate(Base):
    __tablename__ = "medical_certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    
    # Candidate Details
    candidate_name = Column(String(255), nullable=False)
    identification_mark = Column(String(255), nullable=False)
    major_illness_operation = Column(Boolean, nullable=False)
    major_illness_details = Column(Text, nullable=True)
    height_cm = Column(Integer, nullable=False)
    weight_kg = Column(Integer, nullable=False)
    blood_group = Column(String(10), nullable=False)
    
    # Past History
    mental_illness = Column(Boolean, nullable=False)
    mental_illness_details = Column(Text, nullable=True)
    epileptic_fits = Column(Boolean, nullable=False)
    
    # Medical Examination - Chest
    chest_inspiration_cm = Column(Integer, nullable=False)
    chest_expiration_cm = Column(Integer, nullable=False)
    
    # Medical Examination - Hearing
    hearing_status = Column(String(20), nullable=False)
    
    # Medical Examination - Vision
    vision_right_eye = Column(String(20), nullable=False)
    vision_left_eye = Column(String(20), nullable=False)
    
    # Medical Examination - Systems Examination
    respiratory_system = Column(String(20), nullable=False)
    nervous_system = Column(String(20), nullable=False)
    
    # Medical Examination - Heart
    heart_sounds = Column(String(20), nullable=False)
    heart_murmur = Column(String(20), nullable=False)
    
    # Medical Examination - Abdomen
    liver_status = Column(String(20), nullable=False)
    spleen_status = Column(String(20), nullable=False)
    hydrocele_status = Column(String(20), nullable=False)
    
    # Medical Examination - Other defects
    other_defects = Column(Text, nullable=True)
    
    # Certificate of Medical Fitness
    medical_fitness_status = Column(String(10), nullable=False)
    
    # Date of examination
    examination_date = Column(Date, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    doctor = relationship("Doctor", back_populates="certificates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
