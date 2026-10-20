# main.py
import csv
import json
from pathlib import Path
from normalizer import normalize
from detector import detect_attack

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "test_requests.json"
ALERTS_PATH = BASE_DIR / "alerts.csv"

def main():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            requests = json.load(f)
    except Exception as e:
        print(f"Hata: JSON verisi okunamadi: {e}")
        return

    alerts = []
    
    total_req = len(requests)
    allowed_count = 0
    blocked_count = 0
    sqli_count = 0
    xss_count = 0
    traversal_count = 0

    print("=== MINI WAF INCELEME SONUCLARI ===\n")

    for req in requests:
        # Eksik veya hatali alan kontrolu
        if not isinstance(req, dict):
            continue

        src_ip = req.get("src_ip", "UNKNOWN_IP")
        method = req.get("method", "UNKNOWN_METHOD")
        url = req.get("url", "")

        # Normalizasyon
        normalized_url = normalize(url)

        # Saldiri tespiti
        attack, severity = detect_attack(normalized_url)

        if attack is not None:
            action = "BLOCK"
            blocked_count += 1
            if attack == "SQL_INJECTION":
                sqli_count += 1
            elif attack == "XSS":
                xss_count += 1
            elif attack == "PATH_TRAVERSAL":
                traversal_count += 1

            alerts.append({
                "src_ip": src_ip,
                "method": method,
                "url": url,
                "attack": attack,
                "severity": severity,
                "action": action
            })

            print(f"IP       : {src_ip}")
            print(f"URL      : {url}")
            print(f"Attack   : {attack}")
            print(f"Severity : {severity}")
            print(f"Action   : {action}")
            print("-" * 35)
        else:
            action = "ALLOW"
            allowed_count += 1
            print(f"IP       : {src_ip}")
            print(f"URL      : {url if url else '(BOS URL)'}")
            print("Attack   : NONE")
            print("Severity : NONE")
            print(f"Action   : {action}")
            print("-" * 35)

    # alerts.csv dosyasina kaydetme
    fieldnames = ["src_ip", "method", "url", "attack", "severity", "action"]
    with open(ALERTS_PATH, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(alerts)

    # Ozet istatistik
    print("\n=== OZET ISTATISTIK ===")
    print(f"Toplam Request : {total_req}")
    print(f"Allowed        : {allowed_count}")
    print(f"Blocked        : {blocked_count}")
    print(f"SQL Injection  : {sqli_count}")
    print(f"XSS            : {xss_count}")
    print(f"Path Traversal : {traversal_count}")
    print(f"\nSaldiri loglari '{ALERTS_PATH.name}' dosyasina kaydedildi.")

if __name__ == "__main__":
    main()