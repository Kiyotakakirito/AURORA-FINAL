from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
import os
import sys

# Add evaluation_engine to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import settings
from app.core.database import get_db, engine
from app.models import models
from app.api.router import router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Project Evaluation System",
    description="Automated evaluation system for student projects",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Serve static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/test-endpoint")
async def test_endpoint():
    print("TEST ENDPOINT CALLED!!!")
    return {"message": "Backend is working!", "status": "ok"}

@app.get("/")
async def root():
    return {"message": "AI Project Evaluation System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
