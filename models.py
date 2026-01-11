from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from enum import Enum

class BloodGroupEnum(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class StatusEnum(str, Enum):
    NORMAL = "Normal"
    ABNORMAL = "Abnormal"

class HearingEnum(str, Enum):
    NORMAL = "Normal"
    ABNORMAL = "Abnormal"

class OrganStatusEnum(str, Enum):
    NORMAL = "Normal"
    ENLARGED = "Enlarged"

class MurmurEnum(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"

class HydroceleEnum(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"

class FitnessEnum(str, Enum):
    FIT = "FIT"
    UNFIT = "UNFIT"

class DoctorBase(BaseModel):
    email: EmailStr
    name: str
    medical_registration_number: str

class DoctorCreate(DoctorBase):
    google_id: str

class DoctorResponse(DoctorBase):
    id: int
    google_id: str
    signature_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class MedicalCertificateBase(BaseModel):
    # Candidate Details
    candidate_name: str
    identification_mark: str
    major_illness_operation: bool
    major_illness_details: Optional[str] = None
    height_cm: int
    weight_kg: int
    blood_group: BloodGroupEnum
    
    # Past History
    mental_illness: bool
    mental_illness_details: Optional[str] = None
    epileptic_fits: bool
    
    # Medical Examination - Chest
    chest_inspiration_cm: int
    chest_expiration_cm: int
    
    # Medical Examination - Hearing
    hearing_status: HearingEnum
    
    # Medical Examination - Vision
    vision_right_eye: str
    vision_left_eye: str
    
    # Medical Examination - Systems Examination
    respiratory_system: StatusEnum
    nervous_system: StatusEnum
    
    # Medical Examination - Heart
    heart_sounds: StatusEnum
    heart_murmur: MurmurEnum
    
    # Medical Examination - Abdomen
    liver_status: OrganStatusEnum
    spleen_status: OrganStatusEnum
    hydrocele_status: HydroceleEnum
    
    # Medical Examination - Other defects
    other_defects: Optional[str] = None
    
    # Certificate of Medical Fitness
    medical_fitness_status: FitnessEnum
    
    # Date of examination
    examination_date: date

class MedicalCertificateCreate(MedicalCertificateBase):
    pass

class MedicalCertificateResponse(MedicalCertificateBase):
    id: int
    doctor_id: int
    created_at: datetime
    doctor: DoctorResponse
    
    class Config:
        from_attributes = True

class CertificateSearch(BaseModel):
    candidate_name: Optional[str] = None
    examination_date: Optional[date] = None
