ödev2

Bu odevi events.jsonl dosyasindaki loglari okumak ve filtrelemek icin yaptim
Neler Yapildi
- jsonl dosyasini satir satir okuyup json loads ile dict yapisina cevirdim
- hatali json satiri gelirse program cokmesin diye try except blogu ekledim
- status degeri FAILED olanlari filtreledim
- ip adreslerinin dogrulugunu kontrol etmek icin regex kullandim, gecersiz ipleri eledim
- filtrelenen verileri failed_events.csv dosyasina kaydettim
