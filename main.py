import os
import json
from get_graph_info import GraphInfo
from analyze_logs import LogAnalyzer
from analyze_config import Neo4jConfigAnalyzer
from analyze_query_logs import QueryLogAnalyzer
from graph_visualizer import GraphVisualizer

def main():
    print("Choose an option:")
    print("1. Get node and relationship counts")
    print("2. Analyze logs")
    print("3. Analyze Neo4j configuration")
    print("4. Analyze query logs")
    print("5. Graph visualization")  # New option
    print("6. Full analysis")  # New option
    choice = input("Enter your choice: ")

    if choice == "1":
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = "Aniket60@"
        database = "scsdf"

        graph_info = GraphInfo(uri, user, password, database)
        info = graph_info.get_node_relationship_counts()
        graph_info.close()

        output_folder = "output"
        output_file_path = os.path.join(output_folder, "graph_info.json")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(output_file_path, 'w') as output_file:
            json.dump(info, output_file, indent=4)

        print(f"Graph information saved to {output_file_path}")

    elif choice == "2":
        log_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/logs/neo4j.log"
        analyzer = LogAnalyzer(log_file_path)
        log_analysis, ips = analyzer.analyze_logs()

        output_folder = "output"
        output_file_path = os.path.join(output_folder, "log_analysis.json")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(output_file_path, 'w') as output_file:
            json.dump(log_analysis, output_file, indent=4)

        print(f"Log analysis saved to {output_file_path}")

    elif choice == "3":
        config_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/conf/neo4j.conf"
        analyzer = Neo4jConfigAnalyzer(config_file_path)
        security_issues = analyzer.analyze_config()

        output_folder = "output"
        output_file_path = os.path.join(output_folder, "config_analysis.json")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(output_file_path, 'w') as output_file:
            json.dump(security_issues, output_file, indent=4)

        print(f"Config analysis saved to {output_file_path}")

    elif choice == "4":
        query_log_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/logs/query.log"
        analyzer = QueryLogAnalyzer(query_log_file_path)
        query_analysis = analyzer.analyze_query_logs()

        output_folder = "output"
        output_file_path = os.path.join(output_folder, "query_analysis.json")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(output_file_path, 'w') as output_file:
            json.dump(query_analysis, output_file, indent=4)

        print(f"Query analysis saved to {output_file_path}")

    elif choice == "5":
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = "Aniket60@"
        database = "scsdf" 

        visualizer = GraphVisualizer(uri, user, password, database)

        output_folder = "output"
        output_file = os.path.join(output_folder, "graph_visualization.png")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        visualizer.visualize_graph(output_file)
        print(f"Graph visualization saved to {output_file}")

    elif choice == "6":
        # Perform full analysis combining all features
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = "Aniket60@"

        # Perform node and relationship counts analysis
        graph_info = GraphInfo(uri, user, password, "scsdf")
        node_relationship_counts = graph_info.get_node_relationship_counts()
        graph_info.close()

        # Perform log analysis
        log_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/logs/neo4j.log"
        log_analyzer = LogAnalyzer(log_file_path)
        log_analysis, ips = log_analyzer.analyze_logs()

        # Perform configuration analysis
        config_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/conf/neo4j.conf"
        config_analyzer = Neo4jConfigAnalyzer(config_file_path)
        security_issues = config_analyzer.analyze_config()

        # Perform query log analysis
        query_log_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/logs/query.log"
        query_analyzer = QueryLogAnalyzer(query_log_file_path)
        query_analysis = query_analyzer.analyze_query_logs()

        # Perform graph visualization
        graph_visualizer = GraphVisualizer(uri, user, password, "scsdf")
        graph_output_file = os.path.join("output", "graph_visualization_full.png")
        graph_visualizer.visualize_graph(graph_output_file)

        # Save all analysis results to JSON files
        output_folder = "output"
        graph_info_file_path = os.path.join(output_folder, "graph_info.json")
        log_analysis_file_path = os.path.join(output_folder, "log_analysis.json")
        config_analysis_file_path = os.path.join(output_folder, "config_analysis.json")
        query_analysis_file_path = os.path.join(output_folder, "query_analysis.json")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(graph_info_file_path, 'w') as graph_info_file:
            json.dump(node_relationship_counts, graph_info_file, indent=4)

        with open(log_analysis_file_path, 'w') as log_analysis_file:
            json.dump(log_analysis, log_analysis_file, indent=4)

        with open(config_analysis_file_path, 'w') as config_analysis_file:
            json.dump(security_issues, config_analysis_file, indent=4)

        with open(query_analysis_file_path, 'w') as query_analysis_file:
            json.dump(query_analysis, query_analysis_file, indent=4)

        print("Full analysis completed. Results saved to:")
        print(f"- Graph info: {graph_info_file_path}")
        print(f"- Log analysis: {log_analysis_file_path}")
        print(f"- Config analysis: {config_analysis_file_path}")
        print(f"- Query analysis: {query_analysis_file_path}")
        print(f"- Graph visualization: {graph_output_file}")

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()

