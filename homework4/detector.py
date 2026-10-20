# detector.py
from signatures import SQLI_PATTERNS, XSS_PATTERNS, TRAVERSAL_PATTERNS, SEVERITY_MAP

def detect_sqli(normalized_text):
    for pattern in SQLI_PATTERNS:
        if pattern in normalized_text:
            return True
    return False

def detect_xss(normalized_text):
    for pattern in XSS_PATTERNS:
        if pattern in normalized_text:
            return True
    return False

def detect_traversal(normalized_text):
    for pattern in TRAVERSAL_PATTERNS:
        if pattern in normalized_text:
            return True
    return False

def detect_attack(normalized_text):
    """
    Metinde saldiri olup olmadigini tespit eder.
    Saldiri varsa (saldiri_turu, severity) doner.
    Saldiri yoksa (None, None) doner.
    """
    if detect_sqli(normalized_text):
        return "SQL_INJECTION", SEVERITY_MAP["SQL_INJECTION"]
    
    if detect_xss(normalized_text):
        return "XSS", SEVERITY_MAP["XSS"]
    
    if detect_traversal(normalized_text):
        return "PATH_TRAVERSAL", SEVERITY_MAP["PATH_TRAVERSAL"]
    
    return None, None