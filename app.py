import json
from flask import Flask, jsonify, render_template
import numpy

app = Flask(__name__)

'''Получение товаров'''
with open('parser/PRODUCTS_DATA.json', 'r', encoding='utf-8') as file:
    products = json.load(file)



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

# 
@app.route('/get_products')
def get_products():
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)