"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Implementasi:
- Consistent hashing
- Ring topology
- Successor lookup
- Node join
- Node leave
- Mapping ID Kurir -> IP
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..255."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id -> alamat IP node
        self.nodes: dict[int, str] = {}

        # hash kurir -> (kurir_id, ip_kurir)
        self.data: dict[int, tuple[str, str]] = {}

    def join(self, node_name: str, node_ip: str):
        """
        Tambahkan node baru ke ring.

        Node baru mengambil tanggung jawab atas key yang sebelumnya
        menjadi tanggung jawab successor lama.
        """

        node_id = hash_id(node_name)

        # Cegah node dengan ID yang sama masuk dua kali
        if node_id in self.nodes:
            print(
                f"[JOIN] Node '{node_name}' sudah ada "
                f"(id={node_id})"
            )
            return

        # Cari successor sebelum node baru dimasukkan
        old_successor = None

        if self.nodes:
            old_successor = self.find_successor(node_id)

        # Tambahkan node baru ke ring
        self.nodes[node_id] = node_ip

        print(
            f"[JOIN] Node '{node_name}' bergabung "
            f"(id={node_id}, ip={node_ip})"
        )

        # Kalau ini node pertama, tidak ada data yang perlu dipindahkan
        if old_successor is None:
            return

        # Cari data yang sekarang menjadi tanggung jawab node baru
        moved_data = []

        for key_hash, (kurir_id, ip_kurir) in self.data.items():

            # Setelah node baru masuk, siapa successor key ini?
            new_owner = self.find_successor(key_hash)

            if new_owner == node_id:
                moved_data.append(
                    (key_hash, kurir_id, ip_kurir)
                )

        # Tampilkan data yang berpindah
        for key_hash, kurir_id, ip_kurir in moved_data:
            print(
                f"    [MOVE] {kurir_id} "
                f"(hash={key_hash}) "
                f"pindah tanggung jawab "
                f"dari node {old_successor} "
                f"ke node {node_id}"
            )

    def leave(self, node_name: str):
        """
        Keluarkan node dari ring.

        Data yang sebelumnya menjadi tanggung jawab node tersebut
        akan diambil alih oleh successor berikutnya.
        """

        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(
                f"[LEAVE] Node '{node_name}' "
                f"(id={node_id}) tidak ditemukan"
            )
            return

        # Cari data yang saat ini dimiliki node yang akan keluar
        affected_data = []

        for key_hash, (kurir_id, ip_kurir) in self.data.items():

            current_owner = self.find_successor(key_hash)

            if current_owner == node_id:
                affected_data.append(
                    (key_hash, kurir_id, ip_kurir)
                )

        # Hapus node dari ring
        del self.nodes[node_id]

        print(
            f"[LEAVE] Node '{node_name}' "
            f"(id={node_id}) keluar dari ring"
        )

        # Tentukan successor baru
        for key_hash, kurir_id, ip_kurir in affected_data:

            if self.nodes:
                new_owner = self.find_successor(key_hash)

                print(
                    f"    [MOVE] {kurir_id} "
                    f"(hash={key_hash}) "
                    f"pindah dari node {node_id} "
                    f"ke node {new_owner}"
                )
            else:
                print(
                    f"    [MOVE] {kurir_id} "
                    f"tidak memiliki node tujuan"
                )

    def find_successor(self, key_hash: int) -> int:
        """
        Cari node dengan ID hash terkecil yang >= key_hash.

        Jika tidak ada node yang memenuhi, lakukan wrap-around
        ke node dengan ID terkecil di ring.
        """

        if not self.nodes:
            raise ValueError("Ring belum memiliki node.")

        # Urutkan node berdasarkan hash
        sorted_nodes = sorted(self.nodes.keys())

        # Cari node pertama dengan ID >= hash key
        for node_id in sorted_nodes:
            if node_id >= key_hash:
                return node_id

        # Jika tidak ada, wrap-around ke node terkecil
        return sorted_nodes[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """
        Simpan mapping ID Kurir -> IP.

        Node penanggung jawab ditentukan menggunakan successor.
        """

        key_hash = hash_id(kurir_id)

        responsible_node = self.find_successor(key_hash)

        self.data[key_hash] = (
            kurir_id,
            ip_kurir
        )

        print(
            f"[REGISTER] {kurir_id} "
            f"(hash={key_hash}) -> {ip_kurir} "
            f"| node penanggung jawab={responsible_node}"
        )

    def lookup(self, kurir_id: str) -> str | None:
        """
        Cari alamat IP terkini berdasarkan ID Kurir.
        """

        key_hash = hash_id(kurir_id)

        # Cari node penanggung jawab
        responsible_node = self.find_successor(key_hash)

        # Cari data kurir
        data = self.data.get(key_hash)

        if data is None:
            print(
                f"[LOOKUP] {kurir_id} "
                f"(hash={key_hash}) tidak ditemukan"
            )
            return None

        kurir_id_data, ip_kurir = data

        print(
            f"[LOOKUP] {kurir_id_data} "
            f"(hash={key_hash}) "
            f"-> node {responsible_node} "
            f"-> {ip_kurir}"
        )

        return ip_kurir

    def print_ring(self):
        """Menampilkan node-node pada Chord Ring."""

        print("\n=== CHORD RING ===")

        if not self.nodes:
            print("(ring kosong)")
        else:
            for node_id in sorted(self.nodes.keys()):
                print(
                    f"Node ID {node_id} "
                    f"-> IP {self.nodes[node_id]}"
                )

        print("==================\n")


def main():

    ring = ChordRing()

    # ==========================================================
    # 1. NODE AWAL BERGABUNG
    # ==========================================================

    print("=== NODE AWAL BERGABUNG ===")

    ring.join(
        "node-jakarta-1",
        "10.0.0.1"
    )

    ring.join(
        "node-jakarta-2",
        "10.0.0.2"
    )

    ring.join(
        "node-bandung-1",
        "10.0.0.3"
    )

    ring.join(
        "node-surabaya-1",
        "10.0.0.4"
    )

    ring.print_ring()

    # ==========================================================
    # 2. REGISTER KURIR
    # ==========================================================

    print("=== REGISTER KURIR ===")

    ring.register_kurir(
        "kurir-001",
        "192.168.1.10"
    )

    ring.register_kurir(
        "kurir-002",
        "192.168.1.11"
    )

    ring.register_kurir(
        "kurir-003",
        "192.168.1.12"
    )

    # Kurir tambahan untuk membuktikan perpindahan mapping
    ring.register_kurir(
        "kurir-012",
        "192.168.1.13"
    )

    ring.register_kurir(
        "kurir-005",
        "192.168.1.14"
    )

    # ==========================================================
    # 3. LOOKUP SEBELUM PERUBAHAN TOPOLOGI
    # ==========================================================

    print("\n--- Lookup sebelum perubahan topologi ---")

    ring.lookup("kurir-001")
    ring.lookup("kurir-002")
    ring.lookup("kurir-003")
    ring.lookup("kurir-012")
    ring.lookup("kurir-005")

    # ==========================================================
    # 4. NODE BARU JOIN
    # ==========================================================

    print("\n--- Node baru bergabung ---")

    ring.join(
        "node-medan-1",
        "10.0.0.5"
    )

    ring.print_ring()

    # ==========================================================
    # 5. LOOKUP SETELAH JOIN
    # ==========================================================

    print("--- Lookup setelah JOIN ---")

    ring.lookup("kurir-001")
    ring.lookup("kurir-002")
    ring.lookup("kurir-003")
    ring.lookup("kurir-012")
    ring.lookup("kurir-005")

    # ==========================================================
    # 6. NODE LEAVE
    # ==========================================================

    print("\n--- Sebuah node keluar ---")

    ring.leave(
        "node-jakarta-1"
    )

    ring.print_ring()

    # ==========================================================
    # 7. LOOKUP SETELAH LEAVE
    # ==========================================================

    print("--- Lookup setelah LEAVE ---")

    ring.lookup("kurir-001")
    ring.lookup("kurir-002")
    ring.lookup("kurir-003")
    ring.lookup("kurir-012")
    ring.lookup("kurir-005")


if __name__ == "__main__":
    main()