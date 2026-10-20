# signatures.py

# SQL Injection oruntuleri
SQLI_PATTERNS = [
    "or 1=1",
    "union select",
    "' or '1'='1",
    "sleep(",
    "drop table"
]

# XSS oruntuleri
XSS_PATTERNS = [
    "<script",
    "javascript:",
    "onerror=",
    "onload=",
    "<img src="
]

# Path Traversal oruntuleri
TRAVERSAL_PATTERNS = [
    "../",
    "..\\",
    "/etc/passwd",
    "c:\\windows"
]

# Saldiri turlerine gore severity seviyeleri
SEVERITY_MAP = {
    "SQL_INJECTION": "HIGH",
    "XSS": "HIGH",
    "PATH_TRAVERSAL": "MEDIUM"
}