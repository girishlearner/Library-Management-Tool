import sqlite3

from flask import Flask, render_template, request, redirect, url_for,jsonify , session
from database import Database

app = Flask(__name__)

db = Database()  

# Initialize the database
with app.app_context(): 
    db.create_tables()

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/<user_type>')
def login(user_type):
    if user_type == 'user_login':
        return render_template('user_login.html')
    elif user_type == 'admin_login':
        return render_template('admin_login.html')
    else:
        return redirect(url_for('index'))

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/user_validation', methods=['POST'])
def user_validation():
    username = request.form['username']
    password = request.form['password']

    # Here you would typically check the database for user credentials
    if username == db.get_user_username() and password == db.get_user_password():
        return render_template('user_dashboard.html', username=username)
    else:
        return "Invalid credentials", 401

@app.route('/admin_validation', methods=['POST'])
def admin_validation():
    admin_username = request.form['admin_username']
    admin_password = request.form['admin_password']

    # Here you would typically check the database for admin credentials
    if admin_username ==  db.get_admin_username() and admin_password == db.get_admin_password():
        return redirect(url_for('admin_dashboard'))
    else:
        return "Invalid admin credentials", 401 

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/user_reg')
def user_reg():
    return render_template('user_register.html')

@app.route('/user_register', methods=['POST'])
def user_registration():
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    dob = request.form['dob']

    # Save user registration data to the database
    try:
        db.insert_user(username, password, address, phone, email, dob)
        return redirect(url_for('user_validation'))
    except Exception as e:
        error_message = str(e)
        return render_template('user_register.html', error=error_message)


@app.route('/view_users', methods=['GET'])
def view_users():
    users = db.fetch_users()
    print(users)  # Debugging line to check fetched users
    return jsonify(users)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True) 

