# Autor projekta
- Marko Šuljak, SW-35/2018

# Asistent
- Dragan Vidaković

# Definicija problema
- Zadatak projekta je detekcija lopte na video snimku (koji se beleži live preko kamere laptopa) i praćenje njene pozicije na snimku u real-time.

# Metodologija
- Sama detekcija pozicije lopte na frame-u video snimka biće realizovana uz pomoć procesuiranja slike. Ovaj proces podrazumeva pronalaženje granica lopte i njene boje korišćenjem OpenCV biblioteke. 
- Lokacija lopte na svakom od frame-ova biće beležena u listu kao torka koordinata lopte (x, y). Ovo je potrebno da bi mogli da vizualizujemo detekciju lokacije lopte po frame-ovima i prikazivanje "traga" (pozicije lopte u proteklim frame-ovima).

# Evaluacija 
- Evaluacija samih performansa softvera biće empirijska jer je jednostavno uočiti obeležene granice lopte na slici i liniju koja predstavlja njen trag. 

# Pokretanje aplikacije
- Parametar --video se koristi ako želimo prepoznavanje lopte na nekom već postojećem video snimu (ne na veb kameri). Vrednost koja se prosleđuje je putanja video snimka
- Parametar --buffer prestavlja veličinu dvostruko spregnute liste za pamćenje lokacija lopte po frame-ovima. Predefinisana vrednost ovog argumenta je 64.
- Potrebno je impotovati sve biblioteke koje aplikacija koristi.
