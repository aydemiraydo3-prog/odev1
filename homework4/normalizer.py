# normalizer.py
import re
from urllib.parse import unquote

def normalize(value):
    """
    Girdiyi URL decode eder, kucuk harfe cevirir ve
    ardisik gereksiz bosluklari tek bosluga indirir.
    """
    if not isinstance(value, str):
        return ""
    
    # URL decode islemi
    decoded = unquote(value)
    
    # Kucuk harfe cevirme
    lowered = decoded.lower()
    
    # Fazla bosluklari temizleme (or 1=1 ile or    1=1 ayni olsun diye)
    cleaned = re.sub(r"\s+", " ", lowered).strip()
    
    return cleaned