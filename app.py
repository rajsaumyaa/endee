from flask import Flask, render_template, request, jsonify
from ingest import fetch_and_store_news
from agent import ask_agent

app = Flask(__name__)

# Load news into Endee when app starts
print("🚀 Loading space news into Endee...")
fetch_and_store_news()
print("✅ AstroAgent ready!")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    answer = ask_agent(query)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=False, port=5000)