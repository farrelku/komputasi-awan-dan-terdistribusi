# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Farrel Athallah | 103072400136 | Masalah desain  |
| Sugiwindarto | 103072400107 | The network is reliable |


## Pitfall 1: The network is reliable — ditulis oleh Sugiwindarto

**Bukti di skenario:** Kode eksplisit menulis asumsi network is always reliable, no need for retry, dan tidak ada mekanisme retry saat modul pesanan memanggil modul pembayaran

**Kenapa ini keliru:** Jaringan nyata selalu punya kemungkinan gagal packet loss, koneksi terputus sementara, service sedang restart, DNS resolver bermasalah, dll. Kegagalan ini biasanya bersifat sementara, bukan permanen, sehingga sebenarnya bisa ditangani dengan retry tapi tim FoodGo mengasumsikan kegagalan tidak akan pernah terjadi sama sekali

**Dampak ke FoodGo:** Saat trafik melonjak, kemungkinan gangguan jaringan sesaat meningkat. Karena tidak ada retry, satu kegagalan kecil langsung menjadi error yang diteruskan ke user 

**Solusi desain awal:** Tambahkan retry dengan exponential backoff + jitter untuk panggilan antar service, dibatasi jumlah percobaan maksimum, dan hanya untuk operasi yang idempotent

**Trade-off:** Retry dapat membantu menangani gangguan jaringan sementara, tetapi retry yang terlalu banyak justru dapat menambah beban service yang sudah bermasalah. Oleh karena itu, retry harus memiliki batas jumlah percobaan dan menggunakan backoff

---

## Pitfall 2: Masalah desain — ditulis oleh Farrel Athallah

**Bukti di skenario:** Satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama

**Kenapa ini keliru:** tim FoodGo tampaknya berasumsi satu server bisa menangani beban gabungan dari semua modul tanpa batas. Dalam sistem terdistribusi nyata, resource (CPU, memori dll) selalu terbatas, dan desain monolitik menggabungkan blast radius semua modul jadi satu

**Dampak ke FoodGo:** Karena semua modul (pesanan, pembayaran, notifikasi kurir) berbagi proses dan resource yang sama, saat modul pembayaran mengalami lonjakan beban, ia menghabiskan CPU/memori/koneksi yang seharusnya dipakai modul lain. Akibatnya seluruh sistem termasuk fitur yang tidak berhubungan langsung seperti notifikasi kurir ikut lambat atau crash

**Solusi desain awal:** Pisahkan modul menjadi service service independen dengan resource allocation masing-masing, sehingga modul pembayaran yang overload tidak langsung menjatuhkan modul pesanan atau notifikasi

**Trade-off:** Memisahkan monolit menjadi beberapa service menambah kompleksitas operasional signifikan butuh service discovery, monitoring terdistribusi, deployment terpisah, dan justru menambah titik kegagalan jaringan baru, Ini bukan solusi gratis, tim harus siap dengan observability yang lebih matang sebelum migrasi ke arsitektur terpisah

## Kesimpulan Kelompok

Kegagalan FoodGo bukan hanya disebabkan oleh kurangnya kapasitas server, tetapi juga oleh beberapa asumsi dan keputusan desain yang tidak sesuai dengan karakteristik sistem terdistribusi

Solusi juga tidak boleh hanya berupa "menambah server", karena setiap solusi memiliki trade-off. FoodGo perlu menyeimbangkan reliability, scalability, complexity, dan cost dalam menentukan arsitektur sistemnya
