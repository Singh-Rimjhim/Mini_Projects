from flask import Flask, render_template, request, redirect
import calendar
import sqlite3

app = Flask(__name__)


def create_database():
    connection = sqlite3.connect("events.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            event TEXT
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add-event", methods=["GET", "POST"])
def add_events():

    year = request.args.get("year")
    month = request.args.get("month")

    if request.method == "POST":

        date = request.form["date"]
        event = request.form["event"]

        connection = sqlite3.connect("events.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO events (date, event) VALUES (?, ?)",
            (date, event)
        )

        connection.commit()
        connection.close()

        print("Event saved successfully!")

    return render_template(
        "events.html",
        year=year,
        month=month
    )

@app.route("/delete-event/<int:event_id>", methods=["POST"])
def delete_event(event_id):

    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT date FROM events WHERE id = ?",
        (event_id,)
    )

    result = cursor.fetchone()

    cursor.execute(
        "DELETE FROM events WHERE id = ?",
        (event_id,)
    )

    connection.commit()
    connection.close()

    if result:
        date = result[0]
        date_parts = date.split("-")

        year = int(date_parts[0])
        month = int(date_parts[1])

        return redirect(
            f"/calendar?year={year}&month={month}"
        )

    return redirect("/")

@app.route("/calendar", methods=["GET", "POST"])
def calendar_page():
    if request.method == "GET":
        year = int(request.args.get("year"))
        month = int(request.args.get("month"))

    else:
        year = int(request.form["year"])
        month = int(request.form["month"])

        action = request.form.get("action")

        if action == "previous":
            month = month - 1

            if month == 0:
                month = 12
                year = year - 1

        elif action == "next":
            month = month + 1

            if month == 13:
                month = 1
                year = year + 1

    if year < 1:
        return "Invalid year! Year cannot be less than 1."
    if month < 1 or month > 12:
        return "Invalid month! Please enter a month between 1 and 12."

    month_name = f"{calendar.month_name[month]} {year}"

    weeks = calendar.monthcalendar(year, month)

    days = []

    for week in weeks:
        for day in week:
            days.append(day)
    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, date, event FROM events"
    )

    events = cursor.fetchall()

    connection.close()
    return render_template(
        "calendar.html",
        days=days,
        month_name=month_name,
        year=year,
        month=month,
        events=events
    )


if __name__ == "__main__":
    create_database()
    app.run(debug=True)