# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Tugas Kelompok
Mengapa Membutuhkan Leader?

FoodGo membutuhkan leader untuk mengoordinasikan antrean pesanan agar pemrosesan lebih teratur dan mengurangi konflik. Jika leader mati, node lain melakukan election untuk memilih penggantinya.

### Mekanisme Bully Algorithm

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

Node dengan ID tertinggi yang masih hidup akan menjadi leader karena tidak ada node dengan ID lebih tinggi yang dapat mengambil alih pemilihan.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Hasil Pengujian

| No. | Skenario | Hasil Pengamatan |
|---:|---|---|
| 1 | Menjalankan Node 1–5 | Kelima proses berhasil dijalankan. |
| 2 | Mengamati komunikasi | Pesan `ELECTION`, `OK`, dan `PING` muncul pada log. |
| 3 | Semua node aktif | Node 5 menyatakan dirinya sebagai leader, tetapi pergantian leader berulang juga terlihat. |
| 4 | Node 5 dihentikan | Node 4 menjadi kandidat leader berikutnya. |
| 5 | Node 4 dihentikan | Node 3 menjadi kandidat leader berikutnya. |
| 6 | Node 3 dihentikan | Node 2 menjadi kandidat leader berikutnya. |
| 7 | Node 2 dihentikan | Node 1 menjadi kandidat leader berikutnya. |
| 8 | Menghentikan proses | Traceback muncul setelah proses dihentikan menggunakan `Ctrl + C`. |

## Trade-Off
Bully Algorithm relatif mudah diterapkan karena pemilihan leader didasarkan pada ID node tertinggi yang masih hidup. Namun, proses election dapat menghasilkan banyak pesan, terutama ketika beberapa node memulai election secara bersamaan.

Raft lebih kompleks karena menggunakan mekanisme konsensus dan replikasi log untuk menjaga konsistensi data. Oleh sebab itu, pemilihan algoritma perlu disesuaikan dengan kebutuhan sistem.

## Kesimpulan
Bully Algorithm memungkinkan FoodGo memilih leader pengganti berdasarkan ID node tertinggi yang masih hidup. Pengujian menunjukkan bahwa node dengan ID lebih rendah dapat menjadi kandidat leader ketika node ber-ID lebih tinggi dihentikan.

Namun, pergantian leader berulang ketika semua node aktif menunjukkan bahwa kestabilan implementasi masih perlu diperbaiki. Selain itu, konsistensi urutan pesanan tetap membutuhkan mekanisme tambahan karena pemilihan leader saja tidak menjamin urutan dan pemrosesan pesanan selalu konsisten.
