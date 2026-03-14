import requests
from endee import Endee, Precision
from sentence_transformers import SentenceTransformer

# Connect to Endee server running locally
client = Endee()

# Create index
try:
    client.create_index(
        name="space_news",
        dimension=384,
        space_type="cosine",
        precision=Precision.INT8
    )
    print("✅ Index 'space_news' created!")
except Exception as e:
    print(f"ℹ️ Index already exists, continuing...")

index = client.get_index(name="space_news")

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def fetch_and_store_news():
    print("📰 Fetching latest space & science news...")
    url = "https://api.spaceflightnewsapi.net/v4/articles/?limit=50"
    response = requests.get(url)
    articles = response.json()["results"]

    vectors = []
    for i, article in enumerate(articles):
        text = f"{article['title']}. {article['summary']}"
        embedding = embedder.encode(text).tolist()
        vectors.append({
            "id": str(article["id"]),
            "vector": embedding,
            "meta": {
                "title": article["title"],
                "summary": article["summary"],
                "url": article["url"],
                "published": article["published_at"]
            }
        })
        print(f"  ✓ {i+1}/{len(articles)}: {article['title'][:60]}...")

    index.upsert(vectors)
    print(f"\n✅ Successfully stored {len(vectors)} articles in Endee!")

if __name__ == "__main__":
    fetch_and_store_news()