from flask import render_template, jsonify, request, Flask
from LangChain import initialize_db, get_retriever, retrieve_context
from Chat_filter import answer
import time
from functools import wraps

app = Flask(__name__)

db = initialize_db()
retriever = get_retriever(db) if db else None

request_times = {}
RATE_LIMIT_SECONDS = 2


def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()

        if client_ip in request_times:
            time_since_last_request = current_time - request_times[client_ip]

            if time_since_last_request < RATE_LIMIT_SECONDS:
                wait_time = round(RATE_LIMIT_SECONDS - time_since_last_request, 2)
                return (
                    jsonify(
                        {
                            "error": f"Rate limit exceeded. Please wait {wait_time} seconds before making another request."
                        }
                    ),
                    429,
                )

        request_times[client_ip] = current_time
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
@rate_limit
def query():
    try:
        user_query = request.json.get("query")
        user_query = user_query.strip()

        if not user_query or len(user_query) == 0:
            return jsonify({"error": "Query cannot be empty"}), 400

        if retriever is None:
            return jsonify({"error": "Database not initialized"}), 500

        context_docs = retrieve_context(user_query, retriever)

        ans = answer(user_query, context_docs)

        response = {"query": user_query, "answer": ans}
        return jsonify(response)

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
