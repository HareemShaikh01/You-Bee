# 🐝 You-Bee — Your YouTube Companion Bot

![GitHub last commit](https://img.shields.io/github/last-commit/HareemShaikh01/You-Bee?color=brightgreen&style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)

> ⚡ **"You'll never watch YouTube the same way again!"**  
> Tired of scrubbing through long videos to find *one* answer? Now, just ask.  
> Meet **You-Bee**, your personal AI assistant for any YouTube video.

---

## ✨ What is You-Bee?

You-Bee is a browser assistant powered by RAG (Retrieval-Augmented Generation) that lets you **chat with any YouTube video**. It extracts transcripts, builds a vector store for memory, and gives you intelligent answers based on video content — all without wasting time.

---

## 🔥 Why I Built It

I was sick of endlessly watching long tutorial videos just to find that *one* line of explanation.  
So I thought: **What if I could just "ask" the video directly?**

That’s how You-Bee was born. Now, I never scroll through timelines — I *chat* with the content.

---

## 🧠 Tech Stack

### 🔹 Frontend
- React + TypeScript
- Tailwind CSS
- CRXJS for Chrome Extension

### 🔹 Backend
- FastAPI (Python)
- Langchain
- FAISS (vector store)
- Google Generative AI (gemini-pro)
- YouTube Transcript API

---

## ⚙️ How It Works

1. **YouTube video is loaded**
2. **Transcript is fetched**
3. **Transcript is split & embedded**
4. **FAISS vector store is built or reused from cache**
5. **User asks question**
6. **Langchain + Gemini responds contextually**

---

## 🛠️ Setup Guide

### 📁 1. Clone the Repo
```bash
git clone https://github.com/HareemShaikh01/You-Bee.git
cd YOU_BEE

```
---

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GOOGLE_API_KEY`

`LANGSMITH_TRACING`
`LANGSMITH_ENDPOINT`
`LANGSMITH_API_KEY`
`LANGSMITH_PROJECT`

---

Follow me  !!


