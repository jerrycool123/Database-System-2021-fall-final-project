from flask import Blueprint

from .users.users import users
from .products.products import products
from .orders.orders import orders
from .images.images import images

api = Blueprint('api', __name__)

api.register_blueprint(users, url_prefix='/users')
api.register_blueprint(products, url_prefix='/products')
api.register_blueprint(orders, url_prefix='/orders')
api.register_blueprint(images, url_prefix='/images')