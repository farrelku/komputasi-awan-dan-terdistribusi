# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Farrel Athallah | 103072400136 | Masalah desain  |
| Sugiwindarto | 103072400107 | The network is reliable |
| Hirelda Talahatu | 103072400028 | Single Point of Failure pada Arsitektur Monolitik |


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

## Pitfall 2: Masalah desain — ditulis oleh Farrel Athallah

**Bukti di skenario:** Skenario menyebutkan bahwa:

"satu server yang menangani semua modul"

dan ketika bermasalah:

"server backend kadang crash total dan perlu di-restart manual."

**Kenapa ini keliru:** Jika seluruh fungsi aplikasi bergantung pada satu server/proses, server tersebut menjadi Single Point of Failure (SPOF).

Ketika server mengalami overload atau crash, seluruh fungsi FoodGo ikut tidak tersedia. Tidak ada server alternatif yang dapat langsung mengambil alih pekerjaan

**Dampak ke FoodGo:** Ketika server mengalami overload saat promo besar:

Server overload -> proses backend crash -> Order tidak tersedia -> Payment tidak tersedia -> Notification tidak tersedia -> seluruh aplikasi terganggu.

Selain itu, restart manual membuat waktu pemulihan menjadi lebih lama dan meningkatkan downtime.

**Solusi desain awal:** FoodGo dapat menggunakan beberapa instance backend dan load balancer.

Arsitektur sederhananya:

User → Load Balancer → Server/Instance 1
** → Server/Instance 2**
** → Server/Instance 3**

Jika salah satu instance mengalami masalah, request dapat diarahkan ke instance lainnya.

Untuk tahap berikutnya, modul-modul yang memiliki kebutuhan scaling berbeda dapat dipisahkan menjadi service tersendiri

**Trade-off:** Menjalankan beberapa instance meningkatkan availability dan kemampuan menangani trafik, tetapi membutuhkan biaya infrastruktur dan sistem monitoring yang lebih besar. Selain itu, FoodGo harus memastikan data tetap konsisten ketika request diproses oleh beberapa instance

## Kesimpulan Kelompok

Kegagalan FoodGo bukan hanya disebabkan oleh kurangnya kapasitas server, tetapi juga oleh beberapa asumsi dan keputusan desain yang tidak sesuai dengan karakteristik sistem terdistribusi

Solusi juga tidak boleh hanya berupa "menambah server", karena setiap solusi memiliki trade-off. FoodGo perlu menyeimbangkan reliability, scalability, complexity, dan cost dalam menentukan arsitektur sistemnya
