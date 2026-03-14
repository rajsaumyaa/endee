from dotenv import load_dotenv
load_dotenv()
from groq import Groq
from endee import Endee
from sentence_transformers import SentenceTransformer

# Configure Groq (Free & Fast!)
import os
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Connect to Endee
client = Endee()
index = client.get_index(name="space_news")

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def ask_agent(query):
    print("🔍 Searching Endee vector database...")

    # Step 1: Convert query to vector
    query_vector = embedder.encode(query).tolist()

    # Step 2: Semantic search in Endee
    results = index.query(vector=query_vector, top_k=5)

    # Step 3: Build context
    context = ""
    for item in results:
        context += f"📰 Title: {item['meta']['title']}\n"
        context += f"   Summary: {item['meta']['summary']}\n"
        context += f"   Source: {item['meta']['url']}\n\n"

    if not context:
        return "I couldn't find relevant articles. Try rephrasing!"

    # Step 4: Ask Groq with context
    prompt = f"""You are AstroAgent 🚀 — an expert AI assistant for space, astronomy, and science news.
Answer questions using the latest news articles retrieved from your knowledge base.
Be informative, engaging, and always mention relevant article titles.

Latest Retrieved Articles:
{context}

User Question: {query}

Provide a detailed, helpful answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content