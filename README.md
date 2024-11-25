# Corrective Retrieval Augmentation (CRAG) Implementation

Welcome to the repository for **Corrective Retrieval Augmentation (CRAG)**, a continuation of my exploration of Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), and Agent design. This project builds upon my initial efforts with RAG Agents, tackling one of the significant challenges in RAG workflows—**hallucination**, which occurs when an agent confidently generates incorrect or unrelated responses due to gaps in the retrieved context.

Inspired by the paper *"Corrective Retrieval Augmentation"* ([arXiv:2401.15884](https://arxiv.org/abs/2401.15884)), this implementation provides a novel approach to address hallucination by incorporating a corrective mechanism into the RAG framework. This journey not only deepened my understanding of LangChain's ecosystem but also explored practical solutions for building reliable and robust RAG Agents.

---

## Key Features and Concepts

### Problem Addressed
One major issue in traditional RAG Agents is their response to queries not covered in the retrieved documents. Without corrective measures, this often results in **hallucination**, where the agent fabricates information. CRAG introduces a method to self-reflect, grade retrieved documents, and take corrective steps, ensuring more reliable outputs.

### Tools and Frameworks Used
This implementation leverages the latest advancements in the LangChain ecosystem and related tools:

- **LangSmith**: A powerful tool for monitoring and evaluating application performance, allowing developers to iterate confidently and quickly.
- **LangGraph**: A library designed for building stateful, multi-actor applications with LLMs, facilitating agent and multi-agent workflows.
- **Cassandra (Graph Vector Database)**: Used to store document embeddings, enabling efficient and scalable retrieval.
- **Docker**: Simplifies the setup and deployment of the Cassandra database server.
- **OllamaEmbeddings**: Provides high-quality embeddings for text retrieval and similarity search.
- **OllamaLLM**: An open-source LLM running locally, ensuring privacy and flexibility.
- **Tavily**: A web search engine used to enhance retrieval capabilities with real-time external information.

---

## Implementation Design

### Architecture Overview
The implementation adopts a **multi-agent design** with the following characteristics:

1. **Supervisor Node**: Manages the overall state and passes it to individual agents for updates.
2. **Self-Reflection Mechanism**: Each agent grades the retrieved documents, determining their relevance and reliability.
3. **Corrective Workflow**: Based on the evaluation, agents decide the next steps, such as refining the query, invoking external search tools, or revisiting the document database.
4. **State Persistence**: The state of the workflow is preserved and updated at every step, enabling robust multi-agent collaboration.

---

## Project Setup

### Prerequisites
Ensure you have the following installed:

- Docker
- Python 3.9+
- Cassandra DB (via Docker)
- Required Python libraries (see [requirements.txt](./requirements.txt))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sadiksmart0/CRAG.git
   cd CRAG
   ```

2. Set up and run Cassandra with Docker:
   Installation and setup guide in Cassandra folder

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file with required settings (e.g., database credentials, API keys).

5. Run the application:
   ```bash
   python main.py
   ```

---

## Learning Highlights

This project was a significant milestone in my journey to master RAG systems. Key takeaways include:

- **LangChain Ecosystem**: Deepened understanding of LangChain's capabilities in building RAG apps and agents.
- **Multi-Agent Workflows**: Gained experience with LangGraph for managing stateful, distributed agent interactions.
- **Handling Hallucination**: Implemented corrective retrieval strategies inspired by cutting-edge research.
- **Tool Integration**: Leveraged multiple tools and frameworks to create a seamless, scalable solution.

---

## Acknowledgments

This project is inspired by the paper *Corrective Retrieval Augmentation* ([arXiv:2401.15884](https://arxiv.org/abs/2401.15884)). A special thanks to the creators of LangChain, LangSmith, LangGraph, Ollama, and the broader community contributing to the RAG ecosystem.

---

Happy exploring! Feedback and contributions are welcome. 🚀
