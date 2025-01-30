from flask import Flask, render_template

app = Flask(__name__)

''''''




@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/registration")
def registration():
    return render_template("registration.html")


@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")


if __name__ == '__main__':
    app.run(debug=True)