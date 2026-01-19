TYPE: project

TITLE: Log Ingestion and Analytics Dashboard

PROBLEM:
Application logs were generated across multiple services and environments, making monitoring, debugging, and analysis fragmented, manual, and inefficient.

SOLUTION:
Designed and developed a distributed log ingestion and analytics system to collect, stream, store, and visualize logs from multiple services in near real time.

TECH STACK:
Spring Boot, Kafka, MongoDB, Python, Streamlit

IMPACT:
- Centralized log collection across multiple services
- Improved fault tolerance and scalability for high-volume log ingestion
- Enabled faster debugging and operational monitoring through real-time analytics

DETAILS:
The system uses Spring Boot services to generate logs, Kafka for buffering and streaming multi-level logs, MongoDB for indexed log storage, and a Streamlit-based dashboard for interactive filtering, visualization, and service health monitoring.