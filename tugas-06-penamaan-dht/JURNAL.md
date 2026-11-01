# Jurnal Proses — Tugas 6

## Implementasi `find_successor`

- Kesalahan pertama yang ditemui: pada implementasi awal, fungsi `find_successor()` belum memiliki logika untuk mencari node dengan hash terkecil yang lebih besar atau sama dengan hash key serta belum menangani kondisi ketika hash key lebih besar dari seluruh ID node.
- Cara memperbaikinya: node diurutkan berdasarkan ID hash, kemudian dicari node pertama yang memiliki ID lebih besar atau sama dengan hash key. Jika tidak ditemukan, digunakan node dengan ID terkecil sebagai successor karena adanya mekanisme *wrap-around* pada ring.

## Skenario join/leave

- Hasil sebelum & sesudah node baru bergabung:
  - Kondisi awal ring memiliki node dengan ID `40`, `102`, `136`, dan `177`.
  - `kurir-012` memiliki hash `116` dan awalnya bertanggung jawab pada Node `136`.
  - Node baru `node-medan-1` dengan ID `123` bergabung ke ring.
  - Setelah node baru bergabung, `kurir-012` berpindah tanggung jawab dari Node `136` ke Node `123`.
  - Kurir lain yang tidak berada pada rentang yang terpengaruh tetap berada pada node sebelumnya.

- Hasil sebelum & sesudah node keluar:
  - Sebelum Node `177` keluar, `kurir-005` dengan hash `175` bertanggung jawab pada Node `177`.
  - Node `node-jakarta-1` dengan ID `177` kemudian keluar dari ring.
  - Setelah node tersebut keluar, tidak terdapat node dengan ID yang lebih besar atau sama dengan `175`, sehingga terjadi *wrap-around* ke Node `40`.
  - Dengan demikian, tanggung jawab `kurir-005` berpindah dari Node `177` ke Node `40`.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](https://github.com/aldonesia/komputasi-awan-dan-terdistribusi/blob/main/RUBRIK-UMUM.md).

| **Tanggal** | **Tool AI** | **Prompt yang diberikan** | **Ringkasan saran/ide AI** | **Bagaimana diolah jadi tulisan/kode sendiri** |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| 01-11-2026 | ChatGPT | Meminta penjelasan kode simulasi Chord DHT dan implementasi `lookup`, `join`, dan `leave`. | Membantu memahami konsep *consistent hashing*, *successor*, *ring topology*, serta perubahan tanggung jawab mapping ketika node bergabung atau keluar. | Konsep dipahami kemudian diterapkan pada skeleton yang diberikan. Program dijalankan dan diuji sendiri untuk memastikan hasil `lookup`, `join`, dan `leave` sesuai aturan Chord. |