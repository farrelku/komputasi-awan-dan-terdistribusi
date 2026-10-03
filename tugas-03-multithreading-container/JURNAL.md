# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: `13` (seharusnya `100` pesanan)[cite: 1]
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): 
  Melesetnya angka counter terjadi karena banyak thread mencoba membaca dan mengubah variabel global `total_processed` secara bersamaan tanpa adanya penguncian. Operasi `counter += 1` terdiri dari tiga tahap instruksi (Read-Modify-Write). Karena tidak ada sinkronisasi, terjadi tumpang-tindih (*interleaving*) di mana beberapa thread membaca nilai variabel yang sama sebelum thread lain sempat menuliskan hasil perbaruannya. Akibatnya, nilai perubahan tertimpa (*lost updates*) dan transaksi yang terhitung hanya sebagian kecil dari total pesanan.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: `100` (seharusnya `100` pesanan)[cite: 2]

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: 
  - **Error WSL / Docker Engine**: Saat menjalankan Docker Desktop di Windows, muncul error `Docker daemon is not running` atau `WSL 2 installation is incomplete`.
  - **Penyebab**: Docker Desktop membutuhkan lingkungan Linux (*kernel*) melalui WSL 2 untuk menjalankan container berbasis Linux di OS Windows.
  - **Cara Memperbaiki**: 
    1. Menginstal distro Ubuntu di Windows dengan menjalankan perintah `wsl --install -d Ubuntu` di Command Prompt/PowerShell.
    2. Melakukan *restart* laptop dan mengaktifkan fitur *Virtualization* di BIOS serta fitur *Windows Subsystem for Linux* di Windows Features.
    3. Membuka settings Docker Desktop > **Resources** > **WSL Integration**, lalu mengaktifkan centang pada distro **Ubuntu**.
  - **Hasil**: Setelah integrasi WSL 2 dan Ubuntu selesai, Docker Desktop dapat berjalan dengan status *Engine Running*, serta perintah `docker build -t order-simulator .` dan `docker run order-simulator` berhasil mengeksekusi program di dalam container dengan lancar.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 03/10/2026 | Gemini | "Analisis: race condition, perbaikan, kenapa threading (bukan multiprocessing/proses OS)" | Penjelasan konsep Read Modify Write pada race condition, cara kerja threading.Lock(), dan keunggulan shared memory pada threading untuk tugas I/O-bound. | Memahami alur lost update secara konsep, kemudian menyusun uraian analisis race condition dan argumentasi arsitektur dengan gaya bahasa dan penalaran sendiri di jurnal. |