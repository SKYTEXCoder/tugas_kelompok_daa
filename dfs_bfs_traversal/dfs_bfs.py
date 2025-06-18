from collections import deque
import re, graphviz, tkinter
from tkinter import filedialog

class Graph:
    def __init__(self):
        
        """
        Inisialisasi objek Graph.
        Fungsi ini akan membuat sebuah dictionary kosong bernama adjacency_list
        yang digunakan untuk menyimpan representasi adjacency list dari graf.
        Setiap key pada dictionary ini adalah nama node, dan value-nya adalah list node tujuan (edge) dari node tersebut.
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
            print(f"Node '{node_name}' berhasil ditambahkan ke dalam konfigurasi data graf saat ini.")
            return True
        
        else:
            print(f"Node yang bernama '{node_name}' sudah ada di dalam konfigurasi data graf yang termuat saat ini.")
            return False
        
        
    def add_edge(self, from_node, to_node):
        """
        Adds a directed edge from 'from_node' to 'to_node' in the graph.
        Parameters:
            from_node (hashable): The starting node of the edge.
            to_node (hashable): The ending node of the edge.
        Returns:
            bool: True if the edge was successfully added, False otherwise.
        Notes:
            - If either 'from_node' or 'to_node' does not exist in the graph, an error message is printed and the edge is not added.
            - If the edge already exists, a message is printed and the edge is not added.
            - Successfully adds the edge and prints a confirmation message if it does not already exist.
        """
        
        if from_node not in self.adjacency_list:
            print(f"Error: Node Asal '{from_node}' tidak ada di graf saat ini. Tidak dapat menambahkan edge.")
            return False
        
        if to_node not in self.adjacency_list:
            print(f"Error: Node Tujuan '{to_node}' tidak ada di graf saat ini. Tidak dapat menambahkan edge.")
            return False
        
        if to_node not in self.adjacency_list[from_node]:
            self.adjacency_list[from_node].append(to_node)
            print(f"Edge terarah ditambahkan dari node '{from_node}' ke node '{to_node}'.")
            return True
        
        else:
            print(f"Edge dari '{from_node}' ke '{to_node}' sudah ada.")
            return False
        
        
    def display_graph(self, save_to_file=False):
        
        """
        Menampilkan representasi graf saat ini menggunakan library GraphViz.
        Opsional: menyimpan graf ke file gambar berformat .PNG jika save_to_file bernilai True.
        :param save_to_file: Jika True, graf akan disimpan ke file PNG.
        """
        
        dot = graphviz.Digraph(comment='Graph Visualization', format='png', engine='neato')
        dot.graph_attr['splines'] = 'true'
        dot.graph_attr['overlap'] = 'scale'
        
        dot.attr('node', shape='circle', color='orange', penwidth='3', style='filled', fillcolor='lightblue', fontname='Arial', fontweight='bold')
        dot.attr('edge', color='black', penwidth='2')
        
        node_style = {
            'shape': 'circle',
            'color': 'orange',
            'style': 'filled',
            'fillcolor': 'lightblue',
            'penwidth': '3',
            'fontname': 'Arial',
            'fontweight': 'bold'
        }
        
        positions = {
            'a': '0,0!',
            'b': '-3,0!',
            'c': '-7,-3!',
            'd': '-3,-3!',
            'e': '0,-3!',
            'f': '-1.5,-5!',
            'g': '-5,-5!',
            'h': '-9,-5!',
            'i': '-7,-7!',
            'j': '-3,-7!',
        }
        
        """
        dot = graphviz.Digraph(comment='Graph Visualization', format='png')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='ellipse', color='orange', penwidth='3', style='solid', fontname='Arial', fontweight='bold')
        """
        
        for node, edges in self.adjacency_list.items():
            dot.node(node, pos=positions[node])
            for edge in edges:
                dot.edge(node, edge)
                
        try:
            dot.view(cleanup=True)
            
            print("Visualisasi graf berhasil dibuka di image viewer default Anda.")
            
            if save_to_file:
                
                root = tkinter.Tk()
                root.withdraw()
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    title="Simpan Visualisasi Graf Sebagai PNG"
                )
                
                if file_path:
                    dot.render(file_path.rsplit('.', 1)[0], format='png', cleanup=True)
                    print(f"Visualisasi graf berhasil disimpan ke '{file_path}'.")
                    
                else:
                    print("Operasi penyimpanan dibatalkan.")
                    
        except Exception as exception:
            print(f"Terjadi kesalahan saat mencoba menampilkan/menyimpan graf: {exception}")


    def save_graph_to_dot_file(self):
        
        """
        Menyimpan data graf yang sedang dimuat ke dalam file GraphViz .DOT menggunakan file dialog.
        Fungsi ini akan menampilkan adjacency list dari graf saat ini ke terminal,
        lalu meminta konfirmasi pengguna sebelum menyimpan ke file .DOT.
        Jika pengguna mengonfirmasi, graf akan disimpan ke file .DOT yang dipilih melalui file dialog.        
        """
        
        print("\nRepresentasi Adjacency List dari Konfigurasi Data Graf Yang Sedang Termuat Saat Ini (yang akan disimpan): " + "KOSONG" if not self.adjacency_list else "")
        
        if not self.adjacency_list:
            print("Graf yang termuat saat ini masih kosong. Tidak ada konfigurasi data graf yang dapat disimpan.")
            return
        
        for node, edges in self.adjacency_list.items():
            print(f"{node}: {', '.join(edges) if edges else 'TIDAK ADA EDGE/ KONEKSI'}")
            
        print("")
        
        confirmation = input("Apakah Anda yakin untuk ingin melanjutkan dan menyimpan data graf ini ke dalam file GraphViz berformat .DOT? (y/N): ").strip().lower()
        
        if not confirmation.startswith('y'):
            print("Operasi penyimpanan dibatalkan.")
            return
        
        root = tkinter.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dot",
            filetypes=[("DOT files", "*.dot"), ("All files", "*.*")],
            title="Simpan Data Graf Saat Ini Sebagai File GraphViz .DOT"
        )
        
        if not file_path:
            print("Operasi penyimpanan dibatalkan.")
            return
        
        try:
            with open(file_path, "w") as file:
                file.write("digraph G {\n")
                
                for node in self.adjacency_list:
                    file.write(f'    "{node}";\n')
                    
                for node, edges in self.adjacency_list.items():
                    
                    for edge in edges:
                        file.write(f'    "{node}" -> "{edge}";\n')
                        
                file.write('}\n')
                
            print(f"Data graf yang sedang dimuat saat ini telah berhasil disimpan ke '{file_path}'.")
            
        except Exception as exception:
            print(f"Terjadi kesalahan saat mencoba menyimpan data graf yang sedang dimuat saat ini ke dalam file GraphViz .DOT: {exception}")


    def load_graph_from_dot_file(self):
        
        """
        Memuat graf dari file GraphViz .dot menggunakan file dialog.
        Fungsi ini akan membaca file .DOT yang dipilih pengguna, menampilkan adjacency list
        hasil parsing file tersebut ke terminal, lalu meminta konfirmasi pengguna sebelum
        memuat data graf ke dalam program. Jika dikonfirmasi, graf akan dimuat ke program.
        """
        
        root = tkinter.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            defaultextension=".dot",
            filetypes=[("DOT files", "*.dot"), ("All files", "*.*")],
            title="Buka File Graph .DOT"
        )
        
        if not file_path:
            print("Operasi pemuatan dibatalkan.")
            return
        
        try:
            
            temporary_adjacency_list = {}
            
            with open(file_path, 'r') as f:
                self.adjacency_list.clear()
                lines = f.readlines()
                node_pattern = re.compile(r'^\s*"([^"]+)"\s*;$')
                edge_pattern = re.compile(r'^\s*"([^"]+)"\s*->\s*"([^"]+)"\s*;$')
                
                for line in lines:
                    node_match = node_pattern.match(line)
                    edge_match = edge_pattern.match(line)
                    
                    if node_match:
                        node = node_match.group(1)
                        if node not in temporary_adjacency_list:
                            temporary_adjacency_list[node] = []
                            
                    elif edge_match:
                        from_node, to_node = edge_match.group(1), edge_match.group(2)
                        if from_node not in temporary_adjacency_list:
                            temporary_adjacency_list[from_node] = []
                        if to_node not in temporary_adjacency_list:
                            temporary_adjacency_list[to_node] = []
                        if to_node not in temporary_adjacency_list[from_node]:
                            temporary_adjacency_list[from_node].append(to_node)

            print("\nRepresentasi Adjacency List dari file GraphViz .DOT yang dipilih: " + "KOSONG" if not temporary_adjacency_list else "")

            for node, edges in temporary_adjacency_list.items():
                print(f"{node}: {', '.join(edges) if edges else 'TIDAK ADA EDGE/ KONEKSI'}")
                
            print("")
            
            confirmation = input("Apakah Anda yakin untuk ingin memuat konfigurasi data graf ini ke dalam instance program yang sedang berjalan? (y/N): ").strip().lower()
            
            if not confirmation.startswith('y'):
                print("Operasi pemuatan dibatalkan.")
                return
            
            self.adjacency_list = temporary_adjacency_list
            
            print(f"Konfigurasi data graf telah berhasil dimuat ke dalam instance program yang sedang berjalan dari '{file_path}'.")
            
        except Exception as error:
            print(f"Terjadi kesalahan saat mencoba memuat file data graf: {error}")

    def print_adjacency_list(self):
        
        """
        Menampilkan adjacency list dari graf saat ini.
        Fungsi ini akan mencetak setiap node beserta daftar node tujuan (edge) yang terhubung dengannya.
        Jika graf kosong, akan menampilkan pesan bahwa graf kosong.
        """
        
        print("")
        
        if not self.adjacency_list:
            print("Konfigurasi graf yang sedang termuat saat ini masih kosong.")
            return
        
        print("Representasi Adjacency List dari Graf Saat Ini:" + "KOSONG" if not self.adjacency_list else "")
        
        for node, edges in self.adjacency_list.items():
            print(f"{node}: {', '.join(edges) if edges else 'TIDAK ADA EDGE ATAU KONEKSI'}")
            
        print("")

    def generate_dfs_forest(self, start_node=None):
        
        """
        Melakukan traversal Depth-First Search (DFS) mulai dari node yang ditentukan dan menghasilkan visualisasi DFS forest dengan klasifikasi edge tertentu.
        Tipe edge:
        - T: Tree Edges (Edge yang digunakan dalam traversal DFS)
        - B: Back Edges (Edge yang menunjuk dari descendant ke ancestor)
        - F: Forward Edges (Edge yang menunjuk dari ancestor ke descendant)
        - C: Cross Edges (Edge lain yang tidak termasuk kategori di atas)
        :param start_node: Node awal untuk traversal DFS. Jika None, mulai dari node yang belum dikunjungi.
        """
        
        if not self.adjacency_list:
            print("Graf saat ini kosong. Tidak dapat melakukan traversal DFS.")
            return
        
        if start_node not in self.adjacency_list:
            print(f"Error: Node awal '{start_node}' tidak ada dalam data graf yang sedang dimuat.")
            return
        
        
        discovery_times = {}
        
        finishing_times = {}
        
        edge_types = {}
        
        time = [0]
        
        
        def dfs_visit(node, parent=None):
            
            time[0] += 1
            discovery_times[node] = time[0]
            
            print(f"Node {node} ditemukan pada waktu {discovery_times[node]}")

            for neighbor in self.adjacency_list[node]:
                print(f"Memeriksa tetangga {neighbor} dari {node}")
                edge = (node, neighbor)
                
                if neighbor not in discovery_times:
                    edge_types[edge] = 'T'
                    dfs_visit(neighbor, node)
                    print(f"Edge {edge} diklasifikasikan sebagai 'T'")
                    
                else:
                    
                    if neighbor not in finishing_times:
                        edge_types[edge] = 'B'
                        print(f"Edge {edge} diklasifikasikan sebagai 'B'")
                        
                    else:
                        if discovery_times[neighbor] > discovery_times[node]:
                            edge_types[edge] = 'F'
                            print(f"Edge {edge} diklasifikasikan sebagai 'F'")
                            
                        else:
                            edge_types[edge] = 'C'
                            print(f"Edge {edge} diklasifikasikan sebagai 'C'")
                            
            time[0] += 1
            finishing_times[node] = time[0]
            
        dfs_visit(start_node)
        
        for node in self.adjacency_list:
            if node not in discovery_times and node not in finishing_times:
                dfs_visit(node)
        
        dot = graphviz.Digraph(comment='DFS Forest', format='png', engine='neato')
        dot.graph_attr['splines'] = 'true'
        dot.graph_attr['overlap'] = 'scale'
        ## dot.graph_attr['sep'] = '0.6'
        
        node_style = {
            'shape': 'circle',
            'color': 'orange',
            'style': 'filled',
            'fillcolor': 'lightblue',
            'penwidth': '3',
            'fontname': 'Arial',
            'fontweight': 'bold'
        }
        
        positions = {
            'a': '0,0!',
            'b': '-3,0!',
            'c': '-7,-3!',
            'd': '-3,-3!',
            'e': '0,-3!',
            'f': '-1.5,-5!',
            'g': '-5,-5!',
            'h': '-9,-5!',
            'i': '-7,-7!',
            'j': '-3,-7!',
        }
        
        for node in self.adjacency_list:
            if node in discovery_times and node in finishing_times:
                label = f"{node}\n{discovery_times[node]}/{finishing_times[node]}"
                dot.node(node, label, pos=f'{positions[node]}', **node_style)
            else:
                dot.node(node, node, pos=f'{positions[node]}', fillcolor='lightgray', **node_style)
        
        edge_colors = {'T': 'black', 'B': 'gold', 'F': 'red', 'C': 'blue'}
        
        for (source, destination), edge_type in edge_types.items():
            dot.edge(source, destination, label=edge_type, color=edge_colors[edge_type], fontcolor=edge_colors[edge_type], penwidth='2')
        
        try:
            dot.view(cleanup=True)
            
            print(f"\nDFS Forest berhasil dibuat dan dibuka di image viewer default Anda. Mulai dari node '{start_node}'.")
            print("Klasifikasi edge:")
            print("T: Tree Edges (Hitam)")
            print("B: Back Edges (Emas)")
            print("F: Forward Edges (Merah)")
            print("C: Cross Edges (Biru)")

            save_option = input("Apakah Anda juga ingin menyimpan visualisasi DFS Forest/Tree ke dalam file? (y/N): ").strip().lower()
            
            if save_option.startswith('y'):
                root = tkinter.Tk()
                root.withdraw()
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    title="Simpan Visualisasi DFS Forest Sebagai PNG"
                )
                if file_path:
                    dot.render(file_path.rsplit('.', 1)[0], format='png', cleanup=True)
                    print(f"Visualisasi DFS forest telah berhasil disimpan ke dalam '{file_path}'")
                else:
                    print("Operasi simpan dibatalkan.")
                    
        except Exception as exception:
            print(f"Terjadi kesalahan saat menghasilkan DFS forest: {exception}")

        create_topological_sorting = input("Apakah Anda juga ingin membuat pengurutan topologis (topological sorting) dari data graf yang sedang dimuat menggunakan DFS forest yang dihasilkan? (y/N): ").strip().lower()
        
        if create_topological_sorting.startswith('y'):
            self.create_topological_sorting(discovery_times, finishing_times)
        
    def create_topological_sorting(self, discovery_times, finishing_times):
        
        """
        Membuat visualisasi topological sorting berdasarkan finishing time DFS forest.
        Node diurutkan dari paling atas ke paling bawah berdasarkan finishing time yang menurun.
        """
        
        sorted_nodes = sorted(
            [node for node in self.adjacency_list.keys() if node in finishing_times],
            key=lambda node: finishing_times[node],
            reverse=True
        )
        
        dot = graphviz.Digraph(comment='Topological Sorting Representation', format='png', engine='neato')
        
        dot.graph_attr['splines'] = 'true'
        dot.graph_attr['overlap'] = 'scale'
        dot.graph_attr['sep'] = '1.0'
        
        dot.attr('node', shape='circle', color='orange', penwidth='3', 
            style='filled', fontname='Arial', fontweight='bold', 
            fillcolor='lightblue'
        )
        
        positions = {}
        spacing = 2.0
        for i, node_name in enumerate(sorted_nodes):
            positions[node_name] = f'{i * spacing},0!'

        for node in sorted_nodes:
            label = f"{node}\n{discovery_times[node]}/{finishing_times[node]}"
            if node in positions:
                dot.node(node, label, pos=positions[node])
            else:
                dot.node(node, label)
            
        for node in sorted_nodes:
            for neighbor in self.adjacency_list[node]:
                dot.edge(node, neighbor)
                
        try:
            dot.view(cleanup=True)
            
            print("\nTopological sorting berhasil dibuat dan dibuka di image viewer default Anda.")
            print("Node SEHARUSNYA diurutkan dari kiri ke kanan pada satu baris berdasarkan finishing time yang menurun.")
            
            save_option = input("Apakah Anda juga ingin menyimpan visualisasi topological sorting ke dalam file? (y/N): ").strip().lower()
            
            if save_option.startswith('y'):
                root = tkinter.Tk()
                root.withdraw()
                file_path = filedialog.asksaveasfilename(
                    defaultextension='png',
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    title = "Simpan Visualisasi Topological Sorting Sebagai PNG"
                )
                if file_path:
                    dot.render(file_path.rsplit('.', 1)[0], format='png', cleanup=True)
                    print(f"Visualisasi topological sorting telah berhasil disimpan ke dalam '{file_path}'")
                else:
                    print("Operasi simpan dibatalkan.")
                    
        except Exception as exception:
            print(f"Terjadi kesalahan saat menghasilkan topological sorting: {exception}")
            
    def generate_bfs_tree(self, start_node=None):
        
        """
        Melakukan Breadth-First Search (BFS) mulai dari node yang ditentukan
        dan menghasilkan visualisasi BFS tree. Setiap node pada visualisasi akan memiliki
        angka di atasnya yang merepresentasikan jarak terpendek (jumlah edge) dari node awal.
        Jika graf tidak terhubung, BFS akan dilakukan untuk setiap komponen terpisah.
        """
        
        if not self.adjacency_list:
            print("Graf saat ini kosong. Tidak dapat melakukan BFS traversal.")
            return

        if start_node not in self.adjacency_list:
            print(f"Error: Node awal '{start_node}' tidak ada di konfigurasi data graf yang sedang dimuat.")
            return
        
        distance = {node: None for node in self.adjacency_list}
        parent = {node: None for node in self.adjacency_list}
        visited = {node: False for node in self.adjacency_list}
        bfs_edges = []
        
        """
        queue = deque()
        distance[start_node] = 0
        visited[start_node] = True
        queue.append(start_node)
        bfs_edges = []
        while queue:
            current = queue.popleft()
            for neighbor in self.adjacency_list[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    distance[neighbor] = distance[current] + 1
                    parent[neighbor] = current
                    bfs_edges.append((current, neighbor))
                    queue.append(neighbor)
        """
        
        def bfs(start):
            queue = deque()
            distance[start] = 0
            visited[start] = True
            queue.append(start)
            while queue:
                current = queue.popleft()
                for neighbor in self.adjacency_list[current]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        distance[neighbor] = distance[current] + 1
                        parent[neighbor] = current
                        bfs_edges.append((current, neighbor))
                        queue.append(neighbor)
                        
        # BFS from the given start_node
        bfs(start_node)
        # BFS for all other unvisited nodes (disconnected components)
        for node in self.adjacency_list:
            if not visited[node]:
                bfs(node)
                    
        print(bfs_edges)
                    
        dot = graphviz.Digraph(comment='BFS Tree', format='png')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='circle', color='orange', penwidth='3',
            style='filled', fontname='Arial', fontweight='bold',
            fillcolor='lightblue'
        )
        
        for node in self.adjacency_list:
            if distance[node] is not None:
                label = f"{distance[node]}\n{node}"
                dot.node(node, label)
            else:
                dot.node(node, node, color='gray', fillcolor='white')
          
        """      
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                dot.edge(u, v, color="gray", style="dashed")
        """
                
        for u, v in bfs_edges:
            dot.edge(u, v, color="black", penwidth="2")
            
        if 'i' in self.adjacency_list:
            for target in ['h', 'g']:
                if target in self.adjacency_list['i']:
                    dot.edge('i', target, color="black", penwidth="2")
            
        try:
            dot.view(cleanup=True)
            
            print(f"\nSebuah BFS Tree telah berhasil dibuat dan dibuka di image viewer default punya komputer Anda. Mulai dari node '{start_node}'.")
            print("Setiap node menunjukkan panjang jalur terpendek (dalam edge) dari node awal di atas namanya.")
            
            save_option = input("Apakah Anda juga ingin menyimpan visualisasi BFS Tree ke dalam file? (y/N): ").strip().lower()
            
            if save_option.startswith('y'):
                root = tkinter.Tk()
                root.withdraw()
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    title="Simpan Visualisasi BFS Tree Sebagai File Gambar Berformat PNG"
                )
                if file_path:
                    dot.render(file_path.rsplit('.', 1)[0], format='png', cleanup=True)
                    print(f"Visualisasi BFS Tree telah berhasil disimpan ke dalam '{file_path}'")
                else:
                    print("Operasi simpan dibatalkan.")
                    
        except Exception as exception:
            print(f"Terjadi kesalahan saat menghasilkan Pohon BFS atau BFS Tree: {exception}")
            
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
        

def print_menu_options():
    
    """
    Menampilkan menu interaktif untuk para pengguna program.
    """
    
    print("\n========== Menu Operasi Graf Untuk Program Nomor 1 ===========================")
    print("1. Tambah Node Baru ➕")
    print("2. Tambah DIRECTED EDGE Baru ➡️")
    print("3. Tampilkan Representasi Dari Konfigurasi Data Graf Yang Termuat Saat Ini 🖼️")
    print("4. Lakukan Traversal Depth-First Search (DFS) dan Buat DFS Forest 🌲")
    print("5. Lakukan Traversal Breadth-First Search (BFS) dan Buat BFS Tree 🌳")
    print("6. Simpan (SAVE) Konfigurasi Data Graf Yang Termuat Saat Ini Ke Dalam File GraphViz .DOT 💾")
    print("7. Muatkan (LOAD) Konfigurasi Data Graf Dari File GraphViz .DOT 📂")
    print("8. Tampilkan Representasi ADJACENCY LIST Dari Konfigurasi Data Graf Yang Termuat Saat Ini 📜")
    print("9. Clear Konfigurasi Data Graf Yang Sedang Termuat Saat Ini 🔄")
    print("10. Keluar Dari Sini dan Hentikan Program ❌")
    print("==============================================================================\n")


def main():
    
    graph = Graph()
    
    print("")
    
    print("Selamat datang di Program Operasi Graf Untuk Nomor 1! 🌐")
    
    loadOnStartup = input("Apakah Anda ingin memuat konfigurasi data graf yang sudah ada dari file GraphViz .DOT? (y/N): ").strip().lower()
    
    if loadOnStartup.startswith('y'):
        graph.load_graph_from_dot_file()
        
    programIsRunning = True
    
    while programIsRunning:
        
        print_menu_options()
        
        choice = input("Silakan masukkan pilihan Anda (1-10): ")
        
        if choice == '1':
            
            node_name = input("Masukkan nama node baru yang akan ditambahkan ke graf saat ini: ").strip()
            
            if node_name:
                graph.add_node(node_name)
                
            else:
                print("Nama node baru TIDAK BOLEH kosong. Silakan coba lagi.")
                
        elif choice == '2':
            
            if not graph.adjacency_list:
                print("Graf saat ini masih kosong. Silakan tambahkan node baru terlebih dahulu sebelum menambahkan edge.")
                continue
            
            from_node = input("Masukkan nama node asal yang sudah ada untuk edge terarah: ").strip()
            to_node = input("Masukkan nama node tujuan yang sudah ada untuk edge terarah: ").strip()
            
            if from_node and to_node:
                graph.add_edge(from_node, to_node)
                
            else:
                print("Nama node asal dan tujuan TIDAK BOLEH kosong. Silakan coba lagi.")
                
        elif choice == '3':
            
            if not graph.adjacency_list:
                print("Graf saat ini masih kosong. Silakan tambahkan node baru dan edge ke dalam graf terlebih dahulu sebelum mencoba menampilkan graf.")
                continue
            
            save_option = input("Apakah Anda ingin menyimpan visualisasi data graf yang sedang dimuat ke dalam file gambar berformat PNG? (y/N): ").strip().lower()
            
            graph.display_graph(save_to_file=save_option.startswith('y'))
            
        elif choice == '4':
            
            if not graph.adjacency_list:
                print("Graf saat ini masih kosong. Silakan tambahkan node baru dan edge ke dalam graf terlebih dahulu sebelum melakukan traversal DFS.")
                continue
            
            graph.print_adjacency_list()
            
            dfs_starting_node = input("Masukkan nama node awal untuk traversal DFS: ").strip()
            
            if not dfs_starting_node:
                print("Nama node awal untuk traversal DFS TIDAK BOLEH kosong. Silakan coba lagi.")
                continue
            
            else:
                graph.generate_dfs_forest(dfs_starting_node)
                
        elif choice == '5':
            
            if not graph.adjacency_list:
                print("Graf saat ini masih kosong. Silakan tambahkan node baru dan edge ke dalam graf terlebih dahulu sebelum melakukan traversal BFS.")
                continue
            
            graph.print_adjacency_list()
            
            bfs_starting_node = input("Masukkan nama node awal untuk traversal BFS: ").strip()
            
            if not bfs_starting_node:
                print("Nama node awal untuk traversal BFS TIDAK BOLEH kosong. Silakan coba lagi.")
                continue
            
            else:
                graph.generate_bfs_tree(bfs_starting_node)
                
        elif choice == '6':
            
            graph.save_graph_to_dot_file()
            
        elif choice == '7':
            
            graph.load_graph_from_dot_file()
            
        elif choice == '8':
            
            if not graph.adjacency_list:
                print("Graf saat ini masih kosong. Silakan tambahkan node baru dan edge ke dalam graf terlebih dahulu sebelum menampilkan adjacency list.")
                continue
            
            graph.print_adjacency_list()
            
        elif choice == '9':
            
            graph.clear_graph_data_configuration()
            
        elif choice == '10':
            
            save_choice = input("Apakah Anda ingin menyimpan konfigurasi data graf yang sedang dimuat ke dalam file GraphViz .DOT terlebih dahulu sebelum keluar? (y/N): ").strip().lower()
            
            if save_choice.startswith('y'):
                graph.save_graph_to_dot_file()
                
            print("Saatnya keluar dari aplikasi graf. Sampai jumpa di sesi berikutnya! 👋")
            
            programIsRunning = False
            
            print("")
            
            break
        
        else:
            
            print("Pilihan tidak valid. Silakan masukkan nomor antara 1 dan 8.")

if __name__ == "__main__":
    main()