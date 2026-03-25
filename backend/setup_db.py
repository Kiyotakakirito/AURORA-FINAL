"""
Run this script ONCE to create all tables in Supabase.
Usage: python setup_db.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import engine, Base
from app.models import models  # registers all models

print("Connecting to Supabase PostgreSQL...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
    print("Tables: projects, evaluations, evaluation_criteria")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
