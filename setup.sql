-- Medical Certificate System Database Setup
-- Run this script to create the database and initial setup

-- Create database (run this as root or with appropriate privileges)
CREATE DATABASE IF NOT EXISTS medical_certificates CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE medical_certificates;

-- Create doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    medical_registration_number VARCHAR(255),
    signature_path VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_google_id (google_id),
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- Create medical_certificates table
CREATE TABLE IF NOT EXISTS medical_certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    
    -- Candidate Details
    candidate_name VARCHAR(255) NOT NULL,
    identification_mark VARCHAR(255) NOT NULL,
    major_illness_operation BOOLEAN NOT NULL DEFAULT FALSE,
    major_illness_details TEXT,
    height_cm INT NOT NULL,
    weight_kg INT NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    
    -- Past History
    mental_illness BOOLEAN NOT NULL DEFAULT FALSE,
    mental_illness_details TEXT,
    epileptic_fits BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Medical Examination - Chest
    chest_inspiration_cm INT NOT NULL,
    chest_expiration_cm INT NOT NULL,
    
    -- Medical Examination - Hearing
    hearing_status VARCHAR(20) NOT NULL,
    
    -- Medical Examination - Vision
    vision_right_eye VARCHAR(20) NOT NULL,
    vision_left_eye VARCHAR(20) NOT NULL,
    
    -- Medical Examination - Systems Examination
    respiratory_system VARCHAR(20) NOT NULL,
    nervous_system VARCHAR(20) NOT NULL,
    
    -- Medical Examination - Heart
    heart_sounds VARCHAR(20) NOT NULL,
    heart_murmur VARCHAR(20) NOT NULL,
    
    -- Medical Examination - Abdomen
    liver_status VARCHAR(20) NOT NULL,
    spleen_status VARCHAR(20) NOT NULL,
    hydrocele_status VARCHAR(20) NOT NULL,
    
    -- Medical Examination - Other defects
    other_defects TEXT,
    
    -- Certificate of Medical Fitness
    medical_fitness_status VARCHAR(10) NOT NULL,
    
    -- Date of examination
    examination_date DATE NOT NULL,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    INDEX idx_doctor_id (doctor_id),
    INDEX idx_candidate_name (candidate_name),
    INDEX idx_examination_date (examination_date),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;

-- Create user for the application (optional, for better security)
-- CREATE USER IF NOT EXISTS 'medical_app'@'localhost' IDENTIFIED BY 'secure_password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON medical_certificates.* TO 'medical_app'@'localhost';
-- FLUSH PRIVILEGES;

-- Show the created tables
SHOW TABLES;
