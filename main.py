from flask import render_template, jsonify, request, Flask

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
def query():
    user_query = request.json.get("query")

    if not user_query or len(user_query.strip()) == 0:
        return jsonify({"error": "Query cannot be empty"}), 400

    response = {
        "query": user_query,
        "results": "data",
    }
    return jsonify(response)


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
