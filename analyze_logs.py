import re
import json

class LogAnalyzer:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def analyze_logs(self):
        startup_events = []
        shutdown_events = []
        config_changes = []
        error_logs = []
        warning_logs = []
        ips = set()

        with open(self.log_file_path, 'r') as file:
            for line in file:
                log_entry, ip = self.parse_log_line(line)
                ip = ip or ""  # Handle None value
                ips.add(ip)

                if "Starting" in log_entry['message']:
                    startup_events.append(log_entry)
                elif "Stopping" in log_entry['message']:
                    shutdown_events.append(log_entry)
                elif "deprecated setting" in log_entry['message']:
                    config_changes.append(log_entry)
                elif "ERROR" in log_entry['message']:
                    error_logs.append(log_entry)
                elif "WARN" in log_entry['message']:
                    warning_logs.append(log_entry)
                

        return {
            "startup_events": startup_events,
            "shutdown_events": shutdown_events,
            "config_changes": config_changes,
            "error_logs": error_logs,
            "warning_logs": warning_logs,
        }, list(ips)

    def parse_log_line(self, line):
        log_pattern = re.compile(r'(?P<message>.+)')
        match = log_pattern.match(line)
        if match:
            log_entry = match.groupdict()
            ip = self.extract_ip(log_entry['message'])
            return log_entry, ip
        else:
            return {"message": line.strip()}, None

    def extract_ip(self, message):
        ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        match = ip_pattern.search(message)
        if match:
            return match.group()
        else:
            return None

# Example usage
if __name__ == "__main__":
    log_file_path = "/home/aniket/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-efa94084-d5f8-424e-869f-33830582bdd3/logs/neo4j.log"
    analyzer = LogAnalyzer(log_file_path)
    log_analysis, ips = analyzer.analyze_logs()

    # Define output folder and file path
    output_folder = "output"
    output_file_path = os.path.join(output_folder, "neo4j_logs.json")

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save Neo4j logs analysis to a JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(log_analysis, output_file, indent=4)

    print(f"Neo4j logs analysis saved to {output_file_path}")

    # Print extracted IP addresses
    print("\nIP addresses extracted from logs:")
    for ip in ips:
        print(ip)

