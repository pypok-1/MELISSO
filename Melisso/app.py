"""MELISSO — Raw Artisan Greek Honey
Flask server with SQLite-backed product catalog and working cart.
Run:  python app.py  →  http://localhost:5000
"""
import os
from flask import Flask, render_template, request, session, jsonify

from models import db, Product

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "melisso-secret-key-change-me-in-production"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'melisso.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

FREE_SHIPPING_THRESHOLD = 80.0


def all_products():
    return Product.query.filter_by(is_active=True).order_by(Product.sort_order).all()


def get_product(pid):
    return db.session.get(Product, pid)


def products_dict():
    return {p.id: p for p in all_products()}


def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def build_cart_items(cart):
    items, subtotal = [], 0.0
    catalog = products_dict()

    for pid, qty in cart.items():
        p = catalog.get(pid)
        if not p:
            continue
        line = p.price * qty
        subtotal += line
        items.append({
            **p.to_dict(),
            "qty": qty,
            "line_total": round(line, 2),
        })

    return items, round(subtotal, 2)


def cart_count():
    return sum(get_cart().values())


def shipping_for(subtotal):
    return 0.0 if subtotal >= FREE_SHIPPING_THRESHOLD or subtotal == 0 else 6.90


@app.context_processor
def inject_globals():
    return {"cart_count": cart_count()}


# ────────────────────────────────────────────────────────────
#  Main (index.py)
# ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    products = [p.to_dict() for p in all_products()]
    return render_template("index.html", products=products)


@app.route("/cart")
def cart_page():
    cart = get_cart()
    items, subtotal = build_cart_items(cart)
    shipping = shipping_for(subtotal)
    total = round(subtotal + shipping, 2)

    recommended = [p.to_dict() for p in all_products()[:4]]

    return render_template(
        "cart.html",
        items=items,
        subtotal=subtotal,
        shipping=shipping,
        total=total,
        free_shipping_threshold=FREE_SHIPPING_THRESHOLD,
        recommended=recommended,
    )


# ────────────────────────────────────────────────────────────
#  API cart
# ────────────────────────────────────────────────────────────
@app.route("/api/cart/add", methods=["POST"])
def api_cart_add():
    data = request.get_json(silent=True) or request.form
    pid = data.get("product_id")
    qty = int(data.get("qty", 1))

    if not get_product(pid):
        return jsonify({"ok": False, "error": "Unknown product"}), 404

    cart = get_cart()
    cart[pid] = cart.get(pid, 0) + qty
    save_cart(cart)

    return jsonify({"ok": True, "cart_count": cart_count(), "cart": cart})


@app.route("/api/cart/update", methods=["POST"])
def api_cart_update():
    data = request.get_json(silent=True) or request.form
    pid = data.get("product_id")
    qty = int(data.get("qty", 1))

    cart = get_cart()
    if pid not in cart:
        return jsonify({"ok": False, "error": "Not in cart"}), 404

    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    save_cart(cart)

    items, subtotal = build_cart_items(cart)
    shipping = shipping_for(subtotal)

    return jsonify({
        "ok": True,
        "cart_count": cart_count(),
        "subtotal": subtotal,
        "shipping": shipping,
        "total": round(subtotal + shipping, 2),
    })


@app.route("/api/cart/clear", methods=["POST"])
def api_cart_clear():
    session["cart"] = {}
    session.modified = True
    return jsonify({"ok": True, "cart_count": 0})


@app.route("/api/cart")
def api_cart_get():
    items, subtotal = build_cart_items(get_cart())
    return jsonify({
        "items": items,
        "subtotal": subtotal,
        "cart_count": cart_count(),
    })


# ────────────────────────────────────────────────────────────
#  API products
# ────────────────────────────────────────────────────────────
@app.route("/api/products")
def api_products():
    return jsonify([p.to_dict() for p in all_products()])


@app.route("/api/products/<pid>")
def api_product(pid):
    p = get_product(pid)
    if not p:
        return jsonify({"ok": False, "error": "Not found"}), 404
    return jsonify(p.to_dict())


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
