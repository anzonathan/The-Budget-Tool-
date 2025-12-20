from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Expense, Category
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SECRET_KEY']= 'mysecretkey'

# Configure SQL Alchemy
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Routes
@app.route('/')
def home():
    return '<h1>Welcome to Budget Tool!<h1>'



# # Login
# @app.route("/login", methods=["POST"])
# def login():
#     # Collect info from the form 
#     username = request.form['username']
#     password = request.form['password']
#     user = User.query.filter_by(username=username).first()
#     if user and user.check_password(password):
#         session['username']= username
#         return redirect(url_for('dashboard'))
#         pass
#     else:
#         return render_template("index.html")



# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])


        if User.query.filter_by(username = username).first():
            flash('Username already exists!', 'error')

        else:
            new_user = User(username = username, password = password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration Successful. Please login!', 'success')
            return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username= request.form['username']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    Expenses = Expense.query.filter_by(user_id= current_user.id).all()
    





# # Dashboard
# @app.route("/dashboard")
# def dashboard():
#     if "username" in session:
#         return render_template("dashboard.html", username=session['username'])
#     return redirect(url_for('home'))



# # Logout
# @app.route("/logout")
# def logout():
#     session.pop('username',None)
#     return redirect(url_for('home'))



if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)