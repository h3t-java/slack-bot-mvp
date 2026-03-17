# Slack RAG Bot 🤖


https://github.com/user-attachments/assets/33d420a7-6bef-4d75-aff2-07da8e22c840


![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Slack Bot](https://img.shields.io/badge/Slack-Bot-4A154B?logo=slack&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Enabled-orange)
![ChromaDB](https://img.shields.io/badge/VectorDB-Chroma-purple)

## Description

**Slack RAG Bot MVP** is a Slack chatbot powered by a **retrieval-augmented generation (RAG) pipeline**.  

- The bot allows users to ask questions in a Slack channel.  
- If the question relates to **company documents** (e.g., vacation policies, IT guides, handbooks), it retrieves relevant content from a **vector database** and provides an answer.  
- If the question is **not covered by documents**, it falls back to a **general LLM answer**.  
- Answers include **source citations** for transparency.  

---

## Architecture Overview

![Slack RAG Bot Architecture](assets/architecture.png)

- **FastAPI** handles webhook and background tasks.  
- **Chroma DB** stores embeddings for documents.  
- **Sentence-Transformers** generates embeddings.  
- **LLM client** communicates with OpenAI-compatible or HuggingFace models.

---

## Features

- RAG: Answers based on company documents  
- Source citation for transparency  
- Background processing for Slack events (prevents retries)  
- Fallback to general LLM answers if documents are not relevant  
- Handles Slack app mentions in channels  

---

### Local startup with Docker

### 1. **Build the Docker image**

```bash
docker build -t slack-bot-mvp:latest .
```

### 2. **Run the container**
```bash
docker run -p 8000:8000 \
    -e SLACK_BOT_TOKEN="xoxb-your-slack-bot-token" \
    -e OPENROUTER_API_KEY="sk-your-llm-api-key" \
    slack-bot-mvp:latest
```
### 3. **Test Webhook is available at http://localhost:8000/slack/events**
