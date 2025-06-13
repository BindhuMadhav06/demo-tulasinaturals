from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "tulasi_secret"

products = [
    {"id": 1, "name": "Tulasi Herbal Soap", "price": 80, "img": "static/products/soap1.jpg", "category": "Soap", "description": "Cleanses and refreshes skin with tulasi extracts."},
    {"id": 2, "name": "Neem Oil", "price": 120, "img": "static/products/oil1.jpg", "category": "Oil", "description": "Naturally antibacterial neem oil for skin and hair."},
    {"id": 3, "name": "Amla Hair Oil", "price": 90, "img": "static/products/gel1.jpg", "category": "Oil", "description": "Boosts hair growth and reduces hair fall with Amla."},
    {"id": 4, "name": "Aloe Vera Gel", "price": 70, "img": "static/products/gel2.jpg", "category": "Gel", "description": "Hydrates and soothes skin with pure aloe extract."},
    {"id": 5, "name": "Coconut Hair Oil", "price": 110, "img": "static/products/oil2.jpg", "category": "Oil", "description": "Deeply nourishes hair and strengthens roots."},
    {"id": 6, "name": "Sandalwood Soap", "price": 85, "img": "static/products/soap2.jpg", "category": "Soap", "description": "Soothing aroma and smooth cleansing with sandalwood."},
    {"id": 7, "name": "Tulasi Face Wash", "price": 95, "img": "static/products/face1.jpg", "category": "Face Care", "description": "Removes impurities and gives glowing skin."},
    {"id": 8, "name": "Neem Face Pack", "price": 105, "img": "static/products/face2.jpg", "category": "Face Care", "description": "Tightens pores and reduces acne naturally."},
    {"id": 9, "name": "Lemon Herbal Soap", "price": 75, "img": "static/products/soap3.jpg", "category": "Soap", "description": "Brightens and energizes your skin with lemon zest."},
    {"id": 10, "name": "Brahmi Hair Oil", "price": 115, "img": "static/products/oil3.jpg", "category": "Oil", "description": "Strengthens hair and promotes healthy scalp."},
    {"id": 11, "name": "Turmeric Cream", "price": 90, "img": "static/products/cream1.jpg", "category": "Skin Care", "description": "Fights acne and lightens spots with turmeric."},
    {"id": 12, "name": "Aloe Moisturizer", "price": 100, "img": "static/products/cream2.jpg", "category": "Skin Care", "description": "Deep hydration for soft, glowing skin."},
    {"id": 13, "name": "Honey Lip Balm", "price": 45, "img": "static/products/lip1.jpg", "category": "Lip Care", "description": "Moisturizes and heals dry lips with honey."},
    {"id": 14, "name": "Rose Water", "price": 60, "img": "static/products/rose1.jpg", "category": "Face Care", "description": "Refreshing toner for natural glow and hydration."},
    {"id": 15, "name": "Multani Mitti Pack", "price": 80, "img": "static/products/face3.jpg", "category": "Face Care", "description": "Removes dirt and tightens skin pores."},
    {"id": 16, "name": "Charcoal Soap", "price": 90, "img": "static/products/soap4.jpg", "category": "Soap", "description": "Detoxifies and unclogs skin pores with charcoal."},
    {"id": 17, "name": "Hair Growth Oil", "price": 130, "img": "static/products/oil4.jpg", "category": "Oil", "description": "Stimulates roots and supports rapid hair growth."},
    {"id": 18, "name": "Tulasi Body Wash", "price": 95, "img": "static/products/body1.jpg", "category": "Body Care", "description": "Refreshing full-body cleanse with tulasi."},
    {"id": 19, "name": "Mint Face Mist", "price": 75, "img": "static/products/face4.jpg", "category": "Face Care", "description": "Instant freshness with cooling mint blend."},
    {"id": 20, "name": "Shea Butter Cream", "price": 120, "img": "static/products/cream3.jpg", "category": "Skin Care", "description": "Deep moisturization and skin repair with shea."},
    {"id": 21, "name": "Herbal Bath Powder", "price": 95, "img": "static/products/bath1.jpg", "category": "Body Care", "description": "Traditional herbal formula for body detox."}
]

@app.route('/')
def home():
    return render_template("index.html", products=products)

@app.route('/products')
def show_products():
    sort = request.args.get("sort", "none")
    cat = request.args.get("cat", "All")
    items = [p for p in products if cat == "All" or p["category"] == cat]
    if sort == "low-high":
        items.sort(key=lambda x: x["price"])
    if sort == "high-low":
        items.sort(key=lambda x: x["price"], reverse=True)
    return render_template("products.html", products=items, sort=sort, category=cat)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
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
    session['cart'] = []  # clear
    return render_template("order.html", items=selected, method=method)

@app.route('/track', methods=['GET', 'POST'])
def track():
    status = None
    oid = None
    if request.method == "POST":
        oid = request.form["order_id"]
        status = "In Transit"  # demo
    return render_template("track.html", oid=oid, status=status)

if __name__ == "__main__":
    app.run(debug=True)
