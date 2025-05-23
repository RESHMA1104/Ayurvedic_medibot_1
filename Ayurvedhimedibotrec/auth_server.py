from flask import Flask, request, redirect, send_from_directory
import os

app = Flask(__name__, static_folder=".", template_folder=".")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/login")
def login():
    return send_from_directory(".", "login.html")

@app.route("/signup")
def signup():
    return send_from_directory(".", "signup.html")

@app.route("/login_user", methods=["POST"])
def login_user():
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password:
        return redirect("http://localhost:5000/?showReminder=true")
    return "Login failed", 401

@app.route("/signup_user", methods=["POST"])
def signup_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    if username and email and password:
        return redirect("http://localhost:5000/?showReminder=true")
    return "Signup failed", 400


if __name__ == "__main__":
    app.run(debug=True)
