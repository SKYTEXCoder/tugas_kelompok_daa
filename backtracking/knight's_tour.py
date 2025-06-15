import sys, random

# Penjelasan:
# Mendefinisikan ukuran papan catur (6x6) dan pergerakan kuda yang dimodifikasi.
# Alur berpikir:
# Ukuran papan dan pergerakan kuda diatur agar algoritma dapat berjalan pada papan 6x6 dengan langkah unik (±3, ±2) dan (±2, ±3).
BOARD_SIZE = 6

# Custom knight moves: (±3, ±2) and (±2, ±3)

MOVES = [
    (3, 2), (3, -2), (-3, 2), (-3, -2),
    (2, 3), (2, -3), (-2, 3), (-2, -3)
]


# Official knight moves: (±2, ±1) and (±1, ±2)
"""
MOVES = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]
"""

# Penjelasan:
# Fungsi untuk mengecek apakah posisi (x, y) valid dan belum pernah dikunjungi.
# Alur berpikir:
# Validasi posisi penting agar kuda tidak keluar papan dan tidak mengunjungi kotak yang sama dua kali.
def is_valid(x, y, board):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == -1

# Penjelasan:
# Fungsi rekursif utama untuk mencari semua kemungkinan penjelajahan kuda.
# Alur berpikir:
# Menggunakan backtracking untuk mencoba semua langkah dari posisi saat ini, menyimpan jalur, dan menghitung tree size.
def knight_tour(x, y, move_num, board, path, all_tours, tree_size, max_tours=4):
    tree_size[0] += 1
    board[x][y] = move_num
    path.append((x, y))

    # Jika semua kotak sudah dikunjungi, simpan jalur penjelajahan.
    if move_num == BOARD_SIZE * BOARD_SIZE - 1:
        all_tours.append(list(path))
        board[x][y] = -1
        path.pop()
        return
    
    moves = MOVES[:]
    random.shuffle(moves)

    # Coba semua kemungkinan langkah kuda.
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, board):
            knight_tour(nx, ny, move_num + 1, board, path, all_tours, tree_size, max_tours)
            # Jika sudah cukup penjelajahan ditemukan, hentikan pencarian.
            if len(all_tours) >= max_tours:
                board[x][y] = -1
                path.pop()
                return

    # Backtrack: kembalikan status papan dan jalur.
    board[x][y] = -1
    path.pop()

# Penjelasan:
# Fungsi untuk mencetak urutan langkah penjelajahan kuda.
# Alur berpikir:
# Memudahkan visualisasi hasil penjelajahan dengan menampilkan urutan langkah secara terstruktur.
def print_tour(tour):
    print("Barisan penjelajahan (urutan langkah):")
    for idx, (x, y) in enumerate(tour):
        print(f"m{idx+1}: ({x}, {y})", end='; ')
        print("")
    print("\n")

# Penjelasan:
# Fungsi utama untuk menginisialisasi papan, mencoba penjelajahan dari beberapa posisi awal, dan menampilkan hasil.
# Alur berpikir:
# Mulai dari sudut-sudut papan untuk variasi solusi, lalu jika kurang dari 4 solusi, coba posisi lain.
def main():
    print("")
    all_tours = []
    tree_size = [0]
    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    path = []

    # Mulai dari empat sudut papan.
    start_positions = [(0,0), (0,BOARD_SIZE-1), (BOARD_SIZE-1,0), (BOARD_SIZE-1,BOARD_SIZE-1)]
    randomized_start_positions = start_positions[:]
    random.shuffle(randomized_start_positions)
    for sx, sy in randomized_start_positions:
        if len(all_tours) >= 4:
            break
        print(f"Mencoba dari posisi awal: ({sx}, {sy}).")
        knight_tour(sx, sy, 0, board, path, all_tours, tree_size, max_tours=4)

    # Jika solusi kurang dari 4, coba posisi lain.
    if len(all_tours) < 4:
        for sx in range(BOARD_SIZE):
            for sy in range(BOARD_SIZE):
                if (sx, sy) not in randomized_start_positions:
                    if len(all_tours) >= 4:
                        break
                    print(f"Mencoba dari posisi awal: ({sx}, {sy}).")
                    knight_tour(sx, sy, 0, board, path, all_tours, tree_size, max_tours=4)

    # Tampilkan semua penjelajahan yang ditemukan.
    for i, tour in enumerate(all_tours):
        print(f"Penjelajahan ke-{i+1}:")
        print_tour(tour)

    # Tampilkan statistik pencarian.
    print(f"Estimasi tree size (jumlah node pada pohon pencarian): {tree_size[0]}")
    print(f"Total penjelajahan ditemukan: {len(all_tours)}")
    print("")

# Penjelasan:
# Set recursion limit agar program tidak berhenti karena batas rekursi Python.
# Jalankan fungsi utama jika file dijalankan langsung.
if __name__ == "__main__":
    sys.setrecursionlimit(2147483647)
    main()