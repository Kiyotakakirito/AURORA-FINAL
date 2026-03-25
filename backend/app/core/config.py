from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application settings
    app_name: str = "AI Project Evaluation System"
    debug: bool = True
    version: str = "1.0.0"
    
    # Database settings
    # Local dev uses SQLite (no network needed).
    # For production, set DATABASE_URL in .env to the Supabase Session Pooler URL.
    database_url: str = "sqlite:///./aurora.db"
    
    # Supabase settings (for production / direct SDK use)
    supabase_url: Optional[str] = "https://malrtperngdlvelxvjvp.supabase.co"
    supabase_anon_key: Optional[str] = "sb_publishable_SpN7dip9SqLCKcfpYJtGNg_Swzo0Hp9"
    # Production DB URL (Supabase Session Pooler - IPv4 compatible, port 5432)
    # Set this in .env when deploying to a server that can reach Supabase:
    # DATABASE_URL=postgresql://postgres.malrtperngdlvelxvjvp:[PASS]@aws-0-XX.pooler.supabase.com:5432/postgres
    supabase_db_url: Optional[str] = None
    
    # AI API settings - ONLY OLLAMA (local AI)
    # External APIs disabled - using local Ollama only
    openai_api_key: Optional[str] = None  # Disabled - using Ollama
    anthropic_api_key: Optional[str] = None  # Disabled - using Ollama
    
    # Ollama settings - EXCLUSIVE AI PROVIDER
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3:latest"  # Default model - change if needed
    ollama_api_key: Optional[str] = None  # API key for hosted Ollama services
    use_ollama: bool = True  # ALWAYS True - Ollama is the ONLY AI provider

    # Force Ollama mode - no fallback to external APIs
    force_ollama_exclusive: bool = True  # Ensures ONLY Ollama is used
    
    # File upload settings
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    upload_dir: str = "uploads"
    
    # Evaluation settings
    default_code_weight: float = 0.7
    default_report_weight: float = 0.3
    
    # Scoring rubric defaults
    max_score: int = 100
    code_quality_weight: float = 0.3
    functionality_weight: float = 0.4
    documentation_weight: float = 0.2
    innovation_weight: float = 0.1
    
    class Config:
        env_file = ".env"

settings = Settings()
