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
    time = db.Column(db.DateTime, default=datetime.today())

    def __repr__(self):
        return '<Admin %r>' % self.name


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template("index.html")


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
        return render_template("admin.html", logIn=logIn, admins=admins)


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
            return "При добавлении карточки произошла ошибка"
    else:
        return render_template("add_admin.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True)