===========================================================
TUGAS KELOMPOK DAA - Penyelesaian Nomor 1
Nama            : Dandy Arya Akbar
Program Studi   : Ilmu Komputer
Angkatan        : 2023
Kelas           : A
NIM             : 1313623028
===========================================================

PROGRAM INI:
-------------
Implementasi algoritma penelusuran graf BFS dan DFS, serta visualisasi graf menggunakan library GraphViz dan Tkinter.

-----------------------------------------------------------
PERSYARATAN SISTEM & INSTALASI
-----------------------------------------------------------

1. Python 3.x harus sudah terpasang.
   Cek dengan: python --version

2. Library Python yang dibutuhkan:
   - graphviz (install menggunakan pip)
   - tkinter (biasanya sudah terpasang, jika belum, lihat instruksi di bawah)

3. Software Graphviz (untuk menghasilkan file PNG):
   - Windows: Download & install dari https://graphviz.gitlab.io/download/
   - Linux: sudo apt-get install graphviz
   - MacOS: brew install graphviz

   Pastikan folder instalasi Graphviz sudah masuk ke PATH environment variable.

-----------------------------------------------------------
INSTALASI DEPENDENSI PYTHON
-----------------------------------------------------------

Buka terminal/cmd di folder program, lalu jalankan:

    pip install graphviz

Untuk Tkinter:
- Windows & MacOS: Sudah termasuk di installer Python.
- Linux (Ubuntu/Debian): 
    sudo apt-get install python3-tk

-----------------------------------------------------------
MENJALANKAN PROGRAM
-----------------------------------------------------------

1. Buka terminal/cmd di folder ini.
2. Jalankan perintah berikut:

    python dfs_bfs.py

Jika Anda memiliki beberapa versi Python, gunakan python3 jika perlu.

-----------------------------------------------------------
PENGGUNAAN PROGRAM
-----------------------------------------------------------

- Setelah dijalankan, akan muncul menu interaktif di terminal.
- Anda dapat:
  - Menambah node/edge
  - Menampilkan visualisasi graf (PNG)
  - Melakukan traversal DFS/BFS dan menampilkan visualisasinya
  - Menyimpan/memuat graf ke/dari file .dot
  - Menghapus/mengatur ulang graf
  - Keluar dari program

Visualisasi graf dan hasil traversal akan otomatis terbuka di software image viewer yang menjadi default di komputer Anda. Anda juga dapat menyimpan hasil visualisasi ke file PNG melalui dialog GUI.

-----------------------------------------------------------
CATATAN
-----------------------------------------------------------

- Jika visualisasi tidak muncul, pastikan library GraphViz sudah terinstall/terpasang di sistem dan PATH sudah benar.
- Jika terjadi error terkait Tkinter, pastikan library tersebut sudah terpasang sesuai sistem operasi Anda.
- Untuk penggunaan file .dot, gunakan menu simpan/muat pada program, atau edit file .dot secara manual sesuai format Graphviz.

-----------------------------------------------------------
Selamat mencoba!