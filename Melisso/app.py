import os
from flask import (
    Flask, render_template, request,
    session, jsonify, send_from_directory
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "melisso-secret-key-change-me-in-production"

PRODUCTS = {
    "wild-thyme-reserve": {
        "id": "wild-thyme-reserve",
        "name": "Wild Thyme Reserve",
        "price": 28.00, "weight": "250 G",
        "badge": "BESTSELLER", "badge_class": "bg-secondary text-on-secondary",
        "desc": "Intense resinous aroma with mountain pine & lavender.",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuD6MpD3EcgRoqQMXL19LtfaBPaARMRokdXk7J3VrdokRps08OqM67_oT1DrqCqc3t2AtXE3MvSBSVfNZqp4S8Z_jruYf9PQPQffnXq13pt5_2AeL0KZCix2HGQJsPkWyAGEaVmZBP6TJkXFMN7vnoLg4uKzM4dPWxTEuRhP9eWo3NfFa1xqNG2ItKgL2qkoltyKZiOgz3Z127W6RqPgPBRhC_1Bt4sHU4gy2GmPkG4D36QWNOG8eHhNoNoVtyD-HQtDtNM",
    },
    "white-thistle-blossom": {
        "id": "white-thistle-blossom",
        "name": "White Thistle & Blossom",
        "price": 34.00, "weight": "450 G",
        "badge": "PALE SILK", "badge_class": "bg-primary text-on-primary",
        "desc": "Silk cream texture, floral delicacy, smooth buttery finish.",
        "image": "https://lh3.googleusercontent.com/aida/AEtjO1XlrwNEwbK9EDvW76XCsoXz9zBtI5cgnF2ar2Fraei2p80E4o5tl6ptUZITdtpciEEGhyD02axU4xfF4v_R_Y_Ainc2YstXL0UM8KdIqHSOQyRY1-LMWsfY3eua5UMQ0FveWMbnuIpm-gAxJZrhzJUSbu3a2QeXmjSgY5tkcs4TqWxRh86TQf3nRDGI0jvP88Mq-QKYfPmWfO7jElVWIq6pm1I45Ko2YKxEcQoboFrADXFKLpvH3IAmQoaQ",
    },
    "wild-pine-herbs": {
        "id": "wild-pine-herbs",
        "name": "Wild Pine & Mountain Herbs",
        "price": 38.00, "weight": "450 G",
        "badge": "WILD PINE", "badge_class": "bg-tertiary text-on-tertiary",
        "desc": "Dense dark amber honey with savory, oregano and balsamic notes.",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuDlSuNY7Zu7zMkD67ByfD1TeGm4AZsarjc-fZKEqwuVxrJjW-CoUEMq29I4sN5vpBE0cWOOIGAG7llvbuTY_ZCxdngia-1t0ZPshlvfWmXImu-GzH6eLQ10_U6slXvv2dQ83SsxHgrLwZ1nk365ijE1hXtWU_J0ZVM9tGOCWUiYsrqr3S2Fmtlgp7jNs9EKv4xgh8W7-r5ej2rydmv5HIIFz7sKwODAjDKX06qlXSlhfAZTIIzdwBrt-Q",
    },
    "oak-chestnut": {
        "id": "oak-chestnut",
        "name": "Cretan Oak & Wild Chestnut",
        "price": 42.00, "weight": "450 G",
        "badge": "OAK & CHESTNUT", "badge_class": "bg-primary-container text-on-primary-container",
        "desc": "Deep dark honeydew honey with caramelized malt and walnut notes.",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuD1H_HujxWM6qtfQMI2VmPSdGjj3QtI30InvRCsfaYDWdAjfTn9vA_2hSOWVCkE-9fsD0jrQ-auRVCiaaU_PwypNDGgjJY9nKs5hkwswLidyGqESN99xLxO4McONzQGUwpRJiwy_2aHuInV3a4znWjooPzZ9B1Nj4WailSoNLKS1Uk-lbV2EP4_EiHAwL6HbfP4apRLRZQM1Y8PHANCUf2qWc4Ir3-L6KMC3Xs42xrc750BAU3or1lTOA",
    },
    "raw-honeycomb": {
        "id": "raw-honeycomb",
        "name": "Raw Honeycomb Reserve",
        "price": 42.00, "weight": "500 G",
        "badge": "RAW COMB", "badge_class": "bg-secondary-container text-on-secondary-container",
        "desc": "Whole cellular honeycomb sealed with beeswax.",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAKrXqriDqJ3fdsJII8dBkmv5_RieqrtTFop4kkK7U2lVmvx4rEq__YEm6yGpmi3UaqeFhN6CFj3QPGwY-7yoiE8NxJmCvcVBVD9vjeK0RkcElPBXP3k0a2P9T_APFot0S3KF0NPg5qzTxOKsmpzFRpZrw3ZcWg-4Na00mEfzobxNpqgGHENedR9QdcqvVTidb8oMd3DgVNIw_rXS7RllV-7Eb0NHoYhWIuIlLu7xyVXa2VEhTePIeS_A",
    },
    "tasting-trio": {
        "id": "tasting-trio",
        "name": "Tasting Discovery Trio Box",
        "price": 95.00, "weight": "3 × 450 G",
        "badge": "GIFT SET", "badge_class": "bg-secondary text-on-secondary",
        "desc": "Collector's gift set: Thyme, Fleur d'Oranger, Mountain Pine.",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBqvFWDx_KorzHuuVECxcbzCpYkl-f5CRD6Y4Cz_AhJRziUiXAjA0SUqdXWDuCQmf1n32yC3yS3vjumezvNaNBmLIk6Yf6Lr7_wBxEkNpzs7twBfkJCIMKnNfGwrIxUkRG7aDxH2qUaGJTgWbXIS-RpH1Kgcb_M__wnu1ozaQYKqEPNM6vHbFZGo4yL_8Vz4qAGk070j1IMhRiCsbYCssQGFZl3QRJg9bOV2y0ap0E85u7Me3wScl1L-g",
    },
}

FREE_SHIPPING_THRESHOLD = 80.0


def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def build_cart_items(cart):
    items, subtotal = [], 0.0
    for pid, qty in cart.items():
        p = PRODUCTS.get(pid)
        if not p:
            continue
        line = p["price"] * qty
        subtotal += line
        items.append({**p, "qty": qty, "line_total": round(line, 2)})
    return items, round(subtotal, 2)


def cart_count():
    return sum(get_cart().values())


@app.context_processor
def inject_cart_count():
    return {"cart_count": cart_count()}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cart")
def cart_page():
    cart = get_cart()
    items, subtotal = build_cart_items(cart)
    shipping = 0.0 if subtotal >= FREE_SHIPPING_THRESHOLD or subtotal == 0 else 6.90
    total = round(subtotal + shipping, 2)
    return render_template(
        "cart.html",
        items=items, subtotal=subtotal, shipping=shipping, total=total,
        free_shipping_threshold=FREE_SHIPPING_THRESHOLD,
        recommended=list(PRODUCTS.values())[:4],
    )


@app.route("/api/cart/add", methods=["POST"])
def api_cart_add():
    data = request.get_json(silent=True) or request.form
    pid = data.get("product_id")
    qty = int(data.get("qty", 1))
    if pid not in PRODUCTS:
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
    shipping = 0.0 if subtotal >= FREE_SHIPPING_THRESHOLD or subtotal == 0 else 6.90
    return jsonify({
        "ok": True, "cart_count": cart_count(),
        "subtotal": subtotal, "shipping": shipping,
        "total": round(subtotal + shipping, 2),
    })


@app.route("/api/cart")
def api_cart_get():
    cart = get_cart()
    items, subtotal = build_cart_items(cart)
    return jsonify({"items": items, "subtotal": subtotal, "cart_count": cart_count()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
