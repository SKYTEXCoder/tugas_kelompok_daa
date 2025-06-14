class Graph: 

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
    # (uses union by rank) 
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

        # An index variable, used for sorted edges 
        i = 0

        # An index variable, used for result[] 
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

            # Iterate dari weight yang paling kecil, set x untuk mencari parent dari u begitu pula dengan y dan v
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
        print("Sisi pada MST") 
        for u, v, weight in result: 
            minimumCost += weight 
            print("%d -- %d == %d" % (u, v, weight)) 
        print("Minimum Spanning Tree:", minimumCost) 


if __name__ == '__main__': 
    g = Graph(4) 
    g.addEdge(0, 1, 10)  
    g.addEdge(0, 2, 6) 
    g.addEdge(0, 3, 2) 
    g.addEdge(1, 3, 1) 
    g.addEdge(2, 3, 4) 

    # Lakukan algoritma 
    g.KruskalMST()