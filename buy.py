# нужна регистрация на Юmoney
import flask
from yandex_money.api import Wallet, ExternalPayment
from yandex_money import api

from flask import request

code1=''

scope1 = ['account-info', 'operation-history']
auth_url = Wallet.build_obtain_token_url(client_id=code1,redirect_uri='www.myurl', scope=scope1) + '&response_type=code'

scope = ['account-info', 'operation-history']

auth_url = Wallet.build_obtain_token_url(code,'www.myurl', scope)

app = flask.Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def ymon():


    token = api.Wallet.get_access_token(client_id=token1,
                                        code=flask.request.args['code'],
                                        redirect_uri='www.myurl')

    return render_template('ya.html', token=token)