from collections import deque
import re, graphviz
import tkinter as tk
from tkinter import filedialog

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        
    def add_node(self, node_name):
        if node_name not in self.adjacency_list:
            self.adjacency_list[node_name] = []
            print(f"Node '{node_name}' added.")
            return True
        else:
            print(f"Node '{node_name} already exists in the current graph.'")
            return False
        
    def add_edge(self, from_node, to_node):
        if from_node not in self.adjacency_list:
            print(f"Error: Origin Node '{from_node}' does not exist in the current graph. Cannot add an edge.")
            return False
        if to_node not in self.adjacency_list:
            print(f"Error: Destination Node '{to_node}' does not exist in the current graph. Cannot add an edge.")
            return False
        if to_node not in self.adjacency_list[from_node]:
            self.adjacency_list[from_node].append(to_node)
            print(f"Directed edge added from node '{from_node}' to node '{to_node}'.")
            return True
        else:
            print(f"An edge from '{from_node}' to '{to_node}' already exists.")
            return False
        
    def display_graph(self, save_to_file=False):
        """
        Displays the current representation of the graph using Graphviz.
        Optionally saves the graph to a PNG file if save_to_file is True.
        :param save_to_file: If True, saves the graph to a PNG file.
        """
        dot = graphviz.Digraph(comment='Graph Visualization', format='png')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='ellipse', color='orange', penwidth='3', style='solid', fontname='Arial', fontweight='bold')
        for node, edges in self.adjacency_list.items():
            dot.node(node)
            for edge in edges:
                dot.edge(node, edge)
        try:
            dot.view(cleanup=True)
            print("Graph visualization has been successfully opened in your default image viewer.")
            if save_to_file:
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    title="Save Graph Visualization As PNG"
                )
                if file_path:
                    dot.render(file_path.rsplit('.', 1)[0], format='png', cleanup=True)
                    print(f"Graph visualization has been successfully saved to '{file_path}'.")
                else:
                    print("Save operation cancelled.")
        except Exception as exception:
            print(f"An error occurred while trying to display/save the graph: {exception}")

    def save_graph_to_dot_file(self, file_name=None):
        """Saves the currently-loaded graph data into a GraphViz .DOT file using a file dialog."""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dot",
            filetypes=[("DOT files", "*.dot"), ("All files", "*.*")],
            title="Save Current Graph Data As A GraphViz .DOT File"
        )
        if not file_path:
            print("Save operation cancelled.")
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
            print(f"The currently-loaded graph data has been successfully saved into '{file_path}'.")
        except Exception as exception:
            print(f"An error has occured while trying to save the currently-loaded graph data into a GraphViz .DOT file: {exception}")

    def load_graph_from_dot_file(self, file_name=None):
        """Load a graph from a GraphViz .dot file using a file dialog."""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            defaultextension=".dot",
            filetypes=[("DOT files", "*.dot"), ("All files", "*.*")],
            title="Open Graph .DOT File"
        )
        if not file_path:
            print("Load operation cancelled.")
            return
        try:
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
                        if node not in self.adjacency_list:
                            self.adjacency_list[node] = []
                    elif edge_match:
                        from_node, to_node = edge_match.group(1), edge_match.group(2)
                        if from_node not in self.adjacency_list:
                            self.adjacency_list[from_node] = []
                        if to_node not in self.adjacency_list:
                            self.adjacency_list[to_node] = []
                        if to_node not in self.adjacency_list[from_node]:
                            self.adjacency_list[from_node].append(to_node)
            print(f"Graph data has been successfully loaded into the current instance of the program from '{file_path}'.")
        except Exception as error:
            print(f"An error has occured while trying to load a graph data file: {error}")
            
    def print_adjacency_list(self):
        """Prints the current adjacency list representation of the graph."""
        print("")
        if not self.adjacency_list:
            print("The current graph is empty.")
            return
        print("Current Adjacency List Representation of the Graph:")
        for node, edges in self.adjacency_list.items():
            print(f"{node}: {', '.join(edges) if edges else 'NO EDGES/CONNECTIONS'}")
        print("")

    def generate_dfs_forest(self, start_node=None):
        """
        Performs Depth-First Search (DFS) traversal starting from the specified node and generates a DFS forest visualization with specific edge classifications.
        Edge types:
        - T: Tree Edges (Edges that are used in the DFS traversal)
        - B: Back Edges (Edges that point a descendant node to an ancestor node)
        - F: Forward Edges (Edges that point an ancestor node to a descendant node)
        - C: Cross Edges (Any other edges that do not fit the above categories)
        :param start_node: The node from which to start the DFS traversal. If None, starts from any unvisited node.
        """
        
        if not self.adjacency_list:
            print("The current graph is empty. Cannot perform DFS traversal.")
            return
        
        if start_node not in self.adjacency_list:
            print(f"Error: Start node '{start_node}' does not exist in the currently-loaded graph data.")
            return
        
        discovery_times = {}
        finishing_times = {}
        edge_types = {}
        time = [0]
        
        def dfs_visit(node, parent=None):
            time[0] += 1
            discovery_times[node] = time[0]
            
            for neighbor in self.adjacency_list[node]:
                edge = (node, neighbor)
                
                if neighbor not in discovery_times:
                    edge_types[edge] = 'T'
                    dfs_visit(neighbor, node)
                else:
                    if neighbor not in finishing_times:
                        edge_types[edge] = 'B'
                    else:
                        if discovery_times[neighbor] > discovery_times[node]:
                            edge_types[edge] = 'F'
                        else:
                            edge_types[edge] = 'C'
                            
            time[0] += 1
            finishing_times[node] = time[0]
            
        dfs_visit(start_node)
        
        dot = graphviz.Digraph(comment='DFS Forest', format='png')
        dot.attr(rankdir='LR')
        
        for node in self.adjacency_list:
            if node in discovery_times:
                label = f"{node}\n{discovery_times[node]}/{finishing_times[node]}"
                dot.node(node, label, shape='circle', color='orange', style='filled', fillcolor='lightblue')
            else:
                dot.node(node, node, shape='circle', color='gray')
        
        edge_colors = {'T': 'black', 'B': 'gold', 'F': 'red', 'C': 'blue'}
        for (source, destination), edge_type in edge_types.items():
            dot.edge(source, destination, label=edge_type, color=edge_colors[edge_type], fontcolor=edge_colors[edge_type], penwidth='2')
        
        try:
            dot.view(cleanup=True)
            print(f"\nThe DFS Forest has been successfully generated and opened in your default image viewer. Starting from node '{start_node}'.")
            print("Edge classifications:")
            print("T: Tree Edges (Black)")
            print("B: Back Edges (Gold)")
            print("F: Forward Edges (Red)")
            print("C: Cross Edges (Blue)")
            
            save_option = input("Would you like to save the DFS forest visualization into a file? (y/N): ").strip().lower()
            if save_option.startswith('y'):
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    title="Save DFS Forest Visualization As PNG"
                )
                if file_path:
                    dot.render(file_path.rsplit('.', 1)[0], format='png', cleanup=True)
                    print(f"DFS forest visualization has been successfully saved into '{file_path}'")
                else:
                    print("Save operation cancelled.")
        except Exception as exception:
            print(f"An error has occured while generating the DFS forest: {exception}")

    def generate_bfs_tree(self, start_node=None):

        pass


def print_menu_options():
    """Prints the interactive menu options for the program's user."""
    print("\n========== Graph Operations Menu ==========")
    print("1. Add A New Node ➕")
    print("2. Add A New Edge ➡️")
    print("3. Display The Current Representation Of The Graph 🖼️")
    print("4. Perform Depth-First Search (DFS) Traversal and Create A DFS Forest 🌲")
    print("5. Perform Breadth-First Search (BFS) Traversal and Create A BFS Tree 🌳")
    print("6. Save The Current Graph Data To A GraphViz .DOT File 💾")
    print("7. Load Graph Data From A GraphViz .DOT File 📂")
    print("8. Fully Exit & Terminate The Whole Program ❌")
    print("============================================\n")


def main():
    graph = Graph()
    print("Welcome to the Graph Operations Program! 🌐")
    programIsRunning = True
    while programIsRunning:
        print_menu_options()
        choice = input("Please enter your choice (1-8): ")
        
        if choice == '1':
            node_name = input("Enter the name of the new node to be added into the current graph: ").strip()
            if node_name:
                graph.add_node(node_name)
            else:
                print("The name of the new node CANNOT be empty. Please try again.")
        elif choice == '2':
            if not graph.adjacency_list:
                print("The current graph is still empty. Please add new nodes first before adding edges.")
                continue
            from_node = input("Enter the name of the already-existing origin node for the directed edge: ").strip()
            to_node = input("Enter the name of the already-existing destination node for the directed edge: ").strip()
            if from_node and to_node:
                graph.add_edge(from_node, to_node)
            else:
                print("The names of the origin and the destination nodes CANNOT be empty. Please try again.")
        elif choice == '3':
            if not graph.adjacency_list:
                print("The current graph is still empty. Please add new nodes and edges into the graph first before even trying to display the graph.")
                continue
            save_option = input("Would you like to save the visualization of the currently-loaded graph data into a file? (y/N): ").strip().lower()
            graph.display_graph(save_to_file=save_option.startswith('y'))
        elif choice == '4':
            if not graph.adjacency_list:
                print("The current graph is still empty. Please add new nodes and edges into the graph first before performing DFS traversal.")
                continue
            graph.print_adjacency_list()
            dfs_starting_node = input("Enter the name of the starting node for DFS traversal: ").strip()
            if not dfs_starting_node:
                print("The name of the starting node for DFS traversal CANNOT be empty. Please try again.")
                continue
            else:
                graph.generate_dfs_forest(dfs_starting_node)
        elif choice == '5':
            if not graph.adjacency_list:
                print("The current graph is still empty. Please add new nodes and edges into the graph first before performing BFS traversal.")
                continue
            graph.print_adjacency_list()
            bfs_starting_node = input("Enter the name of the starting node for BFS traversal: ").strip()
            if not bfs_starting_node:
                print("The name of the starting node for BFS traversal CANNOT be empty. Please try again.")
                continue
            else:
                graph.generate_bfs_tree(bfs_starting_node)
        elif choice == '6':
            graph.save_graph_to_dot_file()
        elif choice == '7':
            graph.load_graph_from_dot_file()
        elif choice == '8':
            print("Exiting the application. Goodbye! 👋")
            programIsRunning = False
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()