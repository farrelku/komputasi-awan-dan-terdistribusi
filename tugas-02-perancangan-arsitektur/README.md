# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

## Kelompok

| Nama | NIM | Kontribusi |
|---|---|---|
| Farrel Athallah | 103072400136 | Perancangan Service Pesanan dan arsitektur |
| Sugiwindarto | 103072400107 | Perancangan komunikasi (sinkron/asinkron) |
| Hirelda Talahatu | 103072400028 | Perancangan Service Kurir/Notifikasi dan trade-off |

---

# Gaya Arsitektur yang Dipilih

**Gaya yang dipilih:** kombinasi **Service-Oriented Architecture (SOA)** dan **Publish-Subscribe**.

### Kenapa SOA?

Kebutuhan utama FoodGo adalah **decoupling deployment**. Service Pesanan, Pembayaran, Kurir/Notifikasi, dan Katalog Resto perlu dapat di-deploy dan di-scale secara terpisah.

Dengan pendekatan ini, ketika tim kurir melakukan perubahan pada Service Kurir/Notifikasi, Service Pesanan atau Service Katalog Resto tidak harus ikut di-restart seperti pada arsitektur monolitik.

### Kenapa Publish-Subscribe?

Komunikasi antara Service Pesanan dengan Resto dan Kurir bersifat **event-driven**. Service Pesanan tidak perlu mengetahui secara langsung siapa saja yang membutuhkan informasi pesanan.

Contohnya, ketika pesanan dibuat, Service Pesanan dapat menerbitkan event:

`OrderCreated`

Event tersebut kemudian diterima oleh service yang melakukan subscribe, seperti Service Katalog Resto dan Service Kurir/Notifikasi.

Dengan cara ini, coupling antara Service Pesanan dengan consumer dapat dikurangi.

### Kenapa Dikombinasikan?

SOA dan Publish-Subscribe digunakan untuk kebutuhan komunikasi yang berbeda.

- **SOA** digunakan untuk komunikasi yang membutuhkan respons langsung, seperti Service Pesanan dengan Service Pembayaran.
- **Publish-Subscribe** digunakan untuk komunikasi asinkron, seperti penyampaian informasi pesanan kepada Resto dan Kurir.

Dengan demikian, FoodGo dapat menggunakan komunikasi **sinkron** ketika membutuhkan kepastian hasil dan komunikasi **asinkron** ketika hanya perlu menyebarkan event kepada beberapa service.

---

# Komponen Arsitektur

| Komponen | Tanggung Jawab |
|---|---|
| **API Gateway** | Menjadi titik masuk permintaan pelanggan dan meneruskan request ke service yang sesuai. |
| **Service Pesanan** | Menerima dan mengelola pesanan pelanggan. |
| **Service Pembayaran** | Memproses pembayaran dan memberikan status pembayaran kepada Service Pesanan. |
| **Service Kurir/Notifikasi** | Menugaskan kurir serta mengirimkan notifikasi kepada resto, kurir, dan pelanggan. |
| **Service Katalog Resto** | Menyediakan informasi restoran/katalog dan menerima informasi pesanan baru melalui event. |
| **Message Broker** | Menjadi perantara komunikasi Publish-Subscribe untuk meneruskan event kepada service yang melakukan subscribe. |

---
## Skenario End-to-End

**Skenario:** Pelanggan membuat pesanan -> pembayaran diproses -> resto menerima notifikasi -> kurir ditugaskan.

| Langkah | Dari -> Ke | Jenis Komunikasi | Pola |
|---|---|---|---|
| **1** | Pelanggan -> API Gateway | Sinkron | Request-Response (HTTP) |
| **2** | API Gateway -> Service Pesanan | Sinkron | Request-Response |
| **3** | Service Pesanan -> Service Pembayaran | Sinkron | Request-Response (RPC) |
| **4** | Service Pembayaran -> Service Pesanan | Sinkron | Response (status bayar) |
| **5** | Service Pesanan -> Message Broker | Asinkron | Publish `OrderCreated` |
| **6** | Service Pembayaran -> Message Broker | Asinkron | Publish `PaymentCompleted` |
| **7** | Message Broker -> Service Katalog Resto | Asinkron | Subscribe `OrderCreated` / `PaymentCompleted` |
| **8** | Message Broker -> Service Kurir/Notifikasi | Asinkron | Subscribe `OrderCreated` / `PaymentCompleted` |

### Penjelasan Alur

- **Pelanggan** mengirim *request* pemesanan lewat aplikasi; diteruskan API Gateway ke Service Pesanan (sinkron, karena pelanggan menunggu konfirmasi pesanan diterima).
- **Service Pesanan** memanggil Service Pembayaran secara sinkron karena status pembayaran (berhasil/gagal) harus diketahui sebelum pesanan dikonfirmasi ke pelanggan.
- **Setelah status pembayaran diketahui**, Service Pesanan tidak memanggil Service Resto dan Service Kurir satu-satu. Ia cukup menerbitkan *event* `OrderCreated` (dan Service Pembayaran menerbitkan `PaymentCompleted`) ke Message Broker.
- **Service Katalog Resto** dan **Service Kurir/Notifikasi** masing-masing *subscribe* ke *event* tersebut secara independen. Resto memakainya untuk menyiapkan pesanan; Kurir/Notifikasi memakainya untuk menugaskan kurir dan mengirim notifikasi ke pelanggan/resto/kurir.
- **Karena bersifat asinkron**, Service Pesanan tidak perlu menunggu Resto atau Kurir selesai memproses — pesanan pelanggan sudah dianggap selesai dari sisi *request-response* begitu langkah 1–4 selesai.

---

## Analisis Coupling terhadap Tugas 1

Pada **Tugas 1**, semua modul berjalan dalam satu proses sehingga *deploy* salah satu modul membuat semua modul ikut *restart*, dan satu server menjadi *Single Point of Failure* (SPOF).

Dengan **SOA**, tiap *service* berjalan dan di-*deploy* terpisah, sehingga tim kurir dan tim resto bisa meng-update *service* masing-masing tanpa saling mengganggu.

Dengan **Publish-Subscribe**, Service Pesanan tidak perlu tahu siapa saja yang membutuhkan info pesanan — *service* baru bisa *subscribe* ke *event* tanpa mengubah Service Pesanan sama sekali. Beban atau kegagalan pada satu *service* (misalnya Resto *down*) juga tidak lagi ikut menjatuhkan *service* lain, karena setiap *service* punya proses dan *resource* sendiri.

---

## Trade-Off

| Kelebihan | Kekurangan / Kompleksitas Baru |
|---|---|
| Deployment & scaling tiap *service* independen | Sistem terdistribusi jauh lebih kompleks dibanding monolit |
| *Coupling* antar-*service* berkurang lewat *event* | Perlu infrastruktur tambahan: Message Broker (harus di-*manage*, dipantau, dan bisa jadi titik kegagalan baru) |
| *Service* baru bisa *subscribe event* tanpa mengubah Service Pesanan | Debugging lebih sulit karena alur tidak linear — melacak satu pesanan berarti menelusuri log di banyak *service* dan broker, bukan satu *call stack* |
| Kegagalan satu *service* (mis. Resto *down*) tidak langsung menjatuhkan *service* lain | Konsistensi data antar-*service* (mis. status pesanan di Service Pesanan vs status yang dilihat Resto) perlu ditangani eksplisit — berpotensi *eventual consistency*, bukan konsistensi langsung |
| Beban tinggi di satu *service* tidak membebani *service* lain | Butuh *observability* (*distributed tracing*, monitoring per-*service*) yang lebih matang; tanpa ini, gangguan justru lebih sulit dideteksi dibanding monolit |
| — | Perlu strategi tambahan untuk keandalan komunikasi (*retry*, *idempotency*) baik pada panggilan sinkron (Pesanan <-> Pembayaran) maupun asinkron (*publish/subscribe*), sesuai *pitfall* “network is reliable” dari Tugas 1 |

### Kesimpulan Trade-Off

Kompleksitas operasional (*deployment*, monitoring, debugging, konsistensi data) meningkat signifikan dibanding monolit. Kelompok menilai *trade-off* ini sepadan untuk FoodGo karena masalah utama di Tugas 1 (*downtime* total saat *deploy*, SPOF) berdampak langsung ke bisnis (pesanan gagal saat promo besar), sedangkan kompleksitas tambahan bisa dimitigasi bertahap dengan investasi pada *tooling* monitoring dan praktik desain (*retry*, *idempotency*, *event schema* yang jelas).

---

## Kesimpulan Kelompok

Arsitektur FoodGo diusulkan berubah dari satu aplikasi monolitik menjadi **kombinasi SOA** (untuk pemisahan fungsi inti: Pesanan, Pembayaran, Kurir/Notifikasi, Katalog Resto) dan **Publish-Subscribe** (untuk komunikasi *event* seperti `OrderCreated` dan `PaymentCompleted` lewat Message Broker).

Kombinasi ini dipilih karena karakteristik komunikasi FoodGo tidak seragam: sebagian butuh jawaban pasti dan langsung (pembayaran), sebagian bersifat notifikasi ke banyak pihak tanpa perlu ditunggu (resto dan kurir). Pendekatan ini secara langsung menjawab masalah *coupling* dan *single point of failure* dari Tugas 1, dengan konsekuensi kompleksitas operasional yang harus diimbangi dengan monitoring, *observability*, dan penanganan konsistensi data yang lebih matang.

