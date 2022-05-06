from crypt import methods
from click import password_option
from flask import Flask, url_for, render_template, redirect, request
import flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# mongodb connection codes

# mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/users")
# db = mongodb_client.db
app.config["MONGO_URI"] = "mongodb://localhost:27017/User"
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/math')
def math():
    return render_template('math.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    users = db.users

    if request.method == 'POST':
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            users.insert_one({'name': request.form['name'],
                              'email': request.form['email'],
                              'password': request.form['password']})
            return redirect(url_for('main'))

        return "That email already exists! Please enter a different email"

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    users = db.users

    if request.method == 'POST':

        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if request.form['password'] == login_user['password']:
                return redirect(url_for('main'))
        return "wrong email/ password!" + f"{login_user['password']}"
    return render_template('login.html')


@app.route('/admin-login', methods=['POST', 'GET'])
def admin_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email == "omarzai@search.ai" and password == "112233":
            return redirect(url_for('admin'))

        return "wrong password/email!"

    return render_template('admin-login.html')


@app.route('/admin')
def admin():
    users = db.users.find()
    return render_template('admin.html', users=users)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    users = db.users.find()

    if request.method == 'POST':
        db.users.delete_one({"email": request.form['email_id']})

    return render_template('delete.html', users=users)


@app.route('/edit', methods=['POST', 'GET'])
def edit():

    if request.method == 'POST':
        db.users.delete_one({"email": request.form['email_id']})
        return render_template('updateUser.html')

    users = db.users.find()
    return render_template('edit.html', users=users)


@app.route('/updateUser', methods=['POST', 'GET'])
def updateUSer():
    users = db.users

    if request.method == 'POST':
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            users.insert_one({'name': request.form['name'],
                              'email': request.form['email'],
                              'password': request.form['password']})
            return redirect(url_for('edit'))

        return "That email already exists! Please enter a different email"

    return render_template('updateUser.html')


if __name__ == '__main__':
    app.run()
