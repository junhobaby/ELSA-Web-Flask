from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>This is Home!</p>"


@app.route("/about")
def about():
    return "<p>This is about!</p>"


@app.route("/profile/<profile_uid>")
def greeting(profile_uid):
    return f"<p>Profile {profile_uid}</p>"


@app.route("/api")
def get_api():
    return {"message": "hello"}
