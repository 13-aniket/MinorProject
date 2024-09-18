from neo4j import GraphDatabase

class GraphInfo:
    def __init__(self, uri, user, password, database):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def get_node_relationship_counts(self):
        with self.driver.session(database=self.database) as session:
            result = session.run("MATCH (n) RETURN count(n) AS node_count")
            node_count = result.single()["node_count"]

            result = session.run("MATCH ()-[r]->() RETURN count(r) AS rel_count")
            rel_count = result.single()["rel_count"]

            # Retrieve node names
            node_names_result = session.run("MATCH (n) RETURN n.name AS name")
            node_names = [record["name"] for record in node_names_result]

            # Retrieve relationship types
            rel_types_result = session.run("MATCH ()-[r]->() RETURN type(r) AS rel_type")
            rel_types = [record["rel_type"] for record in rel_types_result]

            # Retrieve node properties
            node_properties_result = session.run("MATCH (n) RETURN properties(n) AS props")
            node_properties = [record["props"] for record in node_properties_result]

            return {
                "node_count": node_count,
                "relationship_count": rel_count,
                "node_names": node_names,
                "relationship_types": rel_types,
                "node_properties": node_properties
            }

# Example usage
if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "Aniket60@"
    database = "scsdf"

    graph_info = GraphInfo(uri, user, password, database)
    info = graph_info.get_node_relationship_counts()
    print(info)
    graph_info.close()

