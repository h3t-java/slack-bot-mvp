# Slack RAG Bot MVP

## Description

**Slack RAG Bot MVP** is a Slack chatbot powered by a **retrieval-augmented generation (RAG) pipeline**.  

- The bot allows users to ask questions in a Slack channel.  
- If the question relates to **company documents** (e.g., vacation policies, IT guides, handbooks), it retrieves relevant content from a **vector database** and provides an answer.  
- If the question is **not covered by documents**, it falls back to a **general LLM answer**.  
- Answers include **source citations** for transparency.  

This bot is designed for **lightweight, production-ready deployment** on free cloud tiers like Railway, Render, or Fly.io.

---

## Architecture Overview

Slack RAG Bot workflow:

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

## Setup Locally

1. **Clone the repository**

``` git clone https://github.com/h3t-java/slack-bot-mvp.git ```
``` cd slack-bot-mvp ```

2. **Create a virtual enviroment**
``` python -m venv venv ```
``` source venv/bin/activate   # Linux/macOS ```
``` # venv\Scripts\activate    # Windows ```

3. **Install dependancies**
``` pip install -r requirements.txt ```

4. **Create .env file in project root**
``` SLACK_BOT_TOKEN=xoxb-your-slack-bot-token ```
``` LLM_API_KEY=sk-your-llm-api-key ```

5 **Add sample documents in data/documents/**
``` Example: employee_handbook.txt, company_faq.txt, it_support_guide.txt. ```

6 **Inject documents into Chroma DB**
``` python scripts/ingest_docs.py ```

7. **Run locally**
``` uvicorn main:app --reload --port 8000 ```
``` Webhook is available at http://localhost:8000/slack/events ```