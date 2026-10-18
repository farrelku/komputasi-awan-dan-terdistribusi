# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1–4: Implementasi dilakukan dengan melengkapi mekanisme election, pengiriman pesan antarnode, dan penentuan leader. Pengujian dilakukan untuk memastikan pemilihan leader berjalan sesuai mekanisme Bully Algorithm.Selain itu, saat proses dihentikan menggunakan Ctrl + C, traceback muncul di terminal.

- Hasil implementasi: Ketika semua node aktif, Node 5 menjadi leader dan tidak terjadi pergantian leader. Pergantian terjadi ketika leader atau node tertentu dihentikan.
## Skenario 1: Start normal
- Leader yang terpilih: Node 5.

- Log/observasi: Kelima node berhasil dijalankan. Pesan ELECTION, OK, dan PING muncul pada log. Node 5 menjadi leader dan tetap menjadi leader selama semua node aktif.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4 setelah Node 5 dihentikan.

- Waktu sampai leader baru terdeteksi: Beberapa saat setelah node yang lebih tinggi dimatikan (1-2 detik).

- Log/observasi: Setelah Node 5 dihentikan, Node 4 melakukan election dan menjadi leader berikutnya. Ketika node dengan ID tertinggi yang masih aktif dihentikan, pemilihan leader berlanjut ke node dengan ID tertinggi berikutnya, yaitu Node 3, Node 2, lalu Node 1.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 16/10/2026 | ChatGPT | "Analisis: konsep Bully Algorithm, alur pemilihan leader, dan skenario ketika node mengalami kegagalan sesuai dengan tugas 5." | Penjelasan mengenai proses election, komunikasi antarnode, penentuan leader berdasarkan ID tertinggi, dan respons sistem ketika leader tidak aktif. | Memahami konsep dan alur algoritma melalui brainstorming, kemudian mengembangkan analisis serta mengevaluasi perilaku program berdasarkan hasil pengujian sendiri. |