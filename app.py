import os
from flask import Flask
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>I work still</h1>"


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5500")),
        debug=True
    )
