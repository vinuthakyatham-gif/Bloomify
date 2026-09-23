import random
import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bloomify.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20))
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    offer = db.Column(db.String(50))
    rating = db.Column(db.String(20))
    reviews = db.Column(db.Integer, default=0)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)  
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    payment = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Order Placed")
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)
flowers = {
    "Rose": {
    "name": "Rose",
    "price": 299,
    "image": "rose.jpg",
    "offer": "25% OFF",
    "rating": "⭐⭐⭐⭐⭐",
    "reviews": 248,
    "quantity": 1,
    "category": "Roses",
    "description": "Beautiful fresh roses arranged with love, perfect for birthdays, anniversaries and special occasions."
},
    
"Tulip": {
    "name": "Tulip",
    "price": 399,
    "image": "tulip.jpg",
    "offer": "20% OFF",
    "rating": "⭐⭐⭐⭐☆",
    "reviews": 189,
    "category": "Tulips",
    "description": "Fresh colorful tulips that bring elegance and happiness to every special moment."
},
"Jasmine": {
    "name": "Jasmine",
    "price": 199,
    "image": "jasmine.jpg",
    "offer": "20% OFF",
    "rating": "⭐⭐⭐⭐⭐",
    "reviews": 312,
    "category": "Jasmine",
    "description": "Fragrant jasmine flowers, perfect for creating a fresh and beautiful atmosphere."
},
"Hibiscus": {
    "name": "Hibiscus",
    "price": 249,
    "image": "hibiscus.jpg",
    "offer": "24% OFF",
    "rating": "⭐⭐⭐⭐☆",
    "reviews": 154,
    "category": "Hibiscus",
    "description": "Bright and beautiful hibiscus flowers, perfect for gifting and special occasions."
},
"Sunflower": {
    "name": "Sunflower",
    "price": 299,
    "image": "sunflower.jpg",
    "offer": "21% OFF",
    "rating": "⭐⭐⭐⭐⭐",
    "reviews": 276,
    "category": "Sunflowers",
    "description": "Cheerful sunflowers that bring warmth, positivity and a little sunshine to your day."
},
    
}

users = {}
reviews = {
    "Rose": [],
    "Tulip": [],
    "Jasmine": [],
    "Hibiscus": [],
    "Sunflower": []
}

gifts = {
    "Teddy Bear": {
        "name": "Teddy Bear",
        "price": 499,
        "image": "teddy.jpg"
    },

    "Chocolate Box": {
        "name": "Chocolate Box",
        "price": 349,
        "image": "chocolate.jpg"
    },

    "Greeting Card": {
        "name": "Greeting Card",
        "price": 99,
        "image": "card.jpg"
    },

    "Flower Combo": {
        "name": "Flower Combo",
        "price": 699,
        "image": "combo.jpg"
    }
}
@app.route("/gifts")
def gifts_page():
    return render_template(
        "gifts.html",
        gifts=gifts
    )

@app.route("/add/<flower>")
def add_to_cart(flower):

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    if flower in flowers:
        current = flowers[flower]
    elif flower in gifts:
        current = gifts[flower]
    else:
        return "Item not found"

    for item in cart:
        if item["name"] == current["name"]:
            item["quantity"] = item.get("quantity", 1) + 1
            session["cart"] = cart
            session.modified = True
            flash("🌸 " + " + ".join(item["name"] for item in cart) + " are in your cart!")
            return redirect("/cart")

    new_item = current.copy()
    new_item["quantity"] = 1
    cart.append(new_item)

    session["cart"] = cart
    session.modified = True
    flash("🌸 " + " + ".join(item["name"] for item in cart) + " are in your cart!")

    return redirect("/cart")
@app.route("/buy-now/<flower>")
def buy_now(flower):

    if flower not in flowers:
        return "Flower Not Found"

    item = flowers[flower].copy()
    item["quantity"] = 1

    session["cart"] = [item]
    session.modified = True

    return redirect("/checkout")

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/home")
def home():

    search = request.args.get("search", "").strip().lower()

    filtered_flowers = {}

    for name, flower in flowers.items():

        if (
            search == ""
            or search in name.lower()
            or search in flower["category"].lower()
        ):
            filtered_flowers[name] = flower

    cart = session.get("cart", [])
    wishlist = session.get("wishlist", [])

    return render_template(
        "home.html",
        flowers=filtered_flowers,
        cart_count=len(cart),
        wishlist_count=len(wishlist)
    )
@app.route("/category/<category>")
def category(category):

    filtered = {}

    for name, flower in flowers.items():
        if category.lower() in flower["category"].lower():
            filtered[name] = flower

    return render_template(
        "categories.html",
        flowers=filtered,
        category=category
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        gender = request.form["gender"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered"

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            gender=gender
)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.name
            session["email"] = user.email
            return redirect("/home")

        return "Invalid Email or Password"

    return render_template("login.html")




@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/home")
@app.route("/flower-details/<flower>")
def flower_details(flower):
    if flower not in flowers:
        return "Flower Not Found"

    product = Product.query.filter_by(name=flower).first()

    if not product:
        return "Product not found"

    db_reviews = Review.query.filter_by(
        product_id=product.id
    ).order_by(Review.id.desc()).all()

    return render_template(
        "flower_details.html",
        flower=product,
        reviews=db_reviews
    )


@app.route("/review/<flower>", methods=["POST"])
def review(flower):
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    product = Product.query.filter_by(name=flower).first()

    if not product:
        return "Product not found"

    name = request.form["name"]
    rating = int(request.form["rating"])
    comment = request.form["comment"]

    new_review = Review(
        user_id=user.id,
        product_id=product.id,
        name=name,
        rating=rating,
        comment=comment
    )

    db.session.add(new_review)
    db.session.commit()

    return redirect("/flower-details/" + flower)

@app.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    total = 0
    for flower in cart_items:
        if isinstance(flower, dict):
            total += flower["price"] * flower.get("quantity", 1)

    return render_template(
        "cart.html",
        flowers=cart_items,
        total=total
    )
@app.route("/wishlist/<flower_name>")
def wishlist(flower_name):
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    product = Product.query.filter_by(name=flower_name).first()

    if not product:
        return "Product not found"

    existing = Wishlist.query.filter_by(
        user_id=user.id,
        product_id=product.id
    ).first()

    if not existing:
        new_wishlist = Wishlist(
            user_id=user.id,
            product_id=product.id
        )

        db.session.add(new_wishlist)
        db.session.commit()

        flash(f"💖 {flower_name} added to wishlist!")

    return redirect("/home")

@app.route("/wishlist")
def wishlist_page():
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    wishlist_items = Wishlist.query.filter_by(user_id=user.id).all()

    wishlist_flowers = []

    for item in wishlist_items:
        product = Product.query.get(item.product_id)

        if product:
            wishlist_flowers.append(product)

    return render_template(
        "wishlist.html",
        flowers=wishlist_flowers
    )

@app.route("/remove-wishlist/<flower_name>")
def remove_wishlist(flower_name):
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    product = Product.query.filter_by(name=flower_name).first()

    if not product:
        return "Product not found"

    wishlist_item = Wishlist.query.filter_by(
        user_id=user.id,
        product_id=product.id
    ).first()

    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()

    return redirect("/wishlist")

@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")
@app.route("/remove/<int:index>")
def remove(index):

    cart = session.get("cart", [])

    if 0 <= index < len(cart):
        cart.pop(index)

    session["cart"] = cart
    session.modified = True

    return redirect("/cart")
@app.route("/increase/<int:index>")
def increase(index):

    cart = session.get("cart", [])

    if 0 <= index < len(cart):
        cart[index]["quantity"] += 1

    session["cart"] = cart
    session.modified = True

    return redirect("/cart")


@app.route("/decrease/<int:index>")
def decrease(index):

    cart = session.get("cart", [])

    if 0 <= index < len(cart):

        if cart[index]["quantity"] > 1:
            cart[index]["quantity"] -= 1
        else:
            cart.pop(index)

    session["cart"] = cart
    session.modified = True

    return redirect("/cart")
@app.route("/checkout")
def checkout():
    if "email" not in session:
        return redirect("/login")

    cart_items = session.get("cart", [])

    cart_items = session.get("cart", [])

    if not cart_items:
        return redirect("/cart")

    total = 0

    for flower in cart_items:
        total += flower["price"] * flower.get("quantity", 1)

    discount = session.get("discount", 0)

    discount_amount = total * discount / 100

    final_total = total - discount_amount

    return render_template(
        "checkout.html",
        flowers=cart_items,
        total=total,
        discount=discount,
        final_total=final_total
    )
@app.route("/placeorder", methods=["POST"])
def placeorder():
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    phone = request.form["phone"]
    address = request.form["address"]
    payment = request.form["payment"]

    cart_items = session.get("cart", [])

    if not cart_items:
        return redirect("/cart")

    order_id = "BLM" + str(random.randint(1000, 9999))

    discount = session.get("discount", 0)

    total = sum(
        item["price"] * item.get("quantity", 1)
        for item in cart_items
    )

    final_total = total * (1 - discount / 100)

    new_order = Order(
        order_id=order_id,
        user_id=user.id,
        name=user.name,
        phone=phone,
        address=address,
        payment=payment,
        total=final_total,
        status="Order Placed"
    )

    db.session.add(new_order)
    db.session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=0,
            product_name=item["name"],
            price=item["price"],
            quantity=item.get("quantity", 1)
        )

        db.session.add(order_item)

    db.session.commit()

    session.pop("cart", None)
    session.pop("discount", None)

    return render_template(
        "thankyou.html",
        name=user.name,
        payment=payment,
        order_id=order_id
    )
@app.route("/orders")
def orders():
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    orders = Order.query.filter_by(
        user_id=user.id
    ).order_by(Order.id.desc()).all()

    return render_template(
        "order_history.html",
        orders=orders,
        order_items={
            order.id: OrderItem.query.filter_by(order_id=order.id).all()
            for order in orders
        }
    )
@app.route("/update_order/<order_id>/<status>")
def update_order(order_id, status):
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    order = Order.query.filter_by(
        order_id=order_id,
        user_id=user.id
    ).first()

    if not order:
        return "Order not found"

    allowed_statuses = [
        "Shipped",
        "Out for Delivery",
        "Delivered",
        "Cancelled"
    ]

    if status not in allowed_statuses:
        return "Invalid order status"

    order.status = status
    db.session.commit()

    return redirect("/orders")
@app.route("/profile")
def profile():
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    if user.gender == "Male":
        image = "boy.png"
    else:
        image = "girl.png"

    order_count = Order.query.filter_by(user_id=user.id).count()

    wishlist_count = Wishlist.query.filter_by(
        user_id=user.id
    ).count()

    cart_count = sum(
        item.get("quantity", 1)
        for item in session.get("cart", [])
        if isinstance(item, dict)
    )

    address = Address.query.filter_by(
        user_id=user.id
    ).first()

    return render_template(
        "profile.html",
        user=user.name,
        image=image,
        order_count=order_count,
        wishlist_count=wishlist_count,
        cart_count=cart_count,
        address=address.address if address else ""
    )
@app.route("/save_address", methods=["POST"])
def save_address():
    if "email" not in session:
        return redirect("/login")

    email = session.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    address_text = request.form["address"]

    existing_address = Address.query.filter_by(
        user_id=user.id
    ).first()

    if existing_address:
        existing_address.address = address_text
    else:
        new_address = Address(
            user_id=user.id,
            address=address_text
        )
        db.session.add(new_address)

    db.session.commit()

    return redirect("/profile")
@app.route("/apply_coupon", methods=["POST"])
def apply_coupon():

    coupon = request.form["coupon"].upper()

    if coupon == "BLOOM10":
        session["discount"] = 10
    else:
        session["discount"] = 0

    return redirect("/checkout")

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    email = session.get("email")

    if not email:
        return redirect("/login")

    user = User.query.filter_by(email=email).first()

    if not user:
        return redirect("/login")

    if request.method == "POST":
        new_name = request.form["name"]
        new_email = request.form["email"]

        existing_user = User.query.filter_by(email=new_email).first()

        if existing_user and existing_user.id != user.id:
            return "Email already registered"

        user.name = new_name
        user.email = new_email

        db.session.commit()

        session["email"] = new_email
        session["user"] = new_name

        return redirect("/profile")

    return render_template(
        "edit_profile.html",
        name=user.name,
        email=user.email
    )

with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)
