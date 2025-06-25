# Penyelesaian Nomor 1: Implementasi Algoritma Penelurusan BFS dan DFS

Project ini merupakan sebuah tugas kelompok untuk mata kuliah **Desain dan Analisis Algoritma**.
Tujuan utamanya adalah untuk mengimplementasikan dan mendemonstrasikan algoritma penelurusan/traversal **Depth-First Search (DFS)** dan **Breadth-First Search (BFS)** dalam sebuah graf yang memiliki sisi-sisi **BERARAH** dan **TIDAK BERBOBOT**

-----------------

## Daftar Isi

- [Pendahuluan](#pendahuluan)
- [Daftar Fitur](#daftar-fitur)
- [Persyaratan](#persyaratan)
- [Tata Cara Penggunaan](#tata-cara-penggunaan)

-----------------

## Pendahuluan

Penelurusan graf adalah konsep fundamental di bidang ilmu komputer, yang digunakan untuk menelusuri titik simpul dan sisi-sisi di dalam suatu graf. Project ini mengimplementasikan 2 dua teknik penelusuran graf yang populer:

1. **Depth-First Search (DFS)**: Algoritma ini menelusuri graf dengan menjelajahi satu cabang sedalam mungkin sebelum kembali (backtracking) untuk menelusuri cabang lainnya. Cocok untuk menemukan jalur atau komponen terhubung dalam graf.

2. **Breadth-First Search (BFS)**: Algoritma ini menelusuri graf secara bertingkat, mengunjungi semua tetangga dari simpul saat ini sebelum melanjutkan ke tingkat berikutnya. BFS sering digunakan untuk menemukan jalur terpendek dalam graf tak berbobot.

Kedua algoritma ini telah berhasil diimplementasikan untuk bekerja pada graf berarah dan graf tidak berarah.

-----------------

## Daftar Fitur

- **Penelusuran DFS**: Implementasi secara rekursif dan/atau iteratif.
- **Penelusuran BFS**: Implementasi menggunakan antrian (queue).
- Mendukung graf berarah maupun tidak berarah.
- Menerima input graf yang didefinisikan oleh pengguna.
- Menampilkan urutan penelusuran untuk DFS dan BFS.

-----------------

## Persyaratan

Untuk menjalankan project ini, Anda memerlukan:

- Python 3.x yang telah terpasang di sistem Anda.
- Library atau Modul GraphViz untuk merender dan menampilkan graf.
- Library atau Modul Tkinter untuk penggunaan fitur filedialog, yang digunakan di sini untuk menyimpan file PNG GraphViz menggunakan suatu GUI (Graphical User Interface)

-----------------

## Tata Cara Penggunaan

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/SKYTEXCoder/tugas_kelompok_daa.git
   cd dfs_bfs_traversal
   ```

2. Jika belum memiliki library **graphviz** dan **tkinter**, install terlebih dahulu menggunakan pip:

    ```bash
    pip install graphviz
    ```

    > **Catatan:**  
    > Untuk **tkinter**, biasanya sudah terpasang secara default pada instalasi Python. Namun, jika belum tersedia, Anda dapat menginstallnya sesuai dengan sistem operasi Anda.  
    > - **Windows:** Tkinter sudah termasuk dalam installer Python.  
    > - **Linux (Ubuntu/Debian):**
    >   ```bash
    >   sudo apt-get install python3-tk
    >   ```
    > - **MacOS:** Tkinter sudah termasuk dalam installer Python.

3. Setelah semua dependensi terpasang, jalankan program utama dengan perintah berikut di terminal:

    ```bash
    python dfs_bfs.py
    ```