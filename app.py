from flask import Flask, jsonify, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    nick = db.Column(db.String, nullable=False)

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


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        msg = MIMEMultipart()
        from_email = 'cmpmarket2@gmail.com' #создал нам почту
        psw = 'yqzo ntux nulx zgwi' # пароль только для нашего приложения
        message = 'Сообщение о регистрации'
        nick = request.form['nick']
        mail = request.form['mail']
        password1 = request.form['password1']
        password2 = request.form['password2']
        msg.attach(MIMEText(message, 'plain'))
        if 'gmail.com' in mail:
            server = smtplib.SMTP('smtp.gmail.com: 587')   
        elif 'mail.ru' in mail:
            server = smtplib.SMTP('smtp.mail.ru: 25')
        else:
            server = smtplib.SMTP('smtp.yandex.com: 465')
        server.starttls()
        server.login(from_email, psw)
        server.sendmail(from_email, mail, msg.as_string())
        server.quit()

        login = Login(mail=mail, password=password1, nick=nick)
        
        try:
            db.session.add(login)
            db.session.commit()
            return redirect('/')
        except:
            return 'Произошла ошибка'
    else:
        return render_template("registration.html")


@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")

if __name__ == '__main__':
    app.run(debug=True)