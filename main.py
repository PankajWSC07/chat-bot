from flask import render_template, jsonify, request, Flask
from LangChain import initialize_db, get_retriever, retrieve_context
from Chat_filter import answer
from functools import wraps
from langchain_core.rate_limiters import InMemoryRateLimiter

app = Flask(__name__)

db = initialize_db()
retriever = get_retriever(db) if db else None

rate_limiter = InMemoryRateLimiter(requests_per_second=0.5)


def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not rate_limiter.acquire(blocking=False):
            return (
                jsonify(
                    {
                        "error": "Rate limit reached. Please wait before making another request."
                    }
                ),
                429,
            )

        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
@rate_limit
def query():
    try:
        user_query = request.json.get("query", "").strip()

        if not user_query:
            return jsonify({"error": "Query cannot be empty"}), 400

        if retriever is None:
            return jsonify({"error": "Database not initialized"}), 500

        context_docs = retrieve_context(user_query, retriever)

        ans = answer(user_query, context_docs)

        return jsonify({"query": user_query, "answer": ans})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if db is None:
        print("Error: Database initialization failed. Please check your data files.")
    else:
        print("Database initialized successfully!")

    app.run(debug=True, host="0.0.0.0")
