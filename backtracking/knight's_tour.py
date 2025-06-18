import sys, random

# Penjelasan:
# Mendefinisikan ukuran papan catur (6x6) dan pergerakan kuda yang dimodifikasi.
# Alur berpikir:
# Ukuran papan dan pergerakan kuda diatur agar algoritma dapat berjalan pada papan 6x6 dengan langkah unik (±3, ±2) dan (±2, ±3).
BOARD_SIZE = 6

# Custom knight moves: (±3, ±2) and (±2, ±3)
"""
MOVES = [
    (3, 2), (3, -2), (-3, 2), (-3, -2),
    (2, 3), (2, -3), (-2, 3), (-2, -3)
]
"""

# Official knight moves: (±2, ±1) and (±1, ±2)

MOVES = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]


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

    # Print langkah yang sekarang
    # print(f"Langkah ke-{move_num + 1}: Kuda di posisi ke-({x}, {y})")

    # Jika semua kotak sudah dikunjungi, simpan jalur penjelajahan.
    if move_num == BOARD_SIZE * BOARD_SIZE - 1:
        print(f"==> Penjelajahan lengkap ditemukan! Menyimpan solusi ke-{len(all_tours)+1}. <==")
        all_tours.append((list(path), tree_size[0]))
        board[x][y] = -1
        path.pop()
        return
    
    moves = MOVES[:]
    random.shuffle(moves)

    # Coba semua kemungkinan langkah kuda.
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, board):
            # print(f"  Mencoba langkah ke ({nx}, {ny}) dari ({x}, {y})")
            knight_tour(nx, ny, move_num + 1, board, path, all_tours, tree_size, max_tours)
            # Jika sudah cukup penjelajahan ditemukan, hentikan pencarian.
            if len(all_tours) >= max_tours:
                board[x][y] = -1
                path.pop()
                return
        # else:
            # print(f"    Tidak valid: ({nx}, {ny}) dari ({x}, {y})")

    # Backtrack: kembalikan status papan dan jalur.
    # print(f"Kembali (backtrack) dari posisi ({x}, {y}), langkah ke-{move_num+1}")
    board[x][y] = -1
    path.pop()

# Penjelasan:
# Fungsi untuk mencetak urutan langkah penjelajahan kuda.
# Alur berpikir:
# Memudahkan visualisasi hasil penjelajahan dengan menampilkan urutan langkah secara terstruktur.
def print_tour_sequence(tour):
    print("Barisan penjelajahan (urutan langkah atau move-sequence):")
    for idx, (x, y) in enumerate(tour):
        print(f"m{idx+1}: ({x}, {y})", end='; ')
        print("")
    print("\n")

def print_tour_chess_board(tour):
    print("Penampilan urutan-urutan langkah dalam papan catur atau chess board: ")
    # Buat Papan Catur Kosong dulu
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # isi papan catur sama nomor langkahnya
    for move_number, (x, y) in enumerate(tour):
        board[x][y] = move_number + 1 # + 1 supaya langkah pertamanya itu 1, bukan 0
    # print papan caturnya
    for row in board:
        print(' '.join(f"{cell:2d}" for cell in row))
    print("")
        

# Penjelasan:
# Fungsi utama untuk menginisialisasi papan, mencoba penjelajahan dari beberapa posisi awal, dan menampilkan hasil.
# Alur berpikir:
# Mulai dari sudut-sudut papan untuk variasi solusi, lalu jika kurang dari 4 solusi, coba posisi lain.
def main():
    print("========== Knight's Tour Pada Papan Catur (Chess Board) 6x6 ==========")
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
        print(f"\nMencoba penjelajahan dari posisi awal: ({sx}, {sy}).")
        knight_tour(sx, sy, 0, board, path, all_tours, tree_size, max_tours=4)

    # Jika solusi kurang dari 4, coba posisi lain.
    if len(all_tours) < 4:
        for sx in range(BOARD_SIZE):
            for sy in range(BOARD_SIZE):
                if (sx, sy) not in randomized_start_positions:
                    if len(all_tours) >= 4:
                        break
                    print(f"\nMencoba penjelajahan dari posisi awal: ({sx}, {sy})")
                    knight_tour(sx, sy, 0, board, path, all_tours, tree_size, max_tours=4)

    # Tampilkan semua penjelajahan yang ditemukan.
    print("")
    for i, (tour, tour_tree_size) in enumerate(all_tours):
        print(f"Penjelajahan ke-{i+1}:")
        print_tour_chess_board(tour)
        print_tour_sequence(tour)
        print(f"Estimasi tree size saat barisan penjelajahan ke-{i+1} ditemukan: {tour_tree_size}\n")

    # Tampilkan statistik pencarian.
    print(f"Estimasi tree size (jumlah node pada pohon pencarian): {tree_size[0]}")
    print(f"Total penjelajahan yang ditemukan sejauh ini: {len(all_tours)}")
    print("")

# Penjelasan:
# Set recursion limit agar program tidak berhenti karena batas rekursi Python.
# Jalankan fungsi utama jika file dijalankan langsung.
if __name__ == "__main__":
    sys.setrecursionlimit(2147483647)
    main()