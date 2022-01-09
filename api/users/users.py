from flask import Blueprint, request
from database import db_connect
from jwthelper import encode_data, decode_data

users = Blueprint('users', __name__)

@users.route('/', methods=['POST'])
def create_user():
    data = request.get_json()

    name = data['name']
    email = data['email']
    password = data['password']
    _type = data['type']
    typeEnum = 0 if _type == '買家' else 1
    phone = data['phone']
    
    con = db_connect()
    cur = con.cursor()
    cur.execute('''INSERT INTO users (name, email, password, type, phone)
                   VALUES (?, ?, ?, ?, ?);''',
                    (name, email, password, typeEnum, phone))
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


@users.route('/<id>', methods=['PATCH'])
def update_user(id):
    data = request.get_json()
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    userdata = decode_data(jwt_token)

    id = int(id)
    name = data['name']
    phone = data['phone']
    user_id = userdata['user_id']

    assert id == user_id

    data['id'] = id

    con = db_connect()
    cur = con.cursor()

    cur.execute('''UPDATE users
                   SET name = ?, phone = ?
                   WHERE id = ?;''', (name, phone, id))
    
    con.commit()
    
    cur.execute('''SELECT * FROM users WHERE id = ?;''', (user_id, ))
    user = cur.fetchone()
    data['email'] = user[2]
    data['type'] = '買家' if user[4] == 0 else '賣家'
    
    con.close()

    response = {
        'status': 200,
        'message': 'success',
        'data': data
    }
    return response, 200


@users.route('/signIn', methods=['POST'])
def sign_in():
    data = request.get_json()
    
    email = data['email']
    password = data['password']

    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT * FROM users 
                   WHERE email = ? AND password = ?;''', (email, password))
    user = cur.fetchone()
    id = user[0]
    _type = '買家' if user[4] == 0 else '賣家'

    con.close()

    token = encode_data({
        'user_id': id,
        'type': _type
    })

    response = {
        'status': 200,
        'message': 'ok',
        'data': {
            'id': id,
            'token': token
        }
    }
    return response, 200


@users.route('/me', methods=['GET'])
def get_self_data():
    data = request.get_json()
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    userdata = decode_data(jwt_token)

    user_id = userdata['user_id']

    con = db_connect()
    cur = con.cursor()

    cur.execute('''SELECT * FROM users
                   WHERE id = ?;''', (user_id, ))
    user = cur.fetchone()
    data = {
        'id': user[0],
        'name': user[1],
        'email': user[2],
        'type': '買家' if user[4] == 0 else '賣家',
        'phone': user[5]
    }

    con.close()

    response = {
        'status': 200,
        'message': 'success',
        'data': data
    }
    return response, 200