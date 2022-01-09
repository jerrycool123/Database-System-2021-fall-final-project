from flask import Blueprint, request
from database import db_connect
from jwthelper import decode_data
import time
from datetime import datetime

orders = Blueprint('orders', __name__)

@orders.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    userdata = decode_data(jwt_token)

    order_id = int(time.time() * 10000000)
    order_date = datetime.today().strftime('%Y-%m-%d')
    user_id = userdata['user_id']
    _type = userdata['type']

    assert _type == '買家'

    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT * FROM users WHERE id = ?;''', (user_id, ))
    user = cur.fetchone()

    products_info = []
    for product_data in data:
        productId = product_data['productId']
        amount = product_data['amount']
        cur.execute('''SELECT * FROM products 
                       WHERE id = ? 
                       AND inventory >= ?;''', (productId, amount))
        product = cur.fetchone()
        startSaleTime = product[6]
        endSaleTime = product[7]

        assert startSaleTime <= order_date and order_date <= endSaleTime

        products_info.append({
            'name': product[1],
            'description': product[2],
            'picture': product[3],
            'price': product[5],
            'amount': amount
        })

        cur.execute('''UPDATE products
                       SET inventory = inventory - ?
                       WHERE id = ? 
                       AND inventory >= ?;''', (amount, productId, amount))
        
        assert cur.rowcount == 1
    
        cur.execute('''INSERT INTO orders (order_id, amount, time, user_id, product_id)
                       VALUES (?, ?, ?, ?, ?);''',
                        (order_id, amount, order_date, user_id, productId))
    
    con.commit()
    con.close()

    response = {
        'status': 201,
        'message': 'created',
        'data': {
            'id': order_id,
            'buyerName': user[1],
            'buyerEmail': user[2],
            'buyerPhone': user[5],
            'timestamp': order_date,
            'products': products_info
        }
    }
    
    return response, 201


@orders.route('/', methods=['GET'])
def get_all_orders():
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    _ = decode_data(jwt_token)

    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT DISTINCT order_id FROM orders;''')
    order_id_list = [order_id[0] for order_id in cur.fetchall()]

    data = []
    for order_id in order_id_list:
        cur.execute('''SELECT * FROM orders WHERE order_id = ?;''', (order_id, ))
        all_products = cur.fetchall()
        order_date = all_products[0][2]
        user_id = all_products[0][3]

        cur.execute('''SELECT * FROM users WHERE id = ?;''', (user_id, ))
        user = cur.fetchone()
        order_data = {
            'id': order_id,
            'buyerName': user[1],
            'buyerEmail': user[2],
            'buyerPhone': user[5],
            'timestamp': order_date
        }

        products_data = []
        for product in all_products:
            amount = product[1]
            product_id = product[4]
            cur.execute('''SELECT * FROM products WHERE id = ?;''', (product_id, ))
            product_info = cur.fetchone()
            products_data.append({
                'name': product_info[1],
                'description': product_info[2],
                'picture': product_info[3],
                'price': product_info[5],
                'amount': amount
            })
        
        order_data['products'] = products_data
        data.append(order_data)

    con.close()

    response = {
        'status': 200,
        'message': 'success',
        'data': data
    }

    return response, 200


@orders.route('/<id>', methods=['GET'])
def get_order(id):
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    _ = decode_data(jwt_token)

    id = int(id)

    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT * FROM orders WHERE order_id = ?;''', (id, ))
    all_products = cur.fetchall()
    order_date = all_products[0][2]
    user_id = all_products[0][3]

    cur.execute('''SELECT * FROM users WHERE id = ?;''', (user_id, ))
    user = cur.fetchone()
    order_data = {
        'id': id,
        'buyerName': user[1],
        'buyerEmail': user[2],
        'buyerPhone': user[5],
        'timestamp': order_date
    }

    products_data = []
    for product in all_products:
        amount = product[1]
        product_id = product[4]
        cur.execute('''SELECT * FROM products WHERE id = ?;''', (product_id, ))
        product_info = cur.fetchone()
        products_data.append({
            'name': product_info[1],
            'description': product_info[2],
            'picture': product_info[3],
            'price': product_info[5],
            'amount': amount
        })
        
    order_data['products'] = products_data

    response = {
        'status': 200,
        'message': 'success',
        'data': order_data
    }
    return response, 200