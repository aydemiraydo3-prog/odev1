import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# En az 8 adet ve 3 farkli onem seviyesinde guvenlik olayi
EVENTS = [
    {"id": 1, "severity": "low", "type": "port-scan"},
    {"id": 2, "severity": "high", "type": "bruteforce"},
    {"id": 3, "severity": "medium", "type": "sql-injection-attempt"},
    {"id": 4, "severity": "low", "type": "ping-sweep"},
    {"id": 5, "severity": "high", "type": "malware"},
    {"id": 6, "severity": "medium", "type": "xss-probe"},
    {"id": 7, "severity": "low", "type": "failed-auth"},
    {"id": 8, "severity": "high", "type": "suspicious-login"}
]

class SecurityEventHandler(BaseHTTPRequestHandler):
    def _send_response_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        # 1. Endpoint: /api/events -> Tum olaylar
        if self.path == "/api/events":
            self._send_response_json(200, EVENTS)

        # 2. Endpoint: /api/events/high -> Yalnizca high severity olaylari
        elif self.path == "/api/events/high":
            high_events = [e for e in EVENTS if e.get("severity") == "high"]
            self._send_response_json(200, high_events)

        # 3. Endpoint: /api/summary -> Olaylarin ozet bilgisi
        elif self.path == "/api/summary":
            summary = {
                "total": len(EVENTS),
                "low": sum(1 for e in EVENTS if e.get("severity") == "low"),
                "medium": sum(1 for e in EVENTS if e.get("severity") == "medium"),
                "high": sum(1 for e in EVENTS if e.get("severity") == "high")
            }
            self._send_response_json(200, summary)

        # Gecersiz endpointler icin 404
        else:
            self._send_response_json(404, {"error": "Endpoint not found"})

    def log_message(self, format, *args):
        # Konsol ciktisini temiz tutmak icin
        print(f"[{self.log_date_time_string()}] {args[0]} -> {args[1]}")

def run(host="127.0.0.1", port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, SecurityEventHandler)
    print(f"Security Event API Server calisiyor: http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer durduruldu.")
        httpd.server_close()

if __name__ == "__main__":
    run()