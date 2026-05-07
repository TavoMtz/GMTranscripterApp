from supabase import create_client, Client
from .config import settings

# Esta es la conexión oficial a tu proyecto GM-Transcripter
supabase: Client = create_client(settings.supabase_url, settings.supabase_key) 