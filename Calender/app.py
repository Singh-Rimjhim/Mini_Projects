from flask import Flask, render_template, request
import calendar

app = Flask(__name__)


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

        print("Date:", date)
        print("Event:", event)

    return render_template(
        "events.html",
        year=year,
        month=month
    )

@app.route("/calendar", methods=["POST"])
def calendar_page():

    year = int(request.form["year"])
    month = int(request.form["month"])

    # Check if year is valid
    if year < 1:
        return "Invalid year! Please enter a year greater than 0."

    # Check if month is valid
    if month < 1 or month > 12:
        return "Invalid month! Please enter a month between 1 and 12."
    
    # Check which button was clicked
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

    month_name = f"{calendar.month_name[month]} {year}"

    weeks = calendar.monthcalendar(year, month)

    days = []

    for week in weeks:
        for day in week:
            days.append(day)

    return render_template(
        "calendar.html",
        days=days,
        month_name=month_name,
        year=year,
        month=month
    )


if __name__ == "__main__":
    app.run(debug=True)