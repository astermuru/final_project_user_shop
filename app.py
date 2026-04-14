from flask import Flask, render_template, request, redirect, url_for, session
import database
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "alsirgj55siiehgh"
UPLOAD_FOLDER = "static/aploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    products = database.get_products()
    cart = session.get("cart", {})
    cart = database.validate_cart(cart)
    cart_count = len(cart)
    return render_template("index.html", products=products, cart=cart, cart_count=cart_count)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        # получить данные из формы
        name = request.form['name']
        price = float(request.form['price'])
        type_products = request.form['type_products']
        description = request.form.get('description')
        image = request.files.get('image')

        #сохрвнить зображения
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        #создать запись в БД
        database.add_product(name, price, type_products, description, image_path)
        return redirect(url_for('index'))
    else:
        return render_template("add_product.html")
    
@app.route("/product/<int:product_id>")
def product(product_id):
    product = database.get_product_by_id(product_id)
    if product:
        return render_template("product.html", product=product)
    else:
        return redirect(url_for('index'))

@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):

    database.delete_product(product_id)
    return redirect(url_for('index'))

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):

    '''
    { id: count, id2: count2 }
    '''
    product_id = str(product_id)
    cart = session.get("cart", {})
    cart = database.validate_cart(cart)
    

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    
    session["cart"] = cart

    return redirect(url_for('index'))

@app.route("/cart", methods=["GET"])
def cart():
    cart = session.get("cart", {})
    cart = database.validate_cart(cart)
    render_cart=[]
    cart_summa = 0
    for product in cart:
        product_info = database.get_product_by_id(int(product))
        product_count = cart[product]
        cart_summa += product_count * product_info["price"]
        render_cart.append(
            {
                "product_info": product_info,
                "count": product_count
            }
        )

    return render_template("cart.html", cart=render_cart, cart_summa=cart_summa)

@app.route("/change_cart_product_amount", methods=["POST"])
def change_cart_product_amount():
    product_id = request.form["product_id"]
    action = request.form["action"]
    cart = session.get("cart", {})
    cart = database.validate_cart(cart)

    if action == "plus":
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] -= 1
        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]
    
    session["cart"] = cart
    return redirect(url_for("cart"))

    

if __name__ == "__main__":
    app.run(debug=True)