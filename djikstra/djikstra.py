import heapq
import os

def dijkstra(graph, start_node):
    # Inisialisasi jarak: 0 untuk node awal, tak terhingga (infinity) untuk lainnya
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0

    # Dictionary untuk merekonstruksi jalur
    previous_nodes = {node: None for node in graph}

    # Priority queue untuk menyimpan (jarak, node) yang akan dikunjungi
    # heapq adalah implementasi min-heap, cocok untuk Dijkstra
    priority_queue = [(0, start_node)]

    while priority_queue:
        # Ambil node dengan jarak terkecil dari priority queue
        current_distance, current_node = heapq.heappop(priority_queue)

        # Jika jarak yang diambil lebih besar dari yang sudah tercatat, abaikan
        if current_distance > distances[current_node]:
            continue

        # Iterasi melalui tetangga dari node saat ini
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Jika ditemukan jalur yang lebih pendek ke tetangga
            if distance < distances[neighbor]:
                # Update jarak dan node sebelumnya
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                # Masukkan tetangga ke priority queue dengan jarak barunya
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous_nodes

def get_path(previous_nodes, start_node, end_node):
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    # Balikkan path karena kita menelusuri dari akhir ke awal
    return ' -> '.join(path[::-1])

def input_graph():
    """
    Meminta input graf dari user.
    Format: jumlah node, nama node, jumlah edge, lalu edge (src dst bobot)
    """
    graph = {}
    n = int(input("Masukkan jumlah node: "))
    nodes = input("Masukkan nama node (pisahkan spasi): ").split()
    for node in nodes:
        graph[node] = {}
    m = int(input("Masukkan jumlah edge: "))
    print("Masukkan edge (format: asal tujuan bobot), contoh: s u 10")
    for _ in range(m):
        src, dst, w = input().split()
        graph[src][dst] = int(w)
    return graph

def write_dot(graph, previous_nodes, filename="graph.dot", highlight_tree=True):
    """
    Menulis file .dot untuk visualisasi graf dan pohon jalur terpendek.
    """
    with open(filename, "w") as f:
        f.write("digraph G {\n")
        # Semua edge
        for src in graph:
            for dst, w in graph[src].items():
                color = "black"
                if highlight_tree and previous_nodes[dst] == src:
                    color = "red"
                f.write(f'    {src} -> {dst} [label="{w}", color={color}];\n')
        f.write("}\n")

def generate_png(dot_file="graph.dot", png_file="graph.png"):
    """
    Menghasilkan file PNG dari file DOT menggunakan Graphviz.
    """
    os.system(f'dot -Tpng "{dot_file}" -o "{png_file}"')

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    print("Pilih input graf:")
    print("1. Default (graf contoh)")
    print("2. Input manual")
    pilihan = input("Pilihan (1/2): ")
    if pilihan == "2":
        graph = input_graph()
    else:
        graph = {
            's': {'u': 10, 'x': 5},
            'u': {'v': 1, 'x': 2},
            'v': {'y': 4},
            'x': {'u': 3, 'v': 9, 'y': 2},
            'y': {'s': 7, 'v': 6}
        }

    start_node = input(f"Masukkan node awal (default: s): ") or "s"
    shortest_distances, previous_path_nodes = dijkstra(graph, start_node)

    print(f"\nHasil Algoritma Dijkstra dari Node '{start_node}':\n")
    print("-" * 50)
    for node, distance in shortest_distances.items():
        if distance == float('infinity'):
            print(f"Node '{node}': Tidak dapat dijangkau")
        else:
            path = get_path(previous_path_nodes, start_node, node)
            print(f"Node '{node}':")
            print(f"  -> Jarak Terpendek: {distance}")
            print(f"  -> Jalur: {path}")
            print("-" * 50)
    
    # Menghitung total bobot dari sisi-sisi pohon jalur terpendek
    edge_weights = []
    for node, parent in previous_path_nodes.items():
        if parent is not None:
            weight = graph[parent][node]
            edge_weights.append(weight)

    weight_expression = " + ".join(str(w) for w in edge_weights)
    total_sp_tree_weight = sum(edge_weights)

    print(f"\nTotal Bobot pada Pohon Jalur Terpendek:")
    print(f"-> {weight_expression} = {total_sp_tree_weight}")

    # Tulis file .dot dan hasilkan PNG
    write_dot(graph, previous_path_nodes, filename="graph.dot", highlight_tree=True)
    print("\nFile DOT telah dibuat: graph.dot")
    print("Jika Graphviz terpasang, akan dibuat file PNG...")
    generate_png("graph.dot", "graph.png")
    print("File PNG (graph.png) telah dihasilkan (cek folder Anda).")