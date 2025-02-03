from flask import Flask, jsonify, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
migrate = Migrate(app, db, render_as_batch=True)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))


class Login(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    nick = db.Column(db.String, nullable=False)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def __repr__(self):
        return str(self.id)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


'''Получение товаров'''

@app.route('/parser')
def get_products():
    with open('parser/PRODUCTS_DATA.json', 'r', encoding='utf-8') as file:
        products = json.load(file)
    return jsonify(products)


@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    return render_template("account.html", current_user=current_user)


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        nick = request.form['nick']
        mail = request.form['mail']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 == password2:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
            login = Login(mail=mail, password=hashed_password, nick=nick)
            try:
                db.session.add(login)
                db.session.commit()
                return redirect('/')
            except:
                return 'Произошла ошибка'
        else:
            return "Пароли не совпадают"
    else:
        return render_template("registration.html")


@app.route("/sign_in", methods=['POST', 'GET'])
def sign_in():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']  
        user = db.session.query(Login).filter(Login.mail == mail).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            flash("Invalid Username or password!", "danger")
            return render_template('sign_in.html')
    else:
        return render_template("sign_in.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/sign_in')

if __name__ == '__main__':
    app.run(debug=True)