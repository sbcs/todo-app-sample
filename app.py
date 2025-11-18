from flask import Flask, request, jsonify, abort
import redis
import os
import uuid
import json

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


@app.route("/todo", methods=["GET"])
def list_todos():
    """
    GET /todo
    Returns a list of all todo items `{ "id": str, "task": str  }`.
    """

    todos_keys = r.keys()
    return jsonify([json.loads(r.get(key)) for key in todos_keys]), 200


@app.route("/todo", methods=["POST"])
def create_todo():
    """
    POST /todo
    """

    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    task = data.get("task")

    if not task:
        abort(400, description="Missing 'task' field")

    todo_id = str(uuid.uuid4())
    todo = {"id": todo_id, "task": task}
    r.set(todo_id, json.dumps(todo))

    return jsonify(todo), 201


@app.route("/todo/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """
    DELETE /todo/<todo_id>
    """

    if not r.exists(todo_id):
        abort(404, description="Todo item not found")
    r.delete(todo_id)

    return jsonify({"deleted": todo_id}), 200


# serve index.html for basic ui
@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    # ensure Redis connection early
    try:
        r.ping()
    except Exception as e:
        print(f"Cannot connect to Redis at {REDIS_HOST}:{REDIS_PORT} - {e}")
        raise

    app.run(host="0.0.0.0", port=5000, debug=True)
