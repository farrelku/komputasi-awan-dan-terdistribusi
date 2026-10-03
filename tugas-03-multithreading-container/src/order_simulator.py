import threading
import random
import time

NUM_ORDERS = 100
NUM_WORKERS = 10

processed_count = 0

# TODO 1:
# Untuk tahap pertama, Lock belum digunakan.
lock = threading.Lock()


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasikan kerja nyata
    time.sleep(random.uniform(0.001, 0.01))

    with lock:
        current = processed_count
        time.sleep(0.001)
        processed_count = current + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    global processed_count

    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 3:
    # Bagi order menjadi beberapa bagian
    chunk_size = len(order_ids) // NUM_WORKERS

    threads = []

    for i in range(NUM_WORKERS):
        start = i * chunk_size

        if i == NUM_WORKERS - 1:
            end = len(order_ids)
        else:
            end = start + chunk_size

        order_chunk = order_ids[start:end]

        t = threading.Thread(
            target=worker,
            args=(order_chunk,)
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")

    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!")


if __name__ == "__main__":
    main()