# Encrypted Permission-Based RAG System

A **modular, Retrieval-Augmented Generation (RAG)** system designed for **multi-user, permission-aware access** to private document collections.  
This system integrates encryption, secure retrieval, and agentic reasoning — enabling dynamic, context-driven query refinement and adaptive knowledge retrieval.

---

## Overview

This project implements a **secure and intelligent RAG pipeline** that:
- Ingests documents with **assigned permission levels**.
- Cleans and splits them into semantically meaningful **text chunks**.
- Generates **embeddings** using `MPNet` and indexes them in **FAISS**.
- Encrypts each chunk using **AES encryption** based on permission level.
- At query time, retrieves only the chunks that match or fall **below the user's permission level**.
- Uses a local **Mistral LLM** to refine vague queries, retrieve relevant information, and summarize results in a continuous **agentic feedback loop**.

---

## Core Workflow

### 1. Document Ingestion
- User uploads document(s) and assigns a permission level.
- The system processes, embeds, and encrypts chunks.
- FAISS index stores vectors + metadata; plaintext is never exposed.

### 2. Agentic Retrieval Loop
- User enters their **user ID** → system loads their permission level.
- Query is refined by the **Mistral agent** for clarity and precision.
- FAISS retrieves the top semantic matches.
- Only chunks within the user’s permission level are **decrypted**.
- Mistral summarizes and presents the refined answer.

### 3. Interactive Contextual Chat
- Conversation memory tracks all turns (queries, responses, refinements).
- Each new question is interpreted **in context**, allowing users to build on previous responses.


