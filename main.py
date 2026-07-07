from flask import (  # type: ignore
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)


@app.route("/main")
def main():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


