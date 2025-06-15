import heapq
from graphviz import Graph

class PrimGraph:
    # Constructor, assign jumlah node dan array yang berisi tuple
    # setiap index merupakan node nya yang berisi adjacency list dari node tsb
    def __init__(self, vertices):
        self.V = vertices
        self.adj = [[] for _ in range(vertices)] 

    def addEdge(self, u, v, w):
        # Menambahkan edge dua arah
        # Contoh (1, 2, 5) menghubungkan node 1 dan 2 dan weight 5
        # adj[1] adalah node 1 maka tambahkan (2, 5) artinya terhubung dengan 2 dengan weight 5
        # begitu pula sebaliknya dengan v
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def primMST(self, start=0):
        # Array visited misal node ada 3, maka [False, False, False]
        visited = [False] * self.V

        # Array untuk store priority queue
        min_heap = []

        # Array result
        mst = []

        # Jumlah weight mst
        total_cost = 0

        # Inisisasi loop dengan start dari 0, tidak ada parent, dan weight 0
        heapq.heappush(min_heap, (0, start, -1))  # (weight, node yg dituju, node asal)

        # Looping sampai min_heap dan mst jumlah anggotanya node - 1
        while min_heap and len(mst) < self.V - 1:

            # Assign weight, u, parent dari min_heap awal
            weight, u, parent = heapq.heappop(min_heap)

            # Jika u yang adalah node dituju sudah divisit maka continue
            if visited[u]:
                continue

            # Buat index visited node u jadi True
            visited[u] = True

            # Jika parent tidak sama dengan -1 (-1 adalah node awal)
            # maka pop min_heap yang merupakan cheapest edge karena sudah di
            if parent != -1:
                mst.append((parent, u, weight))
                total_cost += weight

            # Iterasi semua tuple yang ada di current node dan cek apakah v
            # (node yang dituju) sudah divisit atau belum
            # jika belum maka push ke min_heap semua tuple itu
            for v, w in self.adj[u]:
                if not visited[v]:
                    heapq.heappush(min_heap, (w, v, u))

        if len(mst) != self.V - 1:
            print("Graf tidak terhubung!")
        else:
            print("\nSisi pada MST:")
            for u, v, w in mst:
                print(f"{u} -- {v} == {w}")
            print(f"Minimum Spanning Tree Cost: {total_cost}")

        return mst

def draw_graph_with_mst(adj_list, mst_edges, filename='prim_mst'):
    dot = Graph(comment='Graph with MST')
    mst_set = set(tuple(sorted((u, v))) for u, v, _ in mst_edges)
    added_edges = set()

    # Step 1: Draw full graph, mark MST edges in green, others in black
    for u in range(len(adj_list)):
        for v, w in adj_list[u]:
            edge_key = tuple(sorted((u, v)))
            if edge_key in added_edges:
                continue  # skip duplicate undirected edge

            if edge_key in mst_set:
                dot.edge(str(u), str(v), label=str(w), color='green', penwidth='2')
            else:
                dot.edge(str(u), str(v), label=str(w), color='black')

            added_edges.add(edge_key)

    # Step 2: Render the graph
    dot.render(filename=filename, format='png', cleanup=True)
    print(f'\nGraph saved as {filename}.png')

if __name__ == '__main__':
    while True:
        try:
            v = int(input('Masukkan jumlah node: '))
            if v >= 2:
                break;
            else:
                print('Jumlah node minimal 2!\n')
        except:
            print('Masukkan integer!\n')

    g = PrimGraph(v)

    print('\nMasukkan sisi, node pertama dimulai dari 0.\nPastikan node pada edge yang diinput tidak melebihi jumlah node yang sudah diinput.\nFormat input (node1 node2 weight)\nKetik \'done\' jika sudah\n',)
    while True:
        e = input('Masukkan edge: ')
        if e.lower() == 'done':
            break
        try:
            u, v, w = map(int, e.strip().split())
            g.addEdge(u, v, w)
        except:
            print('Format salah')
            
    mst = g.primMST(0)
    draw_graph_with_mst(g.adj, mst, filename='prim_mst')
