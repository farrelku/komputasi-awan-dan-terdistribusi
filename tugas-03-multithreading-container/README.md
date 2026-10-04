# Tugas 3 (Pekan 3) — Efisiensi Proses & Kontainer

**Materi terkait:** Threading, Virtualization, Containers.

---

## Tanpa Lock

### 1. Mengapa Race Condition Terjadi?
Ketika banyak thread berjalan secara konkuren dan mengakses variabel global/shared counter yang sama (misalnya `total_processed`) tanpa mekanisme sinkronisasi, operasi inkremen seperti `counter += 1` bukan merupakan operasi atomik. Akibatnya, beberapa thread dapat membaca dan mengubah nilai counter secara bersamaan sehingga pembaruan salah satu thread dapat tertimpa oleh threa lainnya.

### 2. Analisis Perbaikan
Menggunakan objek `threading.Lock()` untuk membungkus kode penambahan counter di dalam Critical Section.

### 3. Mengapa Menggunakan Threading
* **Penggunaan Memori Bersama**  
  Semua thread berjalan di dalam satu ruang memori yang sama. Variabel seperti `total_processed` dan objek `order_lock` secara alami dapat diakses langsung oleh semua thread. Hal ini memudahkan peragaan race condition dan pengujian fungsi sinkronisasi Lock.

* **Karakteristik Beban Kerja**  
  Simulasi pesanan biasanya melibatkan proses I/O-bound seperti jeda query database, jaringan, atau delay waktu. Untuk tugas berjenis I/O-bound, multithreading sangat efisien karena thread dapat berganti peran secara instan saat thread lain sedang menunggu I/O.

---

## Dengan Lock

Berdasarkan hasil percobaan:
* **Total pesanan terproses:** 100
* **Nilai ekspektasi (seharusnya):** 100

### 1. Analisis Race Condition
Tanpa adanya perlindungan, terjadi interleaving (tumpang-tindih eksekusi). Misalnya Thread A dan Thread B membaca nilai 0 secara bersamaan. Keduanya menghitung 0 + 1 = 1 dan menuliskan angka 1 ke memori. Hasilnya, dua pesanan diproses tetapi counter hanya bertambah 1 (1 transaksi hilang). Inilah yang menyebabkan hasil akhir sebelumnya drop secara drastis menjadi hanya 13 dari 100.

### 2. Analisis Perbaikan
Dengan memaksa urutan akses menjadi serial/terisolasi khusus pada bagian penambahan counter, setiap dari 100 transaksi dijamin menambah nilai persis +1 secara bersih. Hasilnya, counter konsisten mencapai 100/100 tanpa ada data yang tertimpa.

### 3. Alasan Menggunakan Threading
Semua thread berada dalam satu address space (ruang memori) yang sama. Variabel global `total_processed` dan objek `order_lock` dapat diakses langsung secara in-memory oleh seluruh thread.