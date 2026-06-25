from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "applications.db"


# Runs once to create the database table
def init_db():
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT DEFAULT 'Applied',
            notes TEXT
        )
    """)
    con.commit()
    con.close()


# Homepage — show all records
@app.route("/")
def index():
    con = sqlite3.connect(DB)
    apps = con.execute(
        "SELECT * FROM applications ORDER BY date DESC"
    ).fetchall()
    con.close()
    return render_template("index.html", apps=apps)


# Add a new application
@app.route("/add", methods=["POST"])
def add():
    d = request.form
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO applications (company, role, date, status, notes) VALUES (?, ?, ?, ?, ?)",
        (d["company"], d["role"], d["date"], d["status"], d["notes"])
    )
    con.commit()
    con.close()
    return redirect(url_for("index"))


# Edit page
@app.route("/edit/<int:id>")
def edit(id):
    con = sqlite3.connect(DB)
    app_data = con.execute(
        "SELECT * FROM applications WHERE id=?",
        (id,)
    ).fetchone()
    con.close()
    return render_template("edit.html", app=app_data)


# Save the edit
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    d = request.form
    con = sqlite3.connect(DB)
    con.execute(
        """UPDATE applications
           SET company=?, role=?, date=?, status=?, notes=?
           WHERE id=?""",
        (
            d["company"],
            d["role"],
            d["date"],
            d["status"],
            d["notes"],
            id,
        ),
    )
    con.commit()
    con.close()
    return redirect(url_for("index"))


# Delete a record
@app.route("/delete/<int:id>")
def delete(id):
    con = sqlite3.connect(DB)
    con.execute("DELETE FROM applications WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)