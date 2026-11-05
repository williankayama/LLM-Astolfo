# Meet Astolfo! the AI Assistant!

A simple local AI assistant built with **Python and Ollama**, developed through *vibe coding* as a personal learning project.

The main goal of this project is to explore how Large Language Models (LLMs) work locally, experiment with AI memory systems, and understand how different technologies can be integrated to create a basic conversational assistant.

> **Disclaimer:** This project is experimental and was created strictly for educational and study purposes. It is not intended to be a production-ready AI system.

## 🚀 About the Project

This project is an attempt to build a simple AI assistant that runs locally, without relying on external AI APIs.

It uses Ollama to run language models and combines traditional database storage with vector-based semantic search to implement a persistent memory system.

The project was developed using *vibe coding*, with AI-assisted programming as part of the learning process.

## 🧠 Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Ollama | Local LLM execution |
| Qwen 2.5 3B | Conversational language model |
| EmbeddingGemma | Text embeddings |
| ChromaDB | Vector database and semantic search |
| SQLite | Persistent data and memory storage |

## ✨ Features

- **Local AI Chat:** Conversational interaction using locally hosted language models.
- **Streaming Responses:** Displays AI responses progressively as they are generated.
- **Persistent Conversation History:** Stores conversation messages using SQLite.
- **Automatic Memory:** Extracts potentially useful information from user messages.
- **Manual Memory Management:** Allows users to create and manage memories.
- **Semantic Search:** Uses embeddings and ChromaDB to retrieve relevant information based on meaning rather than exact keywords.
- **Memory Retrieval:** Provides relevant context to the AI during conversations.

### Available Commands

| Command | Description |
|---|---|
| `/buscar` (search) | Search stored memories |
| `/memorias` (memories) | Display saved memories |
| `/lembrar` (remember) | Manually save a memory |
| `/esquecer` (forget) | Remove a stored memory |
| `/reset` (reset) | Reset the conversation |

## 🏗️ Project Architecture

The application combines two different approaches to data storage:

- **SQLite:** Acts as the persistent storage for conversation history and memories.
- **ChromaDB:** Maintains a vector index used for semantic similarity searches.

The general workflow is:

1. The user sends a message.
2. The application processes the input.
3. Relevant memories are retrieved through semantic search.
4. The retrieved context is provided to the language model.
5. Ollama generates the response.
6. The conversation is stored in SQLite.
7. The memory system can extract relevant information from the user's message and update the vector database.

## 📁 Project Structure

```text
project/
│
├── assistant.py
├── memory.py
├── memory_manager.py
├── vector_memory.py
├── Modelfile
│
├── database/
│   ├── assistant.db
│   └── chroma/
│
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- Ollama
- Git

### 1. Clone the repository

```bash
cd ./your_repository
git clone https://github.com/williankayama/LLM-Astolfo.git
```

### 2. Install Python dependencies (venv)

```bash
pip install -r requirements.txt
```

### 3. Download the required models

Pull the conversational model:

```bash
ollama pull qwen2.5:3b
```

Pull the embedding model:

```bash
ollama pull embeddinggemma
```

### 4. Run the application

Make sure Ollama is running, then execute:

```bash
python assistant.py
```

## 🔬 Learning Objectives

This project serves as a practical experiment to explore:

- Local Large Language Model execution.
- Prompt engineering and model customization.
- AI-assisted software development.
- Embeddings and vector databases.
- Semantic similarity and information retrieval.
- Persistent memory architectures.
- Python database integration.
- Context management in conversational AI.

## ⚠️ Limitations

This is a learning project, and several limitations are expected:

- The language model may generate inaccurate or inconsistent responses.
- Automatic memory extraction may save irrelevant or incorrect information.
- Semantic search parameters are experimental and may require adjustments.
- Memory retrieval does not guarantee that the most relevant information will always be found.
- Performance depends on the available hardware and the models being used.

## 🎯 Project Status

<badge>Experimental / In Development</badge>

This project is continuously evolving as I explore new concepts and experiment with different approaches to local AI development.

The priority is not to build a perfect AI assistant, but to understand the technologies behind it, learn through experimentation, and improve the implementation over time.

The next steps will involve implementing a limited RAG (Retrieval-Augmented Generation) system, allowing the AI to access and retrieve information from selected local files. This will help evaluate its behavior when working with external knowledge sources, while also focusing on improving the accuracy, consistency, and overall quality of its responses.

---

**Built with Python, Ollama, curiosity, and a lot of vibe coding.**
