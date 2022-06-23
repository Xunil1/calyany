import werkzeug.security
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = config.SECRET_KEY
db = SQLAlchemy(app)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Admin %r>' % self.name


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    messenger = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    deposit = db.Column(db.String(100), nullable=False)
    order_el = db.Column(db.Text, nullable=False)
    order_price = db.Column(db.Float, default=0)
    status = db.Column(db.String(100), default="Принят")
    time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.name


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, default=0)
    count = db.Column(db.Integer, default=0)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        products = Products.query.order_by(Products.time.desc()).all()
        return render_template("index.html", products=products)


@app.route("/admin", methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        user_admin = Admin.query.filter_by(username=request.form['username']).first()
        if werkzeug.security.check_password_hash(user_admin.password, request.form['password']):
            session['username'] = request.form['username']
        return redirect('/admin')
    else:
        if 'username' not in session:
            logIn = False
        else:
            logIn = True
        admins = Admin.query.order_by(Admin.time.desc()).all()
        orders = Order.query.order_by(Order.time.desc()).all()
        products = Products.query.order_by(Products.time.desc()).all()
        return render_template("admin.html", logIn=logIn, admins=admins, orders=orders, products=products)


@app.route("/add_admin", methods=['POST', 'GET'])
def addAdmin():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        email = request.form['email']
        password = werkzeug.security.generate_password_hash(request.form['password'])
        user_admin = Admin(name=name, surname=surname, username=username, email=email, password=password)

        try:
            db.session.add(user_admin)
            db.session.commit()
            return redirect('/admin')
        except:
            return "При добавлении пользователя произошла ошибка"
    else:
        if 'username' not in session:
            return redirect('/admin')
        else:
            return render_template("add_admin.html")


@app.route("/add_product", methods=['POST', 'GET'])
def addProduct():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        count = request.form['count']

        product = Products(name=name, description=description, price=price, count=count, time=datetime.today())

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/admin')
        except:
            return "При добавлении карточки произошла ошибка"
    else:
        if 'username' not in session:
            return redirect('/admin')
        else:
            return render_template("add_products.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect('/admin')


@app.route("/legal_policy")
def legal_policy():
    return render_template('legal_policy.html')


def add_order_from_telegram(order):
    order_to_bd = Order(name=order["name"], address=order["address"], phone=order["phone"], messenger=order["messenger"], comment=order["comment"], deposit=order["deposit"], order_el=order["order_el"], time=datetime.today(), update_time=datetime.today())
    try:
        db.session.add(order_to_bd)
        db.session.commit()
        return True
    except:
        return False

def set_products_into_telegram():
    products = Products.query.order_by(Products.time.desc()).all()
    return products


if __name__ == "__main__":
    app.run(debug=True)