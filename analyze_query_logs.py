import re
import json

class QueryLogAnalyzer:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.query_keywords = ["EXPLAIN"]

    def analyze_query_logs(self):
        queries = []
        query_set = set()  # To keep track of unique queries
        with open(self.log_file_path, 'r') as file:
            entry_lines = []
            for line in file:
                if re.match(r'\d{4}-\d{2}-\d{2}', line) and entry_lines:
                    entry = ' '.join(entry_lines)
                    query = self.extract_query(entry)
                    if query and query not in query_set:
                        queries.append(query)
                        query_set.add(query)
                    entry_lines = [line.strip()]
                else:
                    entry_lines.append(line.strip())
            if entry_lines:
                entry = ' '.join(entry_lines)
                query = self.extract_query(entry)
                if query and query not in query_set:
                    queries.append(query)
                    query_set.add(query)
        return queries

    def extract_query(self, entry):
        query_pattern = re.compile(r'(\b(?:' + '|'.join(self.query_keywords) + r')\b.*?)(?= - \{\})')
        match = query_pattern.search(entry)
        if match:
            return match.group(1).strip()
        return None

# Example usage
if __name__ == "__main__":
    log_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/logs/query.log"  # Change this to your query log path
    analyzer = QueryLogAnalyzer(log_file_path)
    query_analysis = analyzer.analyze_query_logs()

    # Save query analysis to a JSON file
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_path = os.path.join(output_folder, "query_analysis.json")

    with open(output_file_path, 'w') as output_file:
        json.dump(query_analysis, output_file, indent=4)

    print(f"Query analysis saved to {output_file_path}")

