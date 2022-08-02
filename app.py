import json

import werkzeug.security
from flask import Flask, render_template, url_for, request, redirect, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import config
import subprocess


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
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.name


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    count = db.Column(db.Integer, default=0)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form["name"]
        address = request.form["address"]
        phone = request.form["phone"]
        messenger = request.form["messenger"]
        comment = request.form["comment"]
        if request.form["deposit"] == "passport":
            deposit = "паспорт"
        else:
            deposit = "300₾ или 100$"
        order_el = ''
        order_price = 0
        for el in request.form:
            if el.startswith('order_'):
                product_id = el[6:]
                if product_id == "extra-cup":
                    order_el += "Доп.забивка ×" + request.form[el] + " (" + request.form[el] + "×" + str(config.price["Доп.забивка"]) + " GEL); "
                    order_price += int(request.form[el]) * config.price["Доп.забивка"]
                elif product_id == "calyan":
                    order_el += "Кальян ×" + request.form[el]  + " (" + request.form[el] + "×" + str(config.price["Кальян"]) + " GEL); "
                    order_price += int(request.form[el]) * config.price["Кальян"]
                elif product_id == "choise":
                    order_el += "Выберите что-нибудь сами ×" + request.form[el]  + " (" + request.form[el] + "×0 GEL); "
                else:
                    product = Products.query.filter_by(id=product_id).first()
                    order_el += product.name + " ×" + request.form[el]  + " (" + request.form[el] + "×0 GEL); "

        order = Order(name=name, address=address, phone=phone, messenger=messenger, comment=comment, deposit=deposit, order_el=order_el, order_price=order_price, time=datetime.today())
        try:
            db.session.add(order)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении пользователя произошла ошибка"

    else:
        products = Products.query.filter(Products.count > 0).order_by(Products.name.asc()).all()
        for_json = dict()
        for el in products:
            for_json[el.id] = el.name
        return render_template("index.html", products=products, for_json=for_json)


@app.route("/set_order_from_site", methods=["POST"])
def add_order_from_site():
    name = request.form["name"]
    address = request.form["address"]
    phone = request.form["phone"]
    messenger = request.form["messenger"]
    comment = request.form["comment"]
    if request.form["deposit"] == "passport":
        deposit = "паспорт"
    else:
        deposit = "300₾ или 100$"
    order_el = ''
    order_price = 0
    for el in request.form:
        if el.startswith('order_'):
            product_id = el[6:]
            if product_id == "extra-cup":
                order_el += "Доп.забивка ×" + request.form[el] + " (" + request.form[el] + "×" + str(
                    config.price["Доп.забивка"]) + " GEL); "
                order_price += int(request.form[el]) * config.price["Доп.забивка"]
            elif product_id == "calyan":
                order_el += "Кальян ×" + request.form[el] + " (" + request.form[el] + "×" + str(
                    config.price["Кальян"]) + " GEL); "
                order_price += int(request.form[el]) * config.price["Кальян"]
            elif product_id == "choise":
                order_el += "Выберите что-нибудь сами ×" + request.form[el] + " (" + request.form[el] + "×0 GEL); "
            else:
                product = Products.query.filter_by(id=product_id).first()
                order_el += product.name + " ×" + request.form[el] + " (" + request.form[el] + "×0 GEL); "

    order = Order(name=name, address=address, phone=phone, messenger=messenger, comment=comment, deposit=deposit,
                  order_el=order_el, order_price=order_price, time=datetime.today())
    try:
        db.session.add(order)
        db.session.commit()
        return "order_added"
    except:
        return "error"



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
        args = request.args
        get_args = args.to_dict()
        sort = get_args.get("sort")
        products = None
        sort_class = {
            "name": "asc",
            "count": "asc",
            "time": "asc"
        }
        if sort is not None:
            if sort[4:] == "name":
                if sort[:3] == "dsc":
                    products = Products.query.order_by(Products.name.desc()).all()
                    sort_class["name"] = "asc"
                elif sort[:3] == "asc":
                    products = Products.query.order_by(Products.name.asc()).all()
                    sort_class["name"] = "desc"
            elif sort[4:] == "count":
                if sort[:3] == "dsc":
                    products = Products.query.order_by(Products.count.desc()).all()
                    sort_class["count"] = "asc"
                elif sort[:3] == "asc":
                    products = Products.query.order_by(Products.count.asc()).all()
                    sort_class["count"] = "desc"
            elif sort[4:] == "time":
                if sort[:3] == "dsc":
                    products = Products.query.order_by(Products.time.desc()).all()
                    sort_class["time"] = "asc"
                elif sort[:3] == "asc":
                    products = Products.query.order_by(Products.time.asc()).all()
                    sort_class["time"] = "desc"

        else:
            products = Products.query.order_by(Products.time.desc()).all()
            sort_class["time"] = "asc"

        admins = Admin.query.order_by(Admin.time.desc()).all()
        orders = Order.query.order_by(Order.time.desc()).all()
        return render_template("admin.html", logIn=logIn, admins=admins, orders=orders, products=products, sort_class=sort_class)


@app.route("/add_admin", methods=['POST'])
def addAdmin():
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        email = request.form['email']
        password = werkzeug.security.generate_password_hash(request.form['password'])
        user_admin = Admin(name=name, surname=surname, username=username, email=email, password=password,
                           time=datetime.today())

        try:
            db.session.add(user_admin)
            db.session.commit()
            return "added"
        except:
            return "error"


@app.route("/add_product", methods=['POST'])
def addProduct():
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        name = request.form['name']
        description = request.form['description']
        count = request.form['count']

        product = Products(name=name, description=description, count=count, time=datetime.today())
        try:
            db.session.add(product)
            db.session.commit()
            return "added"
        except:
            return "error"


@app.route("/edit_admin/<int:id>", methods=['POST'])
def editAdmin(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        admin = Admin.query.get(id)
        admin.name = request.form['name']
        admin.surname = request.form['surname']
        admin.username = request.form['username']
        admin.email = request.form['email']

        try:
            db.session.commit()
            return "edited"
        except:
            return "error"


@app.route("/edit_order/<int:id>", methods=['POST'])
def editOrder(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        order = Order.query.get(id)
        order.name = request.form['name']
        order.address = request.form['address']
        order.phone = request.form['phone']
        order.order_el = request.form['order_el']
        order.comment = request.form['comment']
        order.deposit = request.form['deposit']

        try:
            db.session.commit()
            return "edited"
        except:
            return "error"


@app.route("/edit_product/<int:id>", methods=['POST'])
def editProduct(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        product = Products.query.get(id)
        product.name = request.form['name']
        product.description = request.form['description']
        product.count = request.form['count']

        try:
            db.session.commit()
            return "edited"
        except:
            return "error"


@app.route("/admin/getUpdate/<int:time_interval>")
def getUpdate(time_interval):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        update = False
        admins = Admin.query.order_by(Admin.time.desc()).all()
        for el in admins:
            if (datetime.now() - el.time).total_seconds() < int(time_interval)/1000:
                update = True
                break
        order = Order.query.order_by(Order.time.desc()).all()
        for el in order:
            if (datetime.now() - el.time).total_seconds() < int(time_interval)/1000:
                update = True
                break
        products = Products.query.order_by(Products.time.desc()).all()
        for el in products:
            if (datetime.now() - el.time).total_seconds() < int(time_interval)/1000:
                update = True
                break
        if update:
            return {"status": "updated"}
        else:
            return {"status": "no_update"}


@app.route("/admin/deleteAdmin/<int:id>")
def deleteAdmin(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        admin = Admin.query.get_or_404(id)
        try:
            db.session.delete(admin)
            db.session.commit()
            return {"status": "deleted"}
        except:
            return {"status": "no_deleted"}


@app.route("/admin/deleteOrder/<int:id>")
def deleteOrder(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        order = Order.query.get_or_404(id)
        try:
            db.session.delete(order)
            db.session.commit()
            return {"status": "deleted"}
        except:
            return {"status": "no_deleted"}


@app.route("/admin/deleteProduct/<int:id>")
def deleteProduct(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        product = Products.query.get_or_404(id)
        try:
            db.session.delete(product)
            db.session.commit()
            return {"status": "deleted"}
        except:
            return {"status": "no_deleted"}


@app.route("/admin/getAdmin/<int:id>")
def getAdmin(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        admin = Admin.query.get_or_404(id)
        for_js = {
            "name": admin.name,
            "surname": admin.surname,
            "username": admin.username,
            "email": admin.email
        }

        return for_js


@app.route("/admin/getOrder/<int:id>")
def getOrder(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        order = Order.query.get_or_404(id)
        for_js = {
            "name": order.name,
            "address": order.address,
            "phone": order.phone,
            "comment": order.comment,
            "deposit": order.deposit,
            "order_el": order.order_el
        }

        return for_js


@app.route("/admin/getProduct/<int:id>")
def getProduct(id):
    if 'username' not in session:
        return {"status": "unauthorized_user"}
    else:
        product = Products.query.get_or_404(id)
        for_js = {
            "name": product.name,
            "description": product.description,
            "count": product.count
        }

        return for_js



@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect('/admin')


@app.route("/legal_policy")
def legal_policy():
    return render_template('legal_policy.html')


@app.route("/cat_page")
def cat_page():
    return render_template('cat_page.html')


@app.route("/set_order", methods=["POST"])
def add_order_from_telegram():
    r = request.json
    order_to_bd = Order(name=r["name"], address=r["address"], phone=r["phone"], messenger=r["messenger"], comment=r["comment"], deposit=r["deposit"], order_el=r["order_el"], order_price=r["order_price"], time=datetime.today())
    try:
        db.session.add(order_to_bd)
        db.session.commit()
        return "True"
    except:
        return ""


@app.route("/set_products")
def set_products_into_telegram():
    products = Products.query.filter(Products.count > 0).order_by(Products.time.desc()).all()
    product = {}
    num = 0
    for el in products:
        product[num] = {"name": el.name}
        num += 1
    return json.dumps(product, indent=4)


@app.route("/set_orders/<int:time_interval>")
def set_orders_into_telegram(time_interval):
    orders = {}
    order = Order.query.order_by(Order.time.desc()).all()
    num = 0
    for el in order:
        if (datetime.now() - el.time).total_seconds() < time_interval:
            orders[num] = {
                    "id": el.id,
                    "name": el.name,
                    "address": el.address,
                    "phone": el.phone,
                    "messenger": el.messenger,
                    "comment": el.comment,
                    "order_el": el.order_el,
                    "order_price": el.order_price
                }

            num += 1
        else:
            break
    return json.dumps(orders, indent=4)


if __name__ == "__main__":
    app.run(debug=True)
