**Neo4j Database Forensic Analysis and Visualization Tool**


This tool provides comprehensive forensic analysis and visualization for Neo4j databases. It includes functionalities for:

**Node and Relationship Analysis:** Summarizes database structure with counts of nodes and relationships.

**Log Analysis:** Detects anomalies and tracks IP addresses from log files.

**Configuration Analysis:** Identifies potential security vulnerabilities and optimization opportunities in Neo4j configurations.

**Query Log Analysis:** Extracts and analyzes queries from query logs.

**Graph Visualization:** Creates detailed visual representations of database structures and relationships.

Features

Retrieve and Summarize Graph Data: Get insights into node and relationship counts.
Analyze Logs: Detect anomalies and generate reports from log files.
Evaluate Neo4j Configuration: Check settings for security and optimization.
Query Log Analysis: Extract and analyze queries for performance and security insights.
Graph Visualization: Visualize database structures using NetworkX and Matplotlib.


Install Dependencies:

Make sure you have Python 3 installed. Install the required Python libraries using:

 *pip install -r requirements.txt*


Configure Settings:

Update configuration files with your Neo4j database details and log file paths.

Usage
Run Analysis:

To analyze graph data:

*python analyze_graph.py*


To analyze logs:

*python analyze_logs.py*


To evaluate Neo4j configuration:

*python analyze_config.py*


To perform query log analysis:

*python analyze_queries.py*


To visualize the graph:

*python visualize_graph.py*


Generate Full Analysis:

Execute the full analysis script to combine all features:

*python full_analysis.py*



**Results**

Analysis results will be saved in the output folder.
Visualizations will be saved as PNG files in the output folder.



**Challenges**

Integration with Neo4j: Addressed by thorough testing and debugging.
Handling large log files: Implemented efficient parsing and analysis techniques.



**Limitations**

Limited to Neo4j and the specific configuration settings and log formats supported.
Visualization may become cluttered with very large graphs.



**Future Work**

Expand support for additional database systems.
Enhance visualization capabilities for better scalability.
Implement automated alerts for detected anomalies.
