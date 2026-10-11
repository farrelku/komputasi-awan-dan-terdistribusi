# Jurnal Proses — Tugas 4

## Jalur yang dipilih
-  Jalur MQ, karena
komunikasi antara modul Pembayaran dan modul Kurir/Notifikasi tidak harus
berlangsung secara langsung atau menunggu respons dari modul lain.

## Kendala teknis
- Saat setup RabbitMQ menggunakan Docker, container sempat gagal berjalan karena
  konfigurasi `RABBITMQ_ERLANG_COOKIE` tidak valid sehingga muncul error
  `Too short cookie string`.
- Solusi yang dilakukan adalah menambahkan `RABBITMQ_ERLANG_COOKIE` dengan nilai
  yang cukup panjang pada `docker-compose.yml`, kemudian menjalankan ulang
  container menggunakan `docker compose down` dan `docker compose up -d`.
- Setelah konfigurasi diperbaiki, RabbitMQ berhasil berjalan dan dapat diakses
  melalui port `5672` untuk komunikasi AMQP dan `15672` untuk RabbitMQ Management.

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
