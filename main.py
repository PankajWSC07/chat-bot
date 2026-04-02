from flask import Flask, render_template, request, jsonify
from Chroma import initialize_database, query_collection

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
            return jsonify({"result": "No relevant result found", "docs": []})

        return jsonify({"result": "Found results", "docs": docs})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    initialize_database()

    app.run(debug=True, host="0.0.0.0", port=5000)
