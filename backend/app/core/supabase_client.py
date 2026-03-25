"""
Supabase client singleton — communicates over HTTPS (port 443).
Replaces the SQLAlchemy engine since port 5432 is unavailable locally.
"""
from supabase import create_client, Client
from .config import settings

_client: Client | None = None

def get_supabase() -> Client:
    """Return (and lazily create) the global Supabase client."""
    global _client
    if _client is None:
        url  = settings.supabase_url
        key  = settings.supabase_anon_key
        if not url or not key:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set in the environment."
            )
        _client = create_client(url, key)
    return _client
