from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

DB = "issues.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            tag TEXT,
            status TEXT DEFAULT 'Open',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    try:
        conn.execute("ALTER TABLE issues ADD COLUMN status TEXT DEFAULT 'Open'")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def auto_tag(description):
    desc = description.lower()
    if "road" in desc:
        return "Road"
    elif "light" in desc:
        return "Electricity"
    elif "water" in desc:
        return "Water"
    return "General"

# ---------- Frontend ----------

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# ---------- API ----------

@app.route("/add-issue", methods=["POST"])
def add_issue():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name or not description:
        return jsonify({"error": "name and description required"}), 400

    tag = auto_tag(description)

    conn = sqlite3.connect(DB)
    cur = conn.execute(
        "INSERT INTO issues (name, description, tag, status) VALUES (?, ?, ?, 'Open')",
        (name, description, tag)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return jsonify({"id": new_id, "name": name, "description": description, "tag": tag, "status": "Open"}), 201

@app.route("/issues", methods=["GET"])
def get_issues():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM issues ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/delete-issue/<int:issue_id>", methods=["DELETE"])
def delete_issue(issue_id):
    conn = sqlite3.connect(DB)
    cur = conn.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "issue not found"}), 404

    return jsonify({"message": "deleted", "id": issue_id}), 200

@app.route("/toggle-status/<int:issue_id>", methods=["PATCH"])
def toggle_status(issue_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT status FROM issues WHERE id = ?", (issue_id,)).fetchone()

    if row is None:
        conn.close()
        return jsonify({"error": "issue not found"}), 404

    new_status = "Closed" if row["status"] == "Open" else "Open"
    conn.execute("UPDATE issues SET status = ? WHERE id = ?", (new_status, issue_id))
    conn.commit()
    conn.close()

    return jsonify({"id": issue_id, "status": new_status}), 200

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)