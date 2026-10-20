import json
import re
import csv
from pathlib import Path

# Dosya yolları
DATA = Path(__file__).parents[1] / "datasets" / "events.jsonl"
CSV_OUT = Path(__file__).parent / "failed_events.csv"

# IPv4 biçimini doğrulayan Regex deseni (0-255 arasındaki 4 oktet)
IP_RE = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

def main():
    total_events = 0
    failed_events_list = []

    if not DATA.exists():
        print(f"Hata: {DATA} dosyası bulunamadı!")
        return

    # 1. events.jsonl dosyasını satır satır okuma
    with open(DATA, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            # 3. Hatalı Veri Kontrolü: JSON formatında olmayan satırları yakalama
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                print(f"Uyarı: Satır {line_num} geçersiz JSON formatında olduğundan atlandı.")
                continue

            total_events += 1

            # 2. Yalnızca status == 'FAILED' olan olayları filtreleme
            if event.get("status") == "FAILED":
                src_ip = str(event.get("src_ip", "")).strip()

                # Regex ile geçerli bir IP adresi olup olmadığını denetleme
                if IP_RE.match(src_ip):
                    failed_events_list.append({
                        "timestamp": event.get("timestamp", ""),
                        "event_id": event.get("event_id", ""),
                        "src_ip": src_ip,
                        "user": event.get("user", ""),
                        "status": event.get("status", "")
                    })

    # Sonuçları ekrana yazdırma
    print(f"Total events: {total_events}")
    print(f"Failed events: {len(failed_events_list)}")

    # 4. Filtrelenen verileri CSV dosyasına yazma
    fieldnames = ["timestamp", "event_id", "src_ip", "user", "status"]
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(failed_events_list)

    print(f"CSV oluşturuldu: {CSV_OUT.name}")

if __name__ == "__main__":
    main()