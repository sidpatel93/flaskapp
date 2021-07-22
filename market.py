from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h2>Hello, World!</h2>"

@app.route("/about/<username>")
def about_page(username):
    return f'<h1>This is about page for {username} </h1>'