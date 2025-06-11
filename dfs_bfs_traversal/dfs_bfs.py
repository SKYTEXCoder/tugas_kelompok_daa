from collections import deque
import re, graphviz

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
        
    def display_graph(self, file_name):
        """Displays the current representation of the graph using Graphviz."""
        dot = graphviz.Digraph(comment='PNG Representation of the Current Graph')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='ellipse', color='orange', penwidth='3', style='solid')
        for node, edges in self.adjacency_list.items():
            for edge in edges:
                dot.edge(node, edge)
        dot.render(file_name, format='png', cleanup=True)
        print(f"A visualized representation of the currently-loaded graph data has been saved into a file named '{file_name}.png'.")

    def save_graph_to_dot_file(self, file_name):
        """Saves the current;y-loaded graph data into a GraphViz .DOT file."""
        try:
            with open(f"{file_name}.dot", "w") as file:
                file.write("digraph G {\n}")
                for node in self.adjacency_list:
                    file.write(f'    "{node}";\n')
                for node, edges in self.adjacency_list.items():
                    for edge in edges:
                        file.write(f'    "{node}" -> "{edge}";\n')
                file.write('}\n')
            print(f"The currently-loaded graph data has been successfully saved into '{file_name}.dot'.")
        except Exception as exception:
            print(f"An error has occured while trying to save the currently-loaded graph data into a GraphViz .DOT file: {exception}")

    def load_graph_from_dot_file(self, file_name):
        """Load a graph from a GraphViz .dot file."""
        try:
            with open(f'{file_name}.dot', 'r') as f:
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
            print(f"Graph data has been successfully loaded into the current instance of the program from '{file_name}.dot'.")
        except Exception as error:
            print(f"An error has occured while trying to load a graph data: {error}")

    def generate_dfs_forest(self, start_node=None):

        pass

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
            file_name = input("Please enter a valid filename for the PNG representation of the currently-loaded graph data (WITHOUT the extension) (Optional, leave blank for default): ").strip()
            if not file_name:
                file_name = "current_graph_representation"
            graph.display_graph(file_name)
        elif choice == '4':
            if not graph.adjacency_list:
                print("The current graph is still empty. Please add new nodes and edges into the graph first before performing DFS traversal.")
                continue
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
            bfs_starting_node = input("Enter the name of the starting node for BFS traversal: ").strip()
            if not bfs_starting_node:
                print("The name of the starting node for BFS traversal CANNOT be empty. Please try again.")
                continue
            else:
                graph.generate_bfs_tree(bfs_starting_node)
        elif choice == '6':
            file_name = input("Enter a valid filename to save the current graph data (WITHOUT the extension): ").strip()
            if file_name:
                graph.save_graph_to_dot_file(file_name)
            else:
                print("The name of the file CANNOT be empty. Please try again.")
        elif choice == '7':
            file_name = input("Enter a valid filename to load the graph data from (WITHOUT the extension): ").strip()
            if file_name:
                graph.load_graph_from_dot_file(file_name)
            else:
                print("The name of the file CANNOT be empty. Please try again.")
        elif choice == '8':
            print("Exiting the application. Goodbye! 👋")
            programIsRunning = False
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()