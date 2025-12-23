import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI

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

def search_documents(query, top_k=5):
    """Search Pinecone for relevant documents"""
    # Get embedding for the query
    query_embedding = get_embedding(query)
    
    # Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    # Extract relevant text chunks
    contexts = []
    for match in results['matches']:
        contexts.append({
            'text': match['metadata']['text'],
            'source': match['metadata']['source'],
            'score': match['score']
        })
    
    return contexts

def generate_answer(query, contexts):
    """Generate answer using GPT-4 with retrieved context"""
    
    # Build context string
    context_str = "\n\n".join([
        f"From {ctx['source']}:\n{ctx['text']}" 
        for ctx in contexts
    ])
    
    # Create prompt
    system_prompt = """You are an AI assistant helping Shri prepare for technical interviews. 
You have access to information about his resume, projects, and technical skills.
Answer questions clearly and concisely, drawing from the provided context.
If asked to explain a project, provide technical details and impact.
Keep answers focused and interview-appropriate (1-2 minutes when spoken)."""

    user_prompt = f"""Context from Shri's documents:
{context_str}

Question: {query}

Answer the question based on the context above. Be specific and mention relevant projects/experience."""

    # Call GPT-4
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def ask_question(query):
    """Main function to ask a question and get an answer"""
    print(f"\n🔍 Searching for: {query}")
    
    # Retrieve relevant contexts
    contexts = search_documents(query, top_k=3)
    
    print(f"✅ Found {len(contexts)} relevant chunks")
    
    # Generate answer
    print("🤖 Generating answer...")
    answer = generate_answer(query, contexts)
    
    return answer, contexts