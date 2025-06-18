import sys, random
from PIL import Image, ImageDraw
import os

# Penjelasan:
# Mendefinisikan ukuran papan catur (6x6) dan pergerakan kuda yang dimodifikasi.
# Alur berpikir:
# Ukuran papan dan pergerakan kuda diatur agar algoritma dapat berjalan pada papan 6x6 dengan langkah unik (±3, ±2) dan (±2, ±3).
BOARD_SIZE = 6
SQUARE_SIZE = 80

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
def knight_tour(x, y, move_num, board, path, all_tours, tree_size, possible_moves_counts, max_tours=4):
    tree_size[0] += 1
    board[x][y] = move_num
    path.append((x, y))
    possible_moves_counts.append(count_possible_moves(x, y, board))

    # Print langkah yang sekarang
    # print(f"Langkah ke-{move_num + 1}: Kuda di posisi ke-({x}, {y})")

    # Jika semua kotak sudah dikunjungi, simpan jalur penjelajahan.
    if move_num == BOARD_SIZE * BOARD_SIZE - 1:
        print(f"=====> Penjelajahan lengkap ditemukan! Menyimpan solusi ke-{len(all_tours)+1}. <=====")
        if path not in [t[0] for t in all_tours]:
            all_tours.append((list(path), tree_size[0], list(possible_moves_counts)))
        board[x][y] = -1
        path.pop()
        possible_moves_counts.pop()
        return
    
    # moves = MOVES[:]
    # random.shuffle(moves)

    # Coba semua kemungkinan langkah kuda.
    # Jika ingin lebih random lagi, ganti for loop di bawah ini untuk mengiterasikan
    # moves (variabel bertipe list[tuple[int, int]]yang merupakan copy dari MOVES 
    # yang sudah dirandomisasi) dan bukan MOVES (yang merupakan constant yang sudah didefinisi di atas)
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, board):
            # print(f"  Mencoba langkah ke ({nx}, {ny}) dari ({x}, {y})")
            knight_tour(nx, ny, move_num + 1, board, path, all_tours, tree_size, possible_moves_counts, max_tours)
            # Jika sudah cukup penjelajahan ditemukan, hentikan pencarian.
            if len(all_tours) >= max_tours:
                board[x][y] = -1
                path.pop()
                possible_moves_counts.pop()
                return
        # else:
            # print(f"    Tidak valid: ({nx}, {ny}) dari ({x}, {y})")

    # Backtrack: kembalikan status papan dan jalur.
    # print(f"Kembali (backtrack) dari posisi ({x}, {y}), langkah ke-{move_num+1}")
    board[x][y] = -1
    path.pop()
    possible_moves_counts.pop()

# Penjelasan:
# Fungsi untuk mencetak urutan langkah penjelajahan kuda.
# Alur berpikir:
# Memudahkan visualisasi hasil penjelajahan dengan menampilkan urutan langkah secara terstruktur.
def print_tour_sequence(tour):
    print("Barisan penjelajahan (urutan langkah atau move-sequence):")
    for idx, (x, y) in enumerate(tour):
        print(f"Langkah ke-{idx+1}: ({x}, {y})", end='; ')
        print("")
    print("\n")

# Untuk menampilkan status dari setiap kotak di papan caturnya setelah menemukan 4 barisan penjelajahan, status di sini merupakan "kudanya menempatkan kotak ini di langkah ke berapa"
def print_tour_chess_board(tour):
    print("Penampilan urutan-urutan langkah dalam layout papan catur atau chess board: ")
    # Buat Papan Catur Kosong dulu
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # isi papan catur sama nomor langkahnya
    for move_number, (x, y) in enumerate(tour):
        board[x][y] = move_number + 1 # + 1 supaya langkah pertamanya itu 1, bukan 0
    # print papan caturnya
    for y in range(BOARD_SIZE):
        print(' '.join(f"{board[x][y]:2d}" for x in range(BOARD_SIZE)))
    print("")
 
# generate tampilan dari setiap frame/langkah
def draw_tour_frame(draw, tour, step):
    light = (238, 238, 210)
    dark = (118, 150, 86)
    knight_color = (255, 0, 0)
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            color = light if (x + y) % 2 == 0 else dark
            draw.rectangle(
                [x * SQUARE_SIZE, y * SQUARE_SIZE, (x+1) * SQUARE_SIZE, (y+1) * SQUARE_SIZE],
                fill=color
            )
    for i in range(step + 1):
        x, y = tour[i]
        cx = x * SQUARE_SIZE + SQUARE_SIZE // 2
        cy = y * SQUARE_SIZE + SQUARE_SIZE // 2
        draw.ellipse(
            [cx - 15, cy - 15, cx + 15, cy + 15],
            fill=knight_color
        )
        draw.text((cx - 5, cy - 8), str(i+1), fill=(255, 255, 255))

# membuat gif perjalanan kuda
def generate_gif(tour, filename):
    frames = []
    for step in range(len(tour)):
        img = Image.new("RGB", (BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
        draw = ImageDraw.Draw(img)
        draw_tour_frame(draw, tour, step)
        frames.append(img)
    frames[0].save(filename, save_all=True, append_images=frames[1:], duration=300, loop=0)

    # nyimpen gambar terakhir gif sebagai hasil akhir
    final_frame_path = filename.replace(".gif", "_final.png")
    frames[-1].save(final_frame_path)
    print(f"Gambar akhir disimpan sebagai '{final_frame_path}'")
    
    
# Untuk menampilkan perhitungan m-nya
def print_m_sequence(possible_moves_counts):
    print("m-sequence (jumlah kemungkinan langkah dari setiap posisi pada tour):")
    print('[', end='')
    print(' '.join(str(m) for m in possible_moves_counts), end='')
    print("]\n")
    
# Untuk menghitung m-m nya
def count_possible_moves(x, y, board):
    count = 0
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, board):
            count += 1
    return count

def estimate_tree_size_from_m_sequence(m_sequence):
    total = 1
    prod = 1
    for m in m_sequence:
        prod *= m
        total += prod
    return total
        
# Penjelasan:
# Fungsi utama untuk menginisialisasi papan, mencoba penjelajahan dari beberapa posisi awal, dan menampilkan hasil.
# Alur berpikir:
# Mulai dari sudut-sudut papan untuk variasi solusi, lalu jika kurang dari 4 solusi, coba posisi lain.
def main():
    print("========== Knight's Tour Pada Papan Catur (Chess Board) Berukuran 6x6 ==========")
    all_tours = []
    tree_size = [0]
    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    path = []
    estimated_tree_sizes = []

    # Mulai dari empat sudut papan.
    # (0,0), (0, 5), (5, 0), (5, 5)
    start_positions = [(0,0), (0,BOARD_SIZE-1), (BOARD_SIZE-1,0), (BOARD_SIZE-1,BOARD_SIZE-1)]
    randomized_start_positions = start_positions[:]
    
    random.shuffle(randomized_start_positions)
    ## jika ingin titik mulai pojoknya untuk dibuat random (urutannya), 
    ## GANTI for loop di bawah ini sehingga loopnya mengiterasikan 
    ## randomized_start_positions DAN BUKAN START_POSITIONS!!!
    for sx, sy in randomized_start_positions:
        if len(all_tours) >= 4:
            break
        print(f"\nMencoba penjelajahan dari posisi awal: ({sx}, {sy}).")
        possible_moves_counts = []
        knight_tour(sx, sy, 0, board, path, all_tours, tree_size, possible_moves_counts, max_tours=4)

    # Jika solusi kurang dari 4, coba posisi lain.
    if len(all_tours) < 4:
        for sx in range(BOARD_SIZE):
            for sy in range(BOARD_SIZE):
                if (sx, sy) not in randomized_start_positions:
                    if len(all_tours) >= 4:
                        break
                    print(f"\nMencoba penjelajahan dari posisi awal: ({sx}, {sy})")
                    possible_moves_counts = []
                    knight_tour(sx, sy, 0, board, path, all_tours, tree_size, possible_moves_counts, max_tours=4)

    os.makedirs("knight_tour_gifs", exist_ok=True)

    # Tampilkan semua penjelajahan yang ditemukan.
    print("")
    for i, (tour, tour_tree_size, possible_moves_counts) in enumerate(all_tours):
        
        filename = f"knight_tour_gifs/knight_tour_{i+1}.gif"
        print(f"Menyimpan animasi GIF ke-{i+1}...")
        generate_gif(tour, filename)
        print(f"GIF disimpan sebagai '{filename}'")

        print("")
        print(f"Penjelajahan ke-{i+1}:")
        # print_tour_chess_board(tour)
        print_tour_sequence(tour)
        print_m_sequence(possible_moves_counts)
        estimated_tree_size = estimate_tree_size_from_m_sequence(possible_moves_counts)
        estimated_tree_sizes.append(estimated_tree_size)
        print(f"Estimasi tree size (berdasarkan rumus m-sequence) untuk barisan penjelajahan ke-{i+1}: {estimated_tree_size}")
        # print(f"Estimasi tree size saat barisan penjelajahan ke-{i+1} ditemukan: {tour_tree_size}\n")

    # Tampilkan statistik pencarian.
    print("")
    print(f"TOTAL dari semua estimasi-estimasi tree size (berdasarkan rumus m-sequence) untuk SEMUA barisan penjelajahan: {sum(estimated_tree_sizes)}")
    print(f"rata rata estimasi size tree: {sum(estimated_tree_sizes)/4}")
    ## print(f"Estimasi tree size (jumlah node pada pohon pencarian): {tree_size[0]}")
    print(f"Total barisan penjelajahan yang ditemukan sejauh ini: {len(all_tours)}")
    print("")

# Penjelasan:
# Set recursion limit agar program tidak berhenti karena batas rekursi Python.
# Jalankan fungsi utama jika file dijalankan langsung.
if __name__ == "__main__":
    sys.setrecursionlimit(2147483647)
    main()