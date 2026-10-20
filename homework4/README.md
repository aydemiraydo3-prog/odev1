homework4

bu odevde gelen http isteklerini filtreleyip saldiri tespiti yapan kucuk bir waf mantigi kurdum

dosya yapisi
- signatures py icinde sqli xss ve path traversal kurallariyla severity derecelerini tanimladim
- normalizer py url decode kucuk harfe cevirme ve fazla bosluklari silme islemlerini yapiyor
- detector py normalize edilen istekte kurallari tarayip saldiri turunu ve severity degerini buluyor
- test requests json icinde hocanin istedigi normal ve saldiri iceren ornekleri tuttum
- main py json dosyasini okuyup tum istekleri analiz ediyor blocklananlari alerts csv ye yaziyor
- alerts csv sadece saldiri tespit edilip blocklanan kayitlari iceriyor

calistirma
terminalde homework4 klasorundeyken su komutla calistirdim
py main.py

detection mantigi
istek geliyor url decode ediliyor kucuk harfe cevrilip bosluklar teke indiriliyor ardindan kurallar taranip saldiri varsa allow ya da block karari veriliyor

severity secimi
- sql injection veri tabanina dogrudan erisim ve veri sizintisi tehlikesi yuzunden high
- xss kullanici tarafinda zararli kod calistirip oturum calabilme riski oldugundan high
- path traversal dosya sistemine yetkisiz erisim denemesi oldugundan medium olarak secildi

false positive calismasi
1. hangi request false positive olusturdu
search q SQL UNION SELECT tutorial istegi
2. hangi signature yakaladi
union select kurali yakaladi
3. kurali silmeden nasil azaltilabilir
sadece duz kelime aramasi yapmak yerine regex ile aralarda tirnak ozel karakter ya da sql yorum satiri var mi diye bakilabilir veya parametrenin arama kutusu mu yoksa id degeri mi olduguna gore kural esnetilebilir

test senaryolari
1. normal request products id 15 allow
2. sql injection products id 1 OR 1 1 block sql injection
3. encoded sql injection products id 1 27 20OR 201 3D1 block sql injection
4. xss search q script alert 1 script block xss
5. path traversal download file etc passwd block path traversal
ek olarak false positive adayi olan arama istegi de kural geregi basariyla blocklandi