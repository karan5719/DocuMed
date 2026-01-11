#!/usr/bin/env python3
"""
Medical Certificate System - Startup Script
"""

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    print("🏥 Starting DocuMed - Medical Certificate System")
    print(f"📍 Server will be available at: http://{host}:{port}")
    print(f"🔄 Auto-reload: {'enabled' if reload else 'disabled'}")
    print(f"🔐 Google OAuth: {'configured' if os.getenv('GOOGLE_CLIENT_ID') else 'not configured'}")
    print(f"🗄️  Database: {'configured' if os.getenv('DATABASE_URL') else 'not configured'}")
    print("\n" + "="*50)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
