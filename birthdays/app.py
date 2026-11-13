import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        ##adding a new birthday to database and then re-render the index page if post requested
        name = request.form.get("name")
        if not name:
            return redirect("/")
        month = request.form.get("month")
        if not month:
            return redirect("/")
        day = request.form.get("day")
        if not day:
            return redirect("/")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?,?,?)", name, month, day )

        return redirect("/")


    else:

        all_records = db.execute("select id, name, month || '/'|| day as birthday from birthdays ")

        return render_template("index.html", all_records = all_records)


@app.route("/deregister", methods=["POST"])

def deregister():

    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)

    return redirect("/")
