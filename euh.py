import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
import PyPDF2
import time

load_dotenv()

# Initialize
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("interview-rag")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    """Get 1024-dim embedding from OpenAI"""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=1024
    )
    return response.data[0].embedding

def chunk_text(text, chunk_size=1000, overlap=200):
    """Simple text chunking"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def read_pdf(filepath):
    """Read PDF file"""
    with open(filepath, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def read_text_file(filepath):
    """Read text file"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

# Load all documents from data/
print("📂 Loading documents from data/...")
all_chunks = []

for root, dirs, files in os.walk('data/'):
    for file in files:
        filepath = os.path.join(root, file)
        print(f"  Reading: {file}")
        
        try:
            if file.endswith('.pdf'):
                text = read_pdf(filepath)
            elif file.endswith(('.txt', '.md', '.py', '.js', '.json')):
                text = read_text_file(filepath)
            else:
                print(f"  ⚠️ Skipping {file} (unsupported format)")
                continue
            
            # Chunk the text
            chunks = chunk_text(text)
            for chunk in chunks:
                if chunk.strip():  # Only add non-empty chunks
                    all_chunks.append({
                        'text': chunk,
                        'source': file
                    })
        except Exception as e:
            print(f"  ❌ Error reading {file}: {e}")

print(f"✅ Created {len(all_chunks)} chunks from documents")

# Upload to Pinecone
print("🚀 Uploading to Pinecone...")
vectors = []

for i, chunk in enumerate(all_chunks):
    embedding = get_embedding(chunk['text'])
    vectors.append({
        "id": f"doc_{i}",
        "values": embedding,
        "metadata": {
            "text": chunk['text'],
            "source": chunk['source']
        }
    })
    
    # Upload in batches of 100
    if len(vectors) >= 100:
        index.upsert(vectors=vectors)
        print(f"  ✅ Uploaded batch {(i//100) + 1}")
        vectors = []

# Upload remaining
if vectors:
    index.upsert(vectors=vectors)
    print(f"  ✅ Uploaded final batch")

print("✅ Done! Documents uploaded to Pinecone")

# Verify
time.sleep(2)
stats = index.describe_index_stats()
print(f"📊 Index now has {stats['total_vector_count']} vectors")