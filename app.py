from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "tulasi_secret"

products = [
    {"id":1,"name":"Tulasi Herbal Soap","price":80,"img":"static\products\soap1.jpg","category":"Soap"},
    {"id":2,"name":"Neem Oil","price":120,"img":"static\products\oil1.jpg","category":"Oil"},
    {"id":3,"name":"Amla Hair Oil","price":90,"img":"static\products\gel1.jpg","category":"Oil"},
    
]

@app.route('/')
def home(): return render_template("index.html")

@app.route('/products')
def show_products():
    sort = request.args.get("sort","none")
    cat = request.args.get("cat","All")
    items = [p for p in products if cat=="All" or p["category"]==cat]
    if sort=="low-high": items.sort(key=lambda x:x["price"])
    if sort=="high-low": items.sort(key=lambda x:x["price"],reverse=True)
    return render_template("products.html", products=items, sort=sort, category=cat)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart']=cart
    return redirect(url_for('show_cart'))

@app.route('/cart')
def show_cart():
    cart = session.get('cart', [])
    items = [p for p in products if p["id"] in cart]
    return render_template("cart.html", cart=items)

@app.route('/place_order', methods=['POST'])
def place_order():
    method = request.form["payment"]
    items = session.get('cart', [])
    selected = [p for p in products if p["id"] in items]
    session['cart']=[]  # clear
    return render_template("order.html", items=selected, method=method)

@app.route('/track', methods=['GET','POST'])
def track():
    status = None
    oid = None
    if request.method=="POST":
        oid = request.form["order_id"]
        status = "In Transit"  # demo
    return render_template("track.html", oid=oid, status=status)

if __name__=="__main__":
    app.run(debug=True)
