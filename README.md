# 🌸 Bloomify – Online Flower E-Commerce Website

Bloomify is a web-based flower e-commerce application developed using Python Flask, HTML, CSS, and SQLite. It provides users with a simple and interactive platform to browse flowers, manage their shopping cart and wishlist, place orders, write reviews, and manage their profile.

## ✨ Features

- User registration and login
- Secure password hashing
- Flower product browsing
- Product details and reviews
- Shopping cart management
- Wishlist management
- Checkout and order placement
- Order history
- Order status tracking
- User profile management
- Address management
- Coupon and discount support
- SQLite database integration
- Responsive user interface

## 🛠️ Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- Jinja2

## 🗄️ Database

Bloomify uses SQLite with Flask-SQLAlchemy.

The database contains tables for:

- Users
- Products
- Orders
- Order Items
- Wishlist
- Reviews
- Addresses
- Coupons

## 📂 Project Structure

```text
Bloomify/
│
├── app.py
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── cart.html
│   ├── checkout.html
│   ├── profile.html
│   ├── wishlist.html
│   ├── order_history.html
│   └── ...
│
├── static/
│   ├── style.css
│   └── images/
│
└── instance/
    └── bloomify.db
