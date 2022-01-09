import sqlite3

database_path = './sqlite.db'

def db_connect():
    con = sqlite3.connect(database_path)
    return con

def create_database():
    con = db_connect()
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                       id INTEGER NOT NULL PRIMARY KEY,
                       name TEXT NOT NULL,
                       email TEXT NOT NULL UNIQUE,
                       password TEXT NOT NULL,
                       type INTEGER NOT NULL,
                       phone TEXT NOT NULL
                   );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS products (
                       id INTEGER NOT NULL PRIMARY KEY,
                       name TEXT NOT NULL,
                       description TEXT NOT NULL,
                       picture TEXT NOT NULL,
                       inventory INTEGER NOT NULL,
                       price INTEGER NOT NULL,
                       startSaleTime STRING NOT NULL,
                       endSaleTime STRING NOT NULL,
                       user_id INTEGER REFERENCES users(id)
                   );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS orders (
                       order_id INTEGER NOT NULL,
                       amount INTEGER NOT NULL,
                       time STRING NOT NULL,
                       user_id INTEGER REFERENCES users(id),
                       product_id INTEGER REFERENCES products(id)   
                   );''')
    con.commit()
    con.close()