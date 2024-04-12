from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.secret_key = '123.com'
    app.config.from_object(config)
    db.init_app(app)

    from app.views import register, login, main, show_goods_list, show_goods_detail, add_cart, show_cart, submit_order

    app.add_url_rule('/reg', view_func=register, methods=['GET', 'POST'])
    app.add_url_rule('/', view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/main', view_func=main)
    app.add_url_rule('/list', view_func=show_goods_list)
    app.add_url_rule('/detail', view_func=show_goods_detail)
    app.add_url_rule('/add', view_func=add_cart)
    app.add_url_rule('/cart', view_func=show_cart)
    app.add_url_rule('/submit_order', view_func=submit_order, methods=['POST'])

    return app


