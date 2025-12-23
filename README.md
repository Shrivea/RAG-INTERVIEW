# 💼 Interview Prep RAG Assistant

An AI-powered interview preparation tool that uses Retrieval-Augmented Generation (RAG) to help you answer interview questions based on your personal documents, resume, and project descriptions.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.52+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-orange.svg)

## 🎯 Problem Statement

Preparing for technical interviews requires quickly recalling details from past projects, internships, and technical skills. This tool solves that by creating a searchable, AI-powered knowledge base of your professional experience that can generate contextually accurate interview responses on demand.

## ✨ Features

- **📤 Document Upload**: Upload resumes, project descriptions, and technical documents (PDF, TXT, MD, DOCX)
- **🔍 Semantic Search**: Uses OpenAI embeddings for intelligent document retrieval
- **🤖 AI-Powered Answers**: GPT-4 generates interview-ready responses based on your actual experience
- **📚 Source Attribution**: See which documents were used to generate each answer
- **💾 Persistent Storage**: Documents stored in Pinecone vector database for fast retrieval
- **👤 User Isolation**: Each user's data is kept separate (multi-tenant ready)

## 🏗️ Architecture
