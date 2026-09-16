# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [Tanggal diskusi 1]
- Peserta: Farrel Athallah, Sugiwindarto
- Poin diskusi: Mengidentifikasi masalah utama FoodGo dan Menentukan pitfall yang paling sesuai
- Perbedaan pendapat (jika ada): -

## [Tanggal diskusi 2]
- 15 September 2026

## Review Silang
- Farrel Athallah mengomentari analisis Sugiwindarto: Menurut saya, analisis Salman sudah cukup jelas dalam menghubungkan pitfall The network is reliable dengan kondisi FoodGo, terutama pada asumsi bahwa jaringan selalu dapat diandalkan dan tidak membutuhkan retry. Dampak yang dijelaskan juga sudah sesuai dengan skenario, yaitu ketika terjadi gangguan komunikasi, error dapat langsung diteruskan ke pengguna. Solusi berupa retry dengan exponential backoff dan jitter juga sudah tepat. Namun, menurut saya bagian dampaknya dapat diperjelas lagi dengan menghubungkannya dengan kondisi trafik tinggi, karena saat trafik meningkat, retry yang tidak dikontrol justru berpotensi memperbesar beban service yang sedang bermasalah

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 15 September 2026 | ChatGpt | Membantu memahami tugas tentang Fallacies of Distributed Computing pada studi kasus FoodGo dan menentukan poin poin yang perlu dianalisis. | AI memberikan beberapa ide pitfall yang dapat digunakan dan menyarankan kerangka pembahasan berupa asumsi, bukti pada skenario, dampak, solusi, dan trade off. | Kelompok menggunakan ide tersebut sebagai bahan awal, kemudian memilih pitfall yang paling sesuai dengan skenario. Analisis dan penjelasan akhir didiskusikan kembali oleh anggota kelompok dan ditulis menggunakan pemahaman kelompok. |
| 15 September 2026 | Claude | Meminta contoh cara menghubungkan pitfall sistem terdistribusi dengan gejala yang terjadi pada FoodGo. | AI memberikan gambaran hubungan antara tidak adanya timeout, request yang menunggu, dan penggunaan resource server. | Contoh hanya digunakan untuk membantu memahami hubungan sebab akibat. Kelompok mencocokkannya kembali dengan informasi pada soal dan menyusun penjelasan akhir sendiri. |