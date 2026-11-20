# Jurnal Proses — Tugas 9

## Diskusi Deployment Model

Dalam diskusi kelompok, kami mempertimbangkan empat opsi deployment model, yaitu Public Cloud, Private Cloud, Hybrid Cloud, dan Community Cloud.

- **Public Cloud:** Memiliki keunggulan dalam skalabilitas elastis dan kemudahan pengelolaan *resource*. Namun, model ini kurang sesuai sebagai infrastruktur utama karena sistem menyimpan data kependudukan yang sangat sensitif dan pemerintah membutuhkan kendali penuh terhadap lokasi penyimpanan (*data sovereignty*) serta keamanan fisik server.

- **Private Cloud:** Menyediakan infrastruktur khusus yang dikelola dan dikendalikan sepenuhnya oleh pemerintah (baik *on-premise* maupun *hosted private cloud*). Model ini dinilai paling sesuai karena memberikan kontrol maksimal terhadap keamanan, audit akses, penyimpanan, dan kepatuhan terhadap regulasi perlindungan data pribadi warga negara.
  
- **Hybrid Cloud:** Menggabungkan *Private Cloud* dan *Public Cloud* sehingga memberikan fleksibilitas dan skalabilitas tinggi. Namun, terdapat peningkatan kompleksitas arsitektur, sinkronisasi data, serta potensi risiko keamanan apabila data sensitif berpindah antarlingkungan *cloud*.

- **Community Cloud:** Dapat digunakan bersama oleh beberapa instansi pemerintah yang memiliki kebutuhan dan standar keamanan serupa. Namun, diperlukan kesepakatan tata kelola (*governance*), pembagian biaya, dan manajemen hak akses lintas instansi yang kompleks.

**Keputusan kelompok:**

Setelah mempertimbangkan kelebihan dan kekurangan setiap model, kelompok kami memilih **Private Cloud** sebagai deployment model utama untuk Sistem Data Kependudukan. Alasannya adalah sistem mengelola data pribadi masyarakat seperti NIK, alamat, dan biometrik yang membutuhkan tingkat keamanan dan pengendalian tinggi.

Private Cloud juga tetap dapat mendukung skalabilitas melalui penambahan resource, load balancing, dan autoscaling ketika terjadi lonjakan akses, misalnya pada periode pemilu atau pendaftaran sekolah. Dengan demikian, kebutuhan kerahasiaan data dan ketersediaan layanan dapat diseimbangkan.

## Diskusi Service Model per Komponen

Dalam menentukan service model, kelompok kami mempertimbangkan kebutuhan pengelolaan, keamanan, dan fleksibilitas dari setiap komponen sistem.

1. **Database Data Kependudukan (IaaS)**

   Kami memilih Infrastructure as a Service (IaaS) untuk database utama karena pemerintah membutuhkan kendali yang tinggi terhadap server, sistem operasi, penyimpanan, dan konfigurasi database. Hal ini penting untuk menjaga keamanan data sensitif seperti NIK dan biometrik.

2. **Backend dan API Sistem  (PaaS)**

   Kami memilih Platform as a Service (PaaS) untuk pengembangan dan pengoperasian backend serta API. PaaS dapat mempermudah pengelolaan aplikasi, deployment, dan penyesuaian kapasitas layanan tanpa harus mengelola seluruh infrastruktur server secara langsung.

3. **Portal Layanan Instansi (SaaS)**

   Kami memilih Software as a Service (SaaS) untuk portal layanan yang digunakan oleh instansi seperti Dukcapil daerah, kepolisian, dan bank. Dengan model ini, instansi dapat menggunakan aplikasi yang telah disediakan pemerintah tanpa harus membangun dan mengelola aplikasi sendiri.

4. **Monitoring Infrastruktur (PaaS)**

   Kami memilih PaaS untuk mendukung pemantauan penggunaan resource seperti CPU, RAM, penyimpanan, dan jaringan. Monitoring ini diperlukan agar pemerintah dapat mengetahui kondisi infrastruktur dan mengantisipasi lonjakan akses maupun gangguan sistem.

**Kesimpulan diskusi:**

Penggunaan kombinasi IaaS, PaaS, dan SaaS dinilai lebih tepat karena setiap komponen memiliki kebutuhan pengelolaan yang berbeda. IaaS memberikan kendali terhadap infrastruktur inti, PaaS mempermudah pengelolaan aplikasi, sedangkan SaaS mempermudah instansi dalam menggunakan layanan kependudukan.

## Log Penggunaan AI (Level 2)

## Log Penggunaan AI (Brainstorming)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19-11-2026 | ChatGPT | Apa saja deployment model cloud computing dan kelebihan serta kekurangannya untuk sistem data kependudukan yang menyimpan data sensitif? | Memberikan gambaran perbandingan Public Cloud, Private Cloud, Hybrid Cloud, dan Community Cloud berdasarkan kebutuhan keamanan dan skalabilitas. | Kami menggunakan ide tersebut sebagai bahan diskusi kelompok, kemudian membandingkan setiap model berdasarkan kebutuhan sistem dan menentukan Private Cloud sebagai pilihan utama. |
| 19-11-2026 | ChatGPT | Service model apa yang cocok untuk database kependudukan, backend API, dan portal layanan instansi? | Memberikan ide penggunaan kombinasi IaaS, PaaS, dan SaaS sesuai fungsi setiap komponen sistem. | Kami mendiskusikan kembali pembagian service model berdasarkan kebutuhan pengelolaan infrastruktur dan layanan masing-masing komponen. |
