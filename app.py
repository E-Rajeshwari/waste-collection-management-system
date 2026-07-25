from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Database connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create table
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS waste_collection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker TEXT NOT NULL,
            area TEXT NOT NULL,
            waste_type TEXT NOT NULL,
            weight TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Add record page
@app.route("/add")
def add():
    return render_template("add_record.html")


# Save record
@app.route("/save", methods=["POST"])
def save():

    worker = request.form["worker"]
    area = request.form["area"]
    waste_type = request.form["waste_type"]
    weight = request.form["weight"]
    date = request.form["date"]


    conn = get_db_connection()

    conn.execute("""
        INSERT INTO waste_collection
        (worker, area, waste_type, weight, date)
        VALUES (?, ?, ?, ?, ?)
    """,
    (worker, area, waste_type, weight, date))


    conn.commit()
    conn.close()

    return redirect("/records")



# View records
@app.route("/records")
def records():

    conn = get_db_connection()

    data = conn.execute(
        "SELECT * FROM waste_collection"
    ).fetchall()

    conn.close()

    return render_template(
        "records.html",
        records=data
    )



# Delete record
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM waste_collection WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/records")



if __name__ == "__main__":

    create_table()

    app.run(
        debug=True
    )