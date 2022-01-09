from flask import Blueprint, request
from database import db_connect
from jwthelper import decode_data

products = Blueprint('products', __name__)

@products.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    userdata = decode_data(jwt_token)

    name = data['name']
    description = data['description']
    picture = data['picture']
    inventory = data['inventory']
    price = data['price']
    startSaleTime = data['startSaleTime']
    endSaleTime = data['endSaleTime']
    user_id = userdata['user_id']
    _type = userdata['type']

    assert _type == '賣家'
    
    con = db_connect()
    cur = con.cursor()

    cur.execute('''INSERT INTO products (name, description, picture, inventory, price, startSaleTime, endSaleTime, user_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                    (name, description, picture, inventory, price, startSaleTime, endSaleTime, user_id))
    id = cur.lastrowid
    con.commit()
    con.close()

    data['id'] = id
    response = {
        'status': 201,
        'message': 'created',
        'data': data
    }
    return response, 201


@products.route('/', methods=['GET'])
def get_all_products():
    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT * FROM products;''')
    all_products = cur.fetchall()

    con.close()

    data = []
    for product in all_products:
        data.append({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'picture': product[3],
            'inventory': product[4],
            'price': product[5],
            'startSaleTime': product[6],
            'endSaleTime': product[7]
        })
    
    response = {
        'status': 200,
        'message': 'success',
        'data': data
    }
    return response, 200


@products.route('/<id>', methods=['GET'])
def get_product(id):
    data = request.get_json()

    id = int(id)

    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT * FROM products WHERE id = ?;''', (id, ))
    product = cur.fetchone()

    con.close()

    data = {
        'id': product[0],
        'name': product[1],
        'description': product[2],
        'picture': product[3],
        'inventory': product[4],
        'price': product[5],
        'startSaleTime': product[6],
        'endSaleTime': product[7]
    }
    
    response = {
        'status': 200,
        'message': 'success',
        'data': data
    }
    return response, 200


@products.route('/<id>', methods=['PATCH'])
def update_product(id):
    data = request.get_json()
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    userdata = decode_data(jwt_token)

    id = int(id)
    name = data['name']
    description = data['description']
    picture = data['picture']
    inventory = data['inventory']
    startSaleTime = data['startSaleTime']
    endSaleTime = data['endSaleTime']
    user_id = userdata['user_id']

    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT * FROM products WHERE id = ?;''', (id, ))
    product = cur.fetchone()
    product_user_id = product[8]
    
    assert product_user_id == user_id

    data['id'] = user_id

    cur.execute('''UPDATE products 
                   SET name = ?, description = ?, picture = ?, inventory = ?, startSaleTime = ?, endSaleTime = ?
                   WHERE id = ?;''', (name, description, picture, inventory, startSaleTime, endSaleTime, id))
    
    con.commit()

    cur.execute('''SELECT * FROM products WHERE id = ?;''', (id, ))
    product = cur.fetchone()
    data['price'] = product[5]

    con.close()

    response = {
        'status': 201,
        'message': 'created',
        'data': data
    }
    return response, 201


@products.route('/<id>', methods=['DELETE'])
def delete_product(id):
    data = request.get_json()
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    userdata = decode_data(jwt_token)

    id = int(id)
    user_id = userdata['user_id']

    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT * FROM products WHERE id = ?;''', (id, ))
    product = cur.fetchone()
    name = product[1]
    product_user_id = product[8]
    
    assert product_user_id == user_id

    cur.execute('''DELETE FROM products WHERE id = ?;''', (id, ))

    con.commit()
    con.close()

    response = {
        'status': 200,
        'message': 'success',
        'data': name + ' deleted'
    }
    return response, 200