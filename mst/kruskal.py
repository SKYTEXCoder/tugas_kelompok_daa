from graphviz import Graph

class MyGraph: 

    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = [] 

    # Method untuk menambah edge
    def addEdge(self, u, v, w): 
        self.graph.append([u, v, w]) 

    # Method untuk mencari root dari i dan update parent dari setiap node yang ditrace ke final parent (path compression)
    def find(self, parent, i): 
        if parent[i] != i: 

            # Reassign current parent ke final parent supaya proses mencari parent dari node lebih cepat
            parent[i] = self.find(parent, parent[i]) 
        return parent[i] 

    # Method untuk merge dua set
    def union(self, parent, rank, x, y): 

        # Merge set yang rank nya lebih kecil ke set yang lebih besar
        if rank[x] < rank[y]: 
            parent[x] = y 
        elif rank[x] > rank[y]: 
            parent[y] = x 

        # Jika rank dua set sama, buat yang satunya root dari yang lain dan increment rank dengan 1
        else: 
            parent[y] = x 
            rank[x] += 1

    # Fungsi mencari MST dengan algoritma kruskal
    def KruskalMST(self): 

        # Array untuk hasil MST
        result = [] 

        # Index untuk sorted edges
        i = 0

        # Index untuk iterasi  node mst
        e = 0

        # Urutkan sisi sesuai weight dari yang paling kecil
        self.graph = sorted(self.graph, key=lambda item: item[2]) 

        parent = [] 
        rank = [] 

        # Buat node sesuai dengan jumlah node dan rank awal (0) 
        for node in range(self.V): 
            parent.append(node) 
            rank.append(0) 

        # Jumlah node MST pasti berjumlah v - 1 (v = jumlah node)
        while e < self.V - 1: 

            # Iterasi dari weight yang paling kecil, set x untuk mencari parent dari u begitu pula dengan y dan v
            u, v, w = self.graph[i] 
            i = i + 1
            x = self.find(parent, u) 
            y = self.find(parent, v) 

            # Jika parent dari kedua set itu tak sama maka append ke result dan lakukan union untuk update parent dan rank agar iterasi selanjutnya bisa optimal
            if x != y: 
                e = e + 1
                result.append([u, v, w]) 
                self.union(parent, rank, x, y) 
            # Jika sama jangan lakukan apapun karena jika dilakukan akan membuat cycle

        minimumCost = 0
        print("\nSisi pada MST") 
        for u, v, weight in result: 
            minimumCost += weight 
            print("%d -- %d == %d" % (u, v, weight)) 
        print("Minimum Spanning Tree:", minimumCost) 
        return result

def draw_graph_with_mst(all_edges, mst_edges, filename='graph_with_mst'):
    dot = Graph(comment='Graph with MST')

    for u, v, w in all_edges:
        if [u, v, w] in mst_edges or [v, u, w] in mst_edges:
            dot.edge(str(u), str(v), label=str(w), color='green', penwidth='2')
        else:  # non-MST edge
            dot.edge(str(u), str(v), label=str(w))

    dot.render(filename=filename, format='png', cleanup=True)

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

    g = MyGraph(v)
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

    # Lakukan algoritma 
    mst = g.KruskalMST()
    
    # Gambar graph
    draw_graph_with_mst(g.graph, mst, filename='kruskal_mst')