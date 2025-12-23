
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
```
User Upload → Document Processing → Text Chunking → OpenAI Embeddings 
→ Pinecone Vector DB → Semantic Search → Context Retrieval → GPT-4 → Answer
```

### RAG Pipeline

1. **Ingestion**: Documents are chunked (1000 chars, 200 overlap) and converted to 1024-dim embeddings
2. **Storage**: Embeddings stored in Pinecone with metadata (source, user_id)
3. **Retrieval**: Query converted to embedding, top-k similar chunks retrieved via cosine similarity
4. **Generation**: Retrieved context injected into GPT-4 prompt for answer generation

## 🛠️ Tech Stack

- **Backend**: Python 3.10+
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4-mini
- **Vector DB**: Pinecone (1024-dim embeddings)
- **Embeddings**: OpenAI text-embedding-3-small
- **Document Processing**: PyPDF2

## 📦 Installation

### Prerequisites

- Python 3.10+
- OpenAI API key
- Pinecone API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/interview-rag.git
cd interview-rag
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

5. **Set up Pinecone index**

- Go to [Pinecone Console](https://app.pinecone.io/)
- Create a new index:
  - Name: `interview-rag`
  - Dimensions: `1024`
  - Metric: `cosine`

## 🚀 Usage

### Run the Streamlit app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Upload Documents

1. Navigate to "📤 Upload Documents"
2. Upload your resume, project descriptions, or any relevant documents
3. Click "🚀 Upload & Process"

### Ask Questions

1. Navigate to "💬 Ask Questions"
2. Type your interview question (e.g., "Tell me about my distributed systems experience")
3. Get an AI-generated answer based on your uploaded documents

### Command Line Testing

For quick testing without the UI:
```bash
python test_rag.py
```

## 📁 Project Structure
```
interview-rag/
├── app.py                 # Streamlit UI
├── rag_engine.py          # Core RAG logic (search, generate)
├── ingest.py              # Initial bulk document ingestion
├── test_rag.py            # CLI testing script
├── data/                  # Local documents for initial upload
│   ├── resume.txt
│   ├── projects.txt
│   └── technical_skills.txt
├── .env                   # Environment variables (not in git)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Adjust Chunk Size

In `rag_engine.py`:
```python
def chunk_text(text, chunk_size=1000, overlap=200):
    # Modify chunk_size and overlap as needed
```

### Change Retrieval Count

In `rag_engine.py`:
```python
def search_documents(query, top_k=5):  # Increase top_k for more context
```

### Swap LLM Model

In `rag_engine.py`:
```python
response = openai_client.chat.completions.create(
    model="gpt-4o",  # Change to gpt-4, gpt-3.5-turbo, etc.
    ...
)
```

## 📊 Performance

- **Embedding Generation**: ~100ms per chunk
- **Search Latency**: <50ms (Pinecone)
- **Answer Generation**: 1-3 seconds (GPT-4)
- **Total Response Time**: ~2-4 seconds

## 🚢 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
5. Deploy!

### Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`

### Docker (Advanced)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t interview-rag .
docker run -p 8501:8501 --env-file .env interview-rag
```

## 🎓 How It Works

### What is RAG?

Retrieval-Augmented Generation combines:
- **Retrieval**: Finding relevant information from a knowledge base
- **Generation**: Using that information to generate accurate responses

### Why RAG?

- ✅ Reduces hallucinations (answers grounded in your documents)
- ✅ Up-to-date information (no training required)
- ✅ Source attribution (see where answers come from)
- ✅ Cost-effective (no fine-tuning needed)

### Technical Deep Dive

1. **Document Processing**: Text is split into semantic chunks
2. **Vectorization**: Each chunk becomes a 1024-dimensional vector
3. **Similarity Search**: Query vector finds most similar document vectors
4. **Context Injection**: Top-k chunks added to GPT-4 prompt
5. **Answer Generation**: GPT-4 generates answer using provided context

## 🔮 Future Enhancements

- [ ] **User Authentication**: Add login/signup with Streamlit-authenticator or Supabase
- [ ] **Conversation History**: Track past questions and answers
- [ ] **Export to PDF**: Save Q&A sessions for offline review
- [ ] **Fine-tuning**: Optional fine-tuning on personal communication style
- [ ] **Multi-modal**: Support for images, code snippets, diagrams
- [ ] **Analytics Dashboard**: Track most-asked questions, usage stats
- [ ] **Mobile App**: React Native or Flutter mobile client
- [ ] **Voice Interface**: Speech-to-text for practice interviews
- [ ] **Collaborative Mode**: Share knowledge bases with teammates

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Use Cases

- **Interview Preparation**: Practice answering technical interview questions
- **Resume Enhancement**: Quickly recall project details and achievements
- **Career Coaching**: Help career coaches understand client backgrounds
- **Academic Research**: Organize and query research papers and notes
- **Sales Enablement**: Sales teams answering product questions
- **Customer Support**: Support agents accessing knowledge bases

## ⚠️ Limitations

- **Context Window**: Limited by GPT-4's context window (4k-8k tokens)
- **Cost**: OpenAI API calls incur costs (~$0.01-0.05 per query)
- **Accuracy**: Dependent on document quality and completeness
- **Latency**: 2-4 second response time (not real-time)

## 🔒 Security & Privacy

- All documents stored in Pinecone with user isolation
- API keys stored in environment variables
- No data sharing between users
- HTTPS recommended for production deployment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Shri**
- University of Wisconsin-Madison
- Computer Science & Data Science
- [GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- OpenAI for GPT-4 and embeddings API
- Pinecone for vector database
- Streamlit for rapid UI development
- LangChain community for RAG best practices

## 📧 Contact

For questions or feedback, please [open an issue](https://github.com/yourusername/interview-rag/issues) or reach out via email.

---

**⭐ If you found this project helpful, please give it a star!**
