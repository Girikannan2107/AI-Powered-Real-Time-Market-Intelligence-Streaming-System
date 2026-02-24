# 🚀 AI-Powered Real-Time Market Intelligence Streaming System

A distributed, real-time market intelligence platform built using **Apache Kafka, Pathway, FastAPI, Docker, and RAG architecture**.

This system streams live stock market data and news headlines, processes them through a real-time streaming engine, performs sentiment analysis, and generates predictive insights — all in an event-driven microservices architecture.

---

## 🧠 System Overview

The platform ingests:

- 📈 Live stock market data (Alpha Vantage API)
- 📰 Streaming news headlines
- 🤖 Sentiment processing via AI agents
- 🔮 Real-time prediction generation
- 🌐 API access for UI/dashboard integration

Everything is containerized and orchestrated using Docker Compose.

---

## 🏗 Architecture

### Components:

- **Market Producer** → Streams live stock prices
- **News Producer** → Streams news data
- **Kafka** → Event streaming backbone
- **Pathway Engine** → Real-time processing
- **RAG Service** → Contextual intelligence layer
- **FastAPI** → Exposes live insights
- **Docker Compose** → Service orchestration

---

## ⚙ Tech Stack

- 🐍 Python 3.10
- ⚡ Apache Kafka
- 🔄 Pathway (Streaming Engine)
- 🚀 FastAPI
- 🐳 Docker & Docker Compose
- 🧠 OpenAI API (RAG / AI)
- 📊 Alpha Vantage API

---

## ✨ Features

✔ Real-time event-driven architecture  
✔ Streaming stock market ingestion  
✔ News sentiment processing  
✔ Prediction topic publishing  
✔ Microservice-based design  
✔ Fully Dockerized deployment  
✔ Scalable architecture  

---


---

## 🔐 Environment Setup

Create a `.env` file in the root directory:
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_KEY=your_alpha_vantage_key

⚠ Never commit `.env` to GitHub.

---

## 🚀 Run the System

```bash
docker-compose up --build


