from flask import Flask, render_template, redirect, url_for, flash, session
# from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm
from models import db, User
from flask_wtf import CSRFProtect
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'foo123'

db.init_app(app)
csrf = CSRFProtect(app)

with app.app_context():
  db.create_all()

def login_required(f):
  from functools import wraps
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'username' not in session:
      flash('Please log in first', 'danger')
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return decorated_function

@app.route('/')
def home():
  return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return render_template('register.html', form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        flash('Registration successful! Welcome, {}!'.format(user.first_name), 'success')

        return redirect(url_for('secret'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.verify_password(form.password.data):
      session['username'] = user.username
      flash('Logged in successfully', 'success')
      return redirect(url_for('secret'))
    else:
      flash('Invalid username or password', 'danger')
  return render_template('login.html', form=form)

@app.route('/secret')
@login_required
def secret():
  return render_template('secret.html')

@app.route('/logout', methods=['POST'])
def logout():
  session.pop('username', None)
  flash('You have been logged out', 'info')
  return redirect(url_for('register'))

if __name__ == '__main__':
  app.run(debug=True)