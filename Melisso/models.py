from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    weight = db.Column(db.String(32), nullable=False)
    badge = db.Column(db.String(64), nullable=False)
    badge_class = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)


    stock = db.Column(db.Integer, default=0)
    batch = db.Column(db.String(32), default="2024")
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "badge": self.badge,
            "badge_class": self.badge_class,
            "desc": self.description,
            "image": self.image,
            "stock": self.stock,
            "batch": self.batch,
        }

    def __repr__(self):
        return f"<Product {self.id}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    email = db.Column(db.String(128))
    total = db.Column(db.Float)
    currency = db.Column(db.String(8), default="EUR")
    status = db.Column(db.String(32), default="pending")

    def __repr__(self):
        return f"<Order #{self.id} {self.status}>"