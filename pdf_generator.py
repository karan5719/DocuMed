from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from database_simple import MedicalCertificate, Doctor

def generate_certificate_pdf(certificate: MedicalCertificate, doctor: Doctor):
    from io import BytesIO
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    story = []
    
    # Title
    story.append(Paragraph("CERTIFICATE OF MEDICAL FITNESS", title_style))
    story.append(Spacer(1, 20))
    
    # Candidate Details Section
    story.append(Paragraph("1. CANDIDATE DETAILS", heading_style))
    
    candidate_data = [
        ["Name of the Candidate:", certificate.candidate_name],
        ["Identification Mark:", certificate.identification_mark],
        ["Major Illness/Operation:", "Yes" if certificate.major_illness_operation else "No"],
    ]
    
    if certificate.major_illness_operation and certificate.major_illness_details:
        candidate_data.append(["Nature of Illness/Operation:", certificate.major_illness_details])
    
    candidate_data.extend([
        ["Height:", f"{certificate.height_cm} cm"],
        ["Weight:", f"{certificate.weight_kg} kg"],
        ["Blood Group:", certificate.blood_group],
    ])
    
    candidate_table = Table(candidate_data, colWidths=[2.5*inch, 3*inch])
    candidate_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(candidate_table)
    story.append(Spacer(1, 12))
    
    # Past History Section
    story.append(Paragraph("2. PAST HISTORY", heading_style))
    
    past_history_data = [
        ["Mental Illness:", "Yes" if certificate.mental_illness else "No"],
    ]
    
    if certificate.mental_illness and certificate.mental_illness_details:
        past_history_data.append(["Details:", certificate.mental_illness_details])
    
    past_history_data.append(["Epileptic Fits:", "Yes" if certificate.epileptic_fits else "No"])
    
    past_history_table = Table(past_history_data, colWidths=[2.5*inch, 3*inch])
    past_history_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(past_history_table)
    story.append(Spacer(1, 12))
    
    # Medical Examination Section
    story.append(Paragraph("3. MEDICAL EXAMINATION", heading_style))
    
    # Chest
    story.append(Paragraph("Chest:", heading_style))
    chest_data = [
        ["Inspiration:", f"{certificate.chest_inspiration_cm} cm"],
        ["Expiration:", f"{certificate.chest_expiration_cm} cm"],
    ]
    
    chest_table = Table(chest_data, colWidths=[2.5*inch, 3*inch])
    chest_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(chest_table)
    story.append(Spacer(1, 8))
    
    # Hearing and Vision
    sensory_data = [
        ["Hearing:", certificate.hearing_status],
        ["Vision (Right Eye):", certificate.vision_right_eye],
        ["Vision (Left Eye):", certificate.vision_left_eye],
    ]
    
    sensory_table = Table(sensory_data, colWidths=[2.5*inch, 3*inch])
    sensory_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(sensory_table)
    story.append(Spacer(1, 8))
    
    # Systems Examination
    story.append(Paragraph("Systems Examination:", heading_style))
    systems_data = [
        ["Respiratory System:", certificate.respiratory_system],
        ["Nervous System:", certificate.nervous_system],
    ]
    
    systems_table = Table(systems_data, colWidths=[2.5*inch, 3*inch])
    systems_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(systems_table)
    story.append(Spacer(1, 8))
    
    # Heart
    story.append(Paragraph("Heart:", heading_style))
    heart_data = [
        ["Sounds:", certificate.heart_sounds],
        ["Murmur:", certificate.heart_murmur],
    ]
    
    heart_table = Table(heart_data, colWidths=[2.5*inch, 3*inch])
    heart_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(heart_table)
    story.append(Spacer(1, 8))
    
    # Abdomen
    story.append(Paragraph("Abdomen:", heading_style))
    abdomen_data = [
        ["Liver:", certificate.liver_status],
        ["Spleen:", certificate.spleen_status],
        ["Hydrocele:", certificate.hydrocele_status],
    ]
    
    abdomen_table = Table(abdomen_data, colWidths=[2.5*inch, 3*inch])
    abdomen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(abdomen_table)
    
    if certificate.other_defects:
        story.append(Spacer(1, 8))
        story.append(Paragraph("Any Other Defects:", heading_style))
        story.append(Paragraph(certificate.other_defects, normal_style))
    
    story.append(Spacer(1, 20))
    
    # Certificate of Medical Fitness
    story.append(Paragraph("4. CERTIFICATE OF MEDICAL FITNESS", heading_style))
    
    fitness_statement = f"The candidate fulfills the prescribed standard of physical fitness, medical fitness and is {certificate.medical_fitness_status} for admission to Engineering / Architecture / Pharmacy / Paramedical course."
    story.append(Paragraph(fitness_statement, normal_style))
    story.append(Spacer(1, 20))
    
    # Doctor's Details
    story.append(Paragraph("5. DOCTOR'S DETAILS", heading_style))
    
    doctor_data = [
        ["Name of the Doctor:", doctor.name],
        ["Google Email ID:", doctor.email],
        ["Medical Registration Number:", doctor.medical_registration_number or "Not Provided"],
        ["Date of Examination:", certificate.examination_date.strftime("%d/%m/%Y")],
    ]
    
    doctor_table = Table(doctor_data, colWidths=[2.5*inch, 3*inch])
    doctor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(doctor_table)
    story.append(Spacer(1, 40))
    
    # Signature line
    signature_data = [
        ["_________________________"],
        [f"Dr. {doctor.name}"],
        ["Signature & Seal"]
    ]
    
    signature_table = Table(signature_data, colWidths=[3*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (0, -1), 10),
        ('BOTTOMPADDING', (0, 0), (0, -1), 5),
    ]))
    
    story.append(signature_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
