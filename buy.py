# pip install cloudipsp
# ссылка на проект на гитхаб: https://github.com/cloudipsp/python-sdk
# для использования нужна регистрация на платежном сервисе Fondy

from cloudipsp import Api, Checkout

api = Api(merchant_id=1396424,
          secret_key='test')    # id и ключ выдаются на сайте при регистрации компании
checkout = Checkout(api=api)
data = {
    "currency": "RUB",
    "amount": ""    # цена(нужно указывать нули в конце для корректного вывода на странице)
}
url = checkout.url(data).get('checkout_url')