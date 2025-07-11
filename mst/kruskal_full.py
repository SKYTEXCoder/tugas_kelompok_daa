import re, graphviz, tkinter
from tkinter import filedialog

class Graph:
    def __init__(self):
        """
        Inisialisasi objek atau instance dari Graph.
        Fungsi ini akan membuat dictionary kosong yang bernama adjacency_list untuk menyimpan konfigurasi data graf.
        Setiap key pada dictionary ini adalah nama atau identifier dari node, dan value-nya adalah list dari tuple yang berisi node tetangga beserta bobot (weight) dari edge yang menghubungkan kedua node tersebut.
        """
        self.adjacency_list = {}
        
    def add_node(self, node_name):
        """
        Adds a new node to the graph if it does not already exist.
        Parameters:
            node_name (str): The name of the node to be added.
        Returns:
            bool: True if the node was successfully added, False if the node already exists.
        Side Effects:
            Prints a message indicating whether the node was added or already exists in the graph.
        """
        if node_name not in self.adjacency_list:
            self.adjacency_list[node_name] = []
            print(f"Node '{node_name}' berhasil ditambahkan ke dalam konfigurasi data graf yang termuat saat ini.")
            return True
        else:
            print(f"Node yang bernama '{node_name}' sudah ada di dalam konfigurasi data graf yang termuat saat ini.")
            return False
        
    def add_edge(self, u, v, weight):
        
        """
        Adds an edge between two nodes with a specified weight.
        Parameters:
            u (str): The name of the first node.
            v (str): The name of the second node.
            weight (int or float): The weight of the edge connecting the two nodes.
        Returns:
            bool: True if the edge was successfully added, False if there was an issue.
        Side Effects:
            Prints a message indicating whether the edge was added, updated, or if there was an issue.
        """
        
        if not isinstance(weight, (int, float)) or weight <= 0:
            print(f"Bobot edge harus berupa angka positif/ Input bobot: {weight}")
            return False
        
        if u not in self.adjacency_list:
            print(f"Node yang bernama '{u}' tidak ada di dalam konfigurasi data graf yang termuat saat ini.")
            return False
        if v not in self.adjacency_list:
            print(f"Node yang bernama '{v}' tidak ada di dalam konfigurasi data graf yang termuat saat ini.")
            return False
        
        for neighbor, existing_weight in self.adjacency_list[u]:
            if neighbor == v:
                if existing_weight == weight:
                    print(f"Edge dari '{u}' ke '{v} dan dari '{v}' ke '{u}' dengan bobot {weight} sudah ada di dalam konfigurasi data graf yang termuat saat ini.")
                    return False
                else:
                    self.adjacency_list[u].remove((v, existing_weight))
                    self.adjacency_list[v].remove((u, existing_weight))
                    self.adjacency_list[u].append((v, weight))
                    self.adjacency_list[v].append((u, weight))
                    print(f"Bobot edge dari '{u}' ke '{v}' dan dari '{v}' ke '{u}' telah berhasil diperbarui menjadi sebesar {weight}.")
                    return True
        
        self.adjacency_list[u].append((v, weight))
        self.adjacency_list[v].append((u, weight))
        print(f"Edge dari '{u}' ke '{v}' dan dari '{v}' ke '{u}' dengan bobot yang sebesar {weight} telah berhasil ditambahkan ke dalam konfigurasi data graf yang termuat saat ini.")
        return True
        
    def display_graph(self, save_to_file=False):
        
        """
        Menampilkan representasi graf saat ini menggunakan library GraphViz.
        Opsional: menyimpan graf ke file gambar berformat .PNG jika save_to_file bernilai True.
        :param save_to_file: Jika True, graf akan disimpan ke file PNG.
        """
        
        dot = graphviz.Graph(comment='Graph Visualization', format='png')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='ellipse', color='orange', penwidth='3', style='solid', fontname='Arial', fontweight='bold')
        
        edges = set()

        for node in self.adjacency_list:
            dot.node(node)  
            for neighbor, weight in self.adjacency_list[node]:
                if (node, neighbor) not in edges and (neighbor, node) not in edges:
                    edges.add((node, neighbor))
                    dot.edge(node, neighbor, label=str(weight))
                    
        try:
            dot.view(cleanup=True)
            print("Visualisasi graf berhasil dibuka di image viewer default Anda.")
            
            if save_to_file:
                root = tkinter.Tk()
                root.withdraw()
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                
                if file_path:
                    dot.render(file_path, view=False)
                    print(f"Graf berhasil disimpan di '{file_path}'")
                    
                else:
                    print("Operasi penyimpanan graf dibatalkan.")
                    
        except Exception as exception:
            print(f"Terjadi kesalahan saat mencoba menampilkan graf: {exception}")
            
    def save_graph_to_dot_file(self):
        """
        Saves the currently-loaded graph data configuration into a GraphViz .DOT file.
        """
        if not self.adjacency_list:
            print("Graf saat ini masih kosong. Tidak ada konfigurasi data graf yang dapat disimpan ke dalam file GraphViz .DOT.")
            return
        
        try:
            root = tkinter.Tk()
            root.withdraw()
            file_path = filedialog.asksaveasfilename(defaultextension=".dot", filetypes=[("DOT files", "*.dot")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write("graph G {\n")
                    file.write("  rankdir=LR;\n")
                    file.write("  node [shape=ellipse, color=orange, style=solid, fontname=Arial, fontweight=bold];\n")

                    edges = set()
                    for node, neighbors in self.adjacency_list.items():
                        for neighbor, weight in neighbors:
                            if (neighbor, node) not in edges:
                                edges.add((node, neighbor))
                                file.write(f'  "{node}" -- "{neighbor}" [label="{weight}"];\n')

                    file.write("}\n")
                print(f"Graf berhasil disimpan ke dalam file '{file_path}'.")
            else:
                print("Operasi penyimpanan graf dibatalkan.")
        except Exception as e:
            print(f"Terjadi kesalahan saat menyimpan graf ke file: {e}")

    def load_graph_from_dot_file(self):
        """
        Loads a graph configuration from a GraphViz .DOT file.
        """
        try:
            root = tkinter.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(filetypes=[("DOT files", "*.dot")])

            if file_path:
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                self.adjacency_list.clear()
                edge_pattern = re.compile(r'"(.+?)"\s*--\s*"(.+?)"\s*\[label="(.+?)"\];')

                for line in lines:
                    match = edge_pattern.search(line)
                    if match:
                        u, v, weight = match.groups()
                        weight = int(weight)
                        if u not in self.adjacency_list:
                            self.adjacency_list[u] = []
                        if v not in self.adjacency_list:
                            self.adjacency_list[v] = []
                        if (v, weight) not in self.adjacency_list[u]:
                            self.adjacency_list[u].append((v, weight))
                        if (u, weight) not in self.adjacency_list[v]:
                            self.adjacency_list[v].append((u, weight))

                print(f"Graf berhasil dimuat dari file '{file_path}'.")
            else:
                print("Operasi pemuatan graf dibatalkan.")
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat graf dari file: {e}")
        
    def print_adjacency_list(self):
        """
        Menampilkan adjacency list dari konfigurasi data graf yang termuat saat ini.
        Fungsi ini akan mencetak setiap node beserta daftar node tujuan (edge) yang terhubung dengannya beserta semua bobot-bobotnya.
        Jika graf kosong, akan menampilkan pesan bahwa graf saat ini kosong.
        """
        print("")
        if not self.adjacency_list:
            print("Konfigurasi data graf yang sedang termuat saat ini masih kosong.")
            return
        print("Representasi ADJACENCY LIST dari konfigurasi data graf yang sedang termuat saat ini:")
        for node, edges in self.adjacency_list.items():
            if edges:
                edges_string = ', '.join([f"({neighbor}, {weight})" for neighbor, weight in edges])
                print(f"{node}: {edges_string}")
            else:
                print(f"{node}: TIDAK ADA EDGE ATAU KONEKSI")
        print("")
        
    def clear_graph_data_configuration(self):
        """
        Menghapus semua data graf yang tersimpan di adjacency list dan mengatur ulang grafnya dari awal.
        Fungsi ini akan mengosongkan adjacency list dan mencetak pesan konfirmasi kepada pengguna program. 
        """
        if not self.adjacency_list:
            print("Graf saat ini sudah kosong. Tidak ada data yang perlu dihapus.")
        else:
            self.adjacency_list.clear()
            print("Semua konfigurasi data graf yang sedang termuat saat ini sudah berhasil dihapus dari program ini. Graf telah diatur ulang dari awal.")
            
    def kruskals_algorithm_mst(self):
        """
        Mencari Minimum Spanning Tree (MST) menggunakan Algoritma Kruskal pada konfigurasi data graf undirected/weighted yang sedang termuat di dalam program saat ini.
        Hasil MST akan langsung divisualisasikan menggunakan library GraphViz dan pengguna program akan diberi opsi untuk menyimpan gambar MST.
        """
        if not self.adjacency_list or len(self.adjacency_list) < 2:
            print("Konfigurasi data graf saat ini isinya masih kosong atau masih terlalu sedikit node untuk membentuk sebuah MST.")
            return

        # collect semua sisi-sisi yang "unik" (karena graf ini undirected dan kita menggunakan adjacency list di atas)
        edges = []
        seen = set()
        for u in self.adjacency_list:
            for v, w in self.adjacency_list[u]:
                if (v, u) not in seen:
                    edges.append((w, u, v))
                    seen.add((u, v))

        # urutkan sisi-sisi (edges) berdasarkan besar bobotnya. Fungsi sort di sini sudah mengsort list edges di atas ke dalam urutab menaik (ascending)
        edges.sort()

        # inisialisasi struktur data disjoint-set (union-find)
        parent = {}
        rank = {}

        # definisi fungsi find(node)
        def find(node):
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        # definisi fungsi union(u, v)
        def union(u, v):
            root_u = find(u)
            root_v = find(v)
            if root_u == root_v:
                return False
            if rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                if rank[root_u] == rank[root_v]:
                    rank[root_u] += 1
            return True

        # Pertama-tama, setiap node akan menjadi parent dirinya sendiri
        for node in self.adjacency_list:
            parent[node] = node
            rank[node] = 0

        # Step 5: Proses edge satu per satu, tambahkan ke MST jika tidak membentuk siklus
        mst_edges = []
        total_weight = 0
        for w, u, v in edges:
            if union(u, v):
                mst_edges.append((u, v, w))
                total_weight += w
            if len(mst_edges) == len(self.adjacency_list) - 1:
                break

        if len(mst_edges) != len(self.adjacency_list) - 1:
            print("Graf tidak terhubung, MST tidak dapat dibentuk dari semua node.")
            return

        # gambar MST menggunakan library GraphViz
        dot = graphviz.Graph(comment="Minimum Spanning Tree (MST) - Kruskal's Algorithm", format='png')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='ellipse', color='green', penwidth='3', style='solid', fontname='Arial', fontweight='bold')
        dot.attr(label=f"Total Bobot: {total_weight}", labelloc='b', fontsize='14', fontname='Arial', fontcolor='black')

        # tambahkan node-node nya
        for node in self.adjacency_list:
            dot.node(node)

        # selanjutnya, tambahkan sisi-sisi mst
        for u, v, w in mst_edges:
            dot.edge(u, v, label=str(w), color='blue', penwidth='2')
            
        # langsung tampilkan gambar mstnya menggunakan library graphviz
        try:
            dot.view(cleanup=True)
            print("Minimum Spanning Tree (MST) hasil Algoritma Kruskal berhasil divisualisasikan.")
            print(f"Total bobot dari semua koneksi atau edge yang terkandung di MST: {total_weight}")

            # tanya pengguna program apakah dia mau menyimpan gambar hasil MST-nya ke file gambar berformat PNG atau ngga
            save_option = input("Apakah Anda ingin menyimpan hasil MST ke file gambar PNG? (y/N): ").strip().lower()
            if save_option.startswith('y'):
                root = tkinter.Tk()
                root.withdraw()
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
                
                if file_path:
                    dot.render(file_path.rsplit('.', 1)[0], view=False, format='png', cleanup=True)
                    print(f"Hasil MST berhasil disimpan di '{file_path}'")
                    
                else:
                    print("Operasi penyimpanan hasil MST dibatalkan.")
                    
        except Exception as exception:
            print(f"Terjadi kesalahan saat menampilkan atau menyimpan hasil MST: {exception}")
        

def print_menu_options():
    """
    Menampilkan menu interaktif untuk para pengguna program Nomor 2 (Algoritma Kruskal).
    """
    print("\n========== Menu Operasi Graf Untuk Program Nomor 2 (Algoritma Kruskal) ===========================")
    print("1. Tambahkan Node Baru ➕")
    print("2. Tambahkan UNDIRECTED EDGE Baru ⬅️➡️")
    print("3. Tampilkan Representasi File Gambar Berformat PNG Dari Konfigurasi Data Graf Yang Termuat Saat Ini 🖼️")
    print("4. Lakukan Algoritma Kruskal (Kruskal's Algorithm) Untuk Membuat Minimum-Spanning Tree (MST)-nya 🌲")
    print("5. Simpan (SAVE) Konfigurasi Data Graf Yang Termuat Saat Ini Ke Dalam File GraphViz .DOT 💾")
    print("6. Muatkan (LOAD) Konfigurasi Data Graf Dari File GraphViz .DOT Yang Sudah Ada 📂")
    print("7. Tampilkan Representasi ADJACENCY LIST Dari Konfigurasi Data Graf Yang Termuat Saat Ini 📜")
    print("8. CLEAR atau BERSIHKAN Konfigurasi Data Graf Yang Sedang Termuat Saat Ini 🔄")
    print("9. Keluar Dari Sini dan Hentikan Program ❌")
    print("==============================================================================\n")
    
def main():
    graph = Graph()
    print("")
    print("Selamat datang di Program Operasi Graf Untuk Nomor 2 (Algoritma Kruskal)! 🌐")
    loadOnStartup = input("Apakah Anda ingin memuat konfigurasi data graf yang sudah ada dari file GraphViz .DOT? (y/N): ").strip().lower()
    if loadOnStartup.startswith('y'):
        graph.load_graph_from_dot_file()
    programIsRunning = True
    while programIsRunning:
        print_menu_options()
        choice = input("Silakan masukkan pilihan Anda (1-9): ")
        if choice == '1':
            node_name = input("Masukkan nama node baru yang akan ditambahkan ke graf saat ini: ").strip()
            if node_name:
                graph.add_node(node_name)  
            else:
                print("Nama node baru TIDAK BOLEH kosong. Silakan coba lagi.")
                
        elif choice == '2':
            if not graph.adjacency_list:
                print("Graf saat ini masih kosong. Silakan tambahkan node-node baru terlebih dahulu sebelum menambahkan edge.")
                continue
            u = input("Masukkan nama node asal yang sudah ada untuk undirected edge: ").strip()
            v = input("Masukkan nama node tujuan yang sudah ada untuk undirected edge: ").strip()
            weight = int(input("Masukkan bobot (weight) dari undirected edge yang akan menghubungkan kedua node tersebut: ").strip())
            if u and v and weight:
                graph.add_edge(u, v, weight)
            else:
                print("Nama node pertama, node kedua, dan bobot TIDAK BOLEH kosong. Silakan coba lagi.")
                
        elif choice == '3':
            if not graph.adjacency_list:
                print("Graf saat ini masih kosong. Silakan tambahkan node baru dan edge ke dalam graf terlebih dahulu sebelum mencoba menampilkan graf.")
                continue   
            save_option = input("Apakah Anda ingin menyimpan visualisasi data graf yang sedang dimuat ke dalam file gambar berformat PNG? (y/N): ").strip().lower()
            graph.display_graph(save_to_file=save_option.startswith('y'))
            
        elif choice == '4':
            graph.kruskals_algorithm_mst()
                                
        elif choice == '5':
            graph.save_graph_to_dot_file()
            
        elif choice == '6':
            graph.load_graph_from_dot_file()
            
        elif choice == '7':
            if not graph.adjacency_list:
                print("Graf saat ini masih kosong. Silakan tambahkan node baru dan edge ke dalam graf terlebih dahulu sebelum menampilkan adjacency list.")
                continue
            graph.print_adjacency_list()
            
        elif choice == '8':
            graph.clear_graph_data_configuration()
            
        elif choice == '9':
            save_choice = input("Apakah Anda ingin menyimpan konfigurasi data graf yang sedang dimuat ke dalam file GraphViz .DOT terlebih dahulu sebelum keluar? (y/N): ").strip().lower()
            if save_choice.startswith('y'):
                graph.save_graph_to_dot_file()
            print("Saatnya keluar dari aplikasi graf. Sampai jumpa di sesi berikutnya! 👋")            
            programIsRunning = False            
            print("")            
            break
        
        else: 
            print("Pilihan tidak valid. Silakan masukkan nomor antara 1 dan 9.")

if __name__ == "__main__":
    main()