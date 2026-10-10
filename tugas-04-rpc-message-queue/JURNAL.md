# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [RPC / MQ / keduanya], alasan: ...
Kami memilih MQ (Message Queue), komunikasi antara modul Pembayaran dan modul Kurir/Notifikasi bersifat asinkron. Modul Pembayaran cukup mengirim event pembayaran_berhasil ke antrean RabbitMQ tanpa menunggu respons dari Kurir, sehingga pembayaran tetap responsif walau modul Kurir sedang down. 
Jika memakai RPC, Pembayaran harus menunggu balasan Kurir dan ikut lambat/error saat Kurir bermasalah.
## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...
-Tidak ada error saat setup. RabbitMQ berjalan via docker compose up -d (port 5672 dan 15672), dan publisher serta consumer terhubung ke localhost tanpa masalah.

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
Hasil yang diamati:
-Saat consumer mati: publisher mencetak 3 baris "Event terkirim" dan "Publisher selesai mengirim event." tanpa error, jadi pengirim tidak terblokir walau consumer tidak aktif (publish_mengirim.jpg).
-Di dashboard RabbitMQ: queue pembayaran_berhasil bertipe classic, berfitur Durable (D), berstatus running, dengan Ready = 3, Unacked = 0, Total = 3. Artinya ketiga pesan tersimpan di antrean dan belum diambil siapa pun (Bukti_Rabbit.jpg).
-Setelah consumer dinyalakan: consumer mencetak "Kurir menerima notifikasi pembayaran" untuk user1 (Rp20000), user2 (Rp40000), dan user3 (Rp60000), sesuai urutan pengiriman (consumer_nyala.jpg).
-Kesimpulan: tidak ada pesan yang hilang. Antrean menyimpan pesan selama consumer mati dan menyerahkannya setelah consumer aktif kembali. Ini membuktikan asynchronous decoupling: pengirim dan penerima tidak harus aktif bersamaan.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 9 Oktober 2026 | ChatGPT | Brainstorming ide awal untuk memahami pendekatan pengerjaan Tugas 4 tentang RPC dan Message Queue. | Memberikan gambaran awal mengenai pilihan jalur komunikasi dan konsep yang perlu dipahami. | Saran hanya digunakan sebagai brainstorming awal. Analisis, implementasi kode, pelaksanaan pengujian, pengamatan hasil, dan penulisan laporan dikerjakan sendiri oleh anggota kelompok. |
