from pathlib import Path

LOG = Path(__file__).parents[1] / "datasets" / "auth.log"
if not LOG.exists():
    LOG = Path(__file__).parent / "datasets" / "auth.log"


def parse_line(line: str) -> dict:
    line = line.strip()
    if not line:
        return {}

    parts = line.split()
    log_data = {}

    # İlk parça doğrudan tarih/saattir (timestamp)
    if parts:
        log_data["timestamp"] = parts[0]

    # Kalan tüm key=value alanlarını sözlüğe ekle
    for item in parts[1:]:
        if "=" in item:
            key, value = item.split("=", 1)
            log_data[key] = value

    return log_data


def main():
    if not LOG.exists():
        print(f"Dosya bulunamadi: {LOG}")
        return

    success_count = 0
    failed_count = 0
    failed_ip_counts = {}

    with open(LOG, "r", encoding="utf-8") as file:
        for line in file:
            entry = parse_line(line)
            if not entry:
                continue

            status = entry.get("status")
            src_ip = entry.get("src_ip")

            if status == "SUCCESS":
                success_count += 1
            elif status == "FAILED":
                failed_count += 1
                if src_ip:
                    failed_ip_counts[src_ip] = failed_ip_counts.get(src_ip, 0) + 1

    print("SUCCESS sayisi:", success_count)
    print("FAILED sayisi:", failed_count)

    # En cok hata veren IP'yi bulma
    max_ip = None
    max_count = 0

    for ip, count in failed_ip_counts.items():
        if count > max_count:
            max_count = count
            max_ip = ip

    print("En cok hata ureten IP:", max_ip, "Hata sayisi:", max_count)


if __name__ == "__main__":
    main()