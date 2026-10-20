homework3

bu odevde server ve client haberlesmesini gosteren mini bir api yaptim

neler yapildi
- server py icinde dahili kutuphanelerle calisan 8 guvenlik olayini tutan bir sunucu olusturdum
- api events api events high ve api summary endpointlerini ekledim
- olmayan sayfalar icin 404 kodu ve json hata mesaji dondurdum
- client py ile servera get istegi atip verileri cektim severity sayilarini hesapladim
- high olan olaylari high events csv dosyasina yazdirdim
- server kapali oldugunda program cokmesin diye try except ve timeout kullandim

calistirma
terminalde once serveri baslatiyoruz
py homework3/server.py

server acikken yeni bir terminal acip clienti calistiriyoruz
py homework3/client.py

cikti
API bağlantısı başarılı.
Toplam olay: 8
Severity dağılımı:
LOW    : 3
MEDIUM : 2
HIGH   : 3

HIGH SEVERITY EVENTS
ID: 2
Type: bruteforce
ID: 5
Type: malware
ID: 8
Type: suspicious-login

Sonuclar 'high_events.csv' dosyasina kaydedildi.