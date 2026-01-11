# DocuMed - Medical Certificate System

A professional web application for creating, managing, and storing medical certificates with Google OAuth authentication for doctors.

## Features

- **Secure Authentication**: Google OAuth integration for doctor login
- **Complete Medical Forms**: All mandatory fields following official medical examination format
- **Database Storage**: MySQL backend for reliable data storage
- **Search Functionality**: Find certificates by candidate name or examination date
- **PDF Generation**: Download professional printable certificates
- **Professional UI**: Hospital-grade interface design
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Google OAuth 2.0
- **PDF Generation**: ReportLab
- **Styling**: Bootstrap 5 + Custom CSS

## Installation

### Prerequisites

- Python 3.8+
- MySQL Server
- Google OAuth credentials

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd medical-certificate-system
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   DATABASE_URL=mysql+pymysql://username:password@localhost/medical_certificates
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   SECRET_KEY=your_secret_key_here
   ```

4. **Create MySQL database**:
   ```sql
   CREATE DATABASE medical_certificates;
   ```

5. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:8000`

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API and Google OAuth2 API
4. Create OAuth 2.0 Client ID
5. Add authorized redirect URI: `http://localhost:8000/auth`
6. Copy Client ID and Client Secret to your `.env` file

## Database Schema

### Doctors Table
- `id` - Primary key
- `google_id` - Google account ID
- `email` - Doctor's email
- `name` - Doctor's name
- `medical_registration_number` - Professional registration number
- `signature_path` - Path to digital signature file
- `created_at` - Account creation timestamp

### Medical Certificates Table
- All medical examination fields as specified in requirements
- `doctor_id` - Foreign key to doctors table
- `examination_date` - Date of medical examination
- `created_at` - Certificate creation timestamp

## Form Sections

The medical certificate form includes all mandatory sections:

1. **Candidate Details**
   - Name, identification mark, major illness history
   - Physical measurements (height, weight, blood group)

2. **Past History**
   - Mental illness history
   - Epileptic fits history

3. **Medical Examination**
   - Chest measurements (inspiration/expiration)
   - Hearing and vision assessment
   - Systems examination (respiratory, nervous)
   - Heart examination (sounds, murmur)
   - Abdominal examination (liver, spleen, hydrocele)
   - Other defects

4. **Certificate of Medical Fitness**
   - Fitness status (FIT/UNFIT)
   - Official statement
   - Examination date

5. **Doctor's Details**
   - Auto-filled from Google profile
   - Medical registration number
   - Digital signature

## API Endpoints

- `GET /` - Home page
- `GET /login` - Google OAuth login
- `GET /auth` - OAuth callback
- `GET /dashboard` - Doctor dashboard
- `GET /certificate/new` - New certificate form
- `POST /certificate/new` - Create certificate
- `GET /certificate/{id}` - View certificate
- `GET /certificate/{id}/pdf` - Download PDF
- `POST /search` - Search certificates
- `GET /profile` - Doctor profile
- `POST /profile` - Update profile
- `GET /logout` - Logout

## Usage

1. **Login**: Click "Login with Google" and authenticate with your Google account
2. **Complete Profile**: Add your medical registration number and optional signature
3. **Create Certificate**: Fill in the comprehensive medical examination form
4. **Manage Certificates**: View, search, and download certificates from dashboard
5. **Generate PDF**: Download professional printable certificates

## Security Features

- Google OAuth 2.0 authentication
- JWT token-based session management
- Secure cookie handling
- Input validation and sanitization
- Database connection security

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
The application automatically creates tables on startup using SQLAlchemy.

### Adding New Features
- Backend logic in `main.py`
- Database models in `database.py` and `models.py`
- Frontend templates in `templates/` directory
- Static files in `static/` directory

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.

---

**Note**: This application is designed for professional medical use and should comply with all relevant medical and data protection regulations in your jurisdiction.
