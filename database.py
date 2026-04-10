import sqlite3
import os

def create_database():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   price REAL NOT NULL,
                   description TEXT DEFAULT "",
                   image TEXT DEFAULT "",
                   type_products TEXT NOT NULL,
            )
                   
        ''')
    
    conn.commit()
    conn.close()

def add_product(name, price, description="", image="", ):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute('''
                   INSERT INTO products
                   (name, price, description, image, type_products)
                   VALUES(?,?,?,?)
                   
                   ''', (name, price, description, image, type_products))
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
            "description": product[3],
            "image": product[4],
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

if __name__ == "__main__":
    create_database()
    print(get_products())