import csv
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 5
CSV_OUT = Path(__file__).parent / "high_events.csv"

def fetch_events(endpoint="/api/events"):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={"User-Agent": "SecurityEventClient/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            status_code = response.getcode()
            if status_code == 200:
                data = json.loads(response.read().decode("utf-8"))
                return data
    except urllib.error.HTTPError as e:
        print(f"HTTP hatası: {e.code}")
    except urllib.error.URLError:
        print("API sunucusuna bağlanılamadı.")
    except TimeoutError:
        print("İstek zaman aşımına uğradı (Timeout).")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
    return None

def main():
    events = fetch_events("/api/events")
    if events is None:
        return

    print("API bağlantısı başarılı.")
    print(f"Toplam olay: {len(events)}")

    # Severity sayilari
    low_count = sum(1 for e in events if e.get("severity") == "low")
    med_count = sum(1 for e in events if e.get("severity") == "medium")
    high_count = sum(1 for e in events if e.get("severity") == "high")

    print("Severity dağılımı:")
    print(f"LOW    : {low_count}")
    print(f"MEDIUM : {med_count}")
    print(f"HIGH   : {high_count}")

    # Yalnizca HIGH olanlar
    high_events = [e for e in events if e.get("severity") == "high"]

    print("\nHIGH SEVERITY EVENTS")
    for ev in high_events:
        print(f"ID: {ev.get('id')}")
        print(f"Type: {ev.get('type')}")

    # high_events.csv kayit
    fieldnames = ["id", "severity", "type"]
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(high_events)

    print(f"\nSonuclar '{CSV_OUT.name}' dosyasina kaydedildi.")

if __name__ == "__main__":
    main()