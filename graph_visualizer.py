from py2neo import Graph
import matplotlib.pyplot as plt
import networkx as nx
import os

class GraphVisualizer:
    def __init__(self, uri, user, password, database):
        self.graph = Graph(uri, auth=(user, password), name=database)

    def visualize_graph(self, output_file):
        query = """
        MATCH (n)-[r]->(m)
        RETURN n.name AS from, type(r) AS relationship, m.name AS to
        """
        data = self.graph.run(query).data()

        G = nx.DiGraph()
        for record in data:
            G.add_edge(record['from'], record['to'], label=record['relationship'])

        # Adjust layout parameters for spring layout
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

        plt.figure(figsize=(18, 18))  # Increase figure size
        nx.draw(G, pos, with_labels=False, node_color='skyblue', node_size=3000, edge_color='black', width=2.0, font_size=12, font_color='black', font_weight='bold')

        # Draw node labels with custom positions
        node_labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_color='black', font_weight='bold')

        # Draw edges
        edges = nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, width=1.0)

        # Draw edge labels with adjusted positions to avoid overlapping with nodes
        edge_labels = nx.get_edge_attributes(G, 'label')
        for edge, label in edge_labels.items():
            x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2
            y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2
            plt.text(x, y, label, fontsize=10, color='black', ha='center', va='center')


        plt.savefig(output_file)
        plt.show()

# Example usage
if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "Aniket60@"
    database = "scsdf"
    visualizer = GraphVisualizer(uri, user, password, database)
    
    # Define output file path
    output_folder = "output"
    output_file = os.path.join(output_folder, "graph_visualization.png")

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate and save the graph visualization
    visualizer.visualize_graph(output_file)
    print(f"Graph visualization saved to {output_file}")

