import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
SALT = "Ijaigawoi32"

def create_database():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()


#Создание таблицы type_user
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Type_user (
            id iNTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL

        )
    ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO Type_user (name) VALUES (?) 
                   ''', ("user", ))
    conn.commit()
    cursor.execute('''
        INSERT INTO Type_user (name) VALUES (?) 
                   ''', ("admin", ))
    conn.commit()
    cursor.execute("INSERT INTO Type_user (name) VALUES (?)", ("super_admin", ) )
    conn.commit()


     #Создание таблицы user
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id iNTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR(1000) NOT NULL,
            password VARCHAR(256) NOT NULL,
            type_user INTEGER,
            FOREIGN KEY (type_user) REFERENCES Type_products(id)
        )
    ''')
    conn.commit()

     #Создание таблицы type_products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Type_products (
            id iNTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL

        )
    ''')
    conn.commit()

    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("electronics", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("food products", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("clothes", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("shoes", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("children's products", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("care cosmetics", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("pet supplies", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("construction and renovation", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("pharmacy", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("accessories", ))
    conn.commit()
    cursor.execute('''
            INSERT INTO Type_products(name) VALUES (?)
                   ''', ("hobby", ))
    conn.commit()

    
    

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   price REAL NOT NULL,
                   type_products INTEGER,
                   description TEXT DEFAULT "",
                   image TEXT DEFAULT "",
                   FOREIGN KEY (type_products) REFERENCES Type_products(id)
    
            )
                   
        ''')
    
    conn.commit()
    conn.close()

def add_product(name, price,  type_products, description="", image="", ):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute('''
                   INSERT INTO products
                   (name, price, type_products, description, image)
                   VALUES(?,?,?,?,?)
                   
                   ''', (name, price, type_products, description, image))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
        
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()
    return products

def get_product_by_id(product_id):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    conn.close()
    if product:
        return {
            "id":product[0],
            "name": product[1],
            "price": product[2],
            "type_products": product[3],
            "description": product[4],
            "image": product[5],
        }
    else:
        return None

def delete_product(product_id):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    image_path = product[4]
    if os.path.exists(image_path):
        os.remove(image_path)

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()

def validate_cart(cart):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    ids = list(cart.keys())
    for i in ids:
        cursor.execute("SELECT * FROM products WHERE id=?", (int(i),))
        product = cursor.fetchone()
        if not product:
            del cart[i]
    return cart

# пользователь
def add_user(login, password, type_user):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor() 
    hashed_password = generate_password_hash(password + SALT)
    

    cursor.execute("INSERT INTO user (login, password, type_user) VALUES (?, ?, ?)", (login, hashed_password, type_user ))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    return users

def check_user_exists(login):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE login=?", (login, ))
    user = cursor.fetchone()
    return True if user else False

def auth_user(login, password):
    #0- авторизация прошла
    #-1 -  что пошло не так

    # 1. Получить пользвателя по логину
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE login=?", (login, ))
    user = cursor.fetchone() #(2, "admin", "sjgiigjaiihb")
    if not user:
        return -1

    # 2. сравнить сгенерированный хеш с тем, что хранится
    if check_password_hash(user[2], password+SALT):
        return user[0]
    
    return -1

def get_user_by_id(user_id):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    if user:
        return {
            "id":user[0],
            "login": user[1],
            "password": user[2],
            "type_user": user[3],
        }
    else:
        return None


if __name__ == "__main__":
    create_database()
    print(get_products())