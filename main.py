from flask import Flask, render_template, request, jsonify
from Chroma import initialize_database, query_collection
from Chat_filter import refine_answer

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
def query():
    try:
        data = request.json
        query_text = data.get("query", "").strip()

        if not query_text:
            return jsonify({"error": "Please enter a valid query"}), 400

        docs = query_collection(query_text, n_results=3)

        if not docs:
            return jsonify({"result": "No relevant context found", "docs": [], "answer": ""})

        refined_answer = refine_answer(query_text, docs)
        
        if refined_answer is None:
            refined_answer = docs[0] if docs else "Unable to process your question."

        return jsonify({
            "result": "Success",
            "answer": refined_answer,
            "docs": docs,
            "query": query_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, host="0.0.0.0", port=5000)
