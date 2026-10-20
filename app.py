from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)
DB = "users.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE)""")

@app.route("/")
def home():
    return "Lab 5 Security Testing"

@app.route("/api/users", methods=["GET"])
def get_users():
    with sqlite3.connect(DB) as conn:
        rows = conn.execute("SELECT id, name, email FROM users").fetchall()
    return jsonify([{"id":u[0],"name":u[1],"email":u[2]} for u in rows])

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    name, email = data.get("name"), data.get("email")
    if not isinstance(name, str) or not isinstance(email, str) or not name.strip() or not email.strip():
        return jsonify({"error":"Invalid input"}), 400
    try:
        with sqlite3.connect(DB) as conn:
            cur = conn.execute("INSERT INTO users (name,email) VALUES (?,?)", (name,email))
            user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        return jsonify({"error":"Email already exists"}), 400
    return jsonify({"id":user_id,"name":name,"email":email}), 201

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return "", 204

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
