# Jurnal Proses — Tugas 2

## [27 September 2026]
- Opsi arsitektur yang dipertimbangkan: SOA murni, Publish-Subscribe murni, dan kombinasi keduanya 

- Kenapa akhirnya pilih SOA + Pub-Sub: SOA murni membuat Service Pesanan harus memanggil Resto dan Kurir satu-satu (coupling seperti Tugas 1). Pub-Sub murni tidak cocok untuk pembayaran karena butuh kepastian jawaban langsung. Kombinasi dipilih: SOA untuk Pesanan↔Pembayaran (sinkron), Pub-Sub untuk notifikasi ke Resto/Kurir lewat Message Broker (asinkron) 

- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): -

## Log Penggunaan AI (Level 2)


| Tanggal | Tool AI | Prompt yang Diberikan | Ringkasan Saran/Ide AI | Bagaimana Diolah Jadi Tulisan/Kode Sendiri |
|---|---|---|---|---|
| **25 September 2026** | ChatGPT | Meminta penjelasan perbedaan karakteristik SOA dan Publish-Subscribe, serta kapan masing-masing cocok dipakai pada sistem seperti FoodGo. | AI menjelaskan bahwa SOA cocok untuk komunikasi yang butuh jawaban pasti (request response), sedangkan Pub-Sub cocok untuk notifikasi ke banyak pihak yang tidak perlu ditunggu, dan menyarankan mempertimbangkan kombinasi keduanya jika kebutuhan komunikasi tidak seragam. | Penjelasan ini hanya dipakai sebagai bahan pemahaman konsep. Kelompok kemudian mendiskusikan sendiri komponen mana yang komunikasinya sinkron/asinkron pada kasus FoodGo, lalu menulis justifikasi pemilihan gaya arsitektur dengan kata-kata dan alasan sendiri. |
| **26 September 2026** | Claude | Meminta ide outline diagram alur end to end yang menunjukkan komponen mana saja yang perlu digambarkan agar sesuai instruksi tugas (minimal 4 komponen + gateway). | AI memberi gambaran umum urutan alur yang lazim sebagai kerangka awal, tanpa detail penomoran atau label jenis komunikasi. | Kerangka umum ini hanya jadi acuan urutan komponen. Kelompok sendiri yang menentukan penomoran langkah, label sinkron/asinkron, serta menyusun dan menggambar diagram akhir sesuai skenario FoodGo yang sudah dianalisis di Tugas 1. |
