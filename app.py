from flask import Flask, render_template, redirect, url_for, flash, session
# from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm, FeedbackForm
from models import db, User, Feedback
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
  if 'username' in session:
    flash('You are already logged in', 'info')
    return redirect(url_for('user_profile', username=session['username']))

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

      return redirect(url_for('user_profile', username=user.username))

  return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
  if 'username' in session:
    flash('You are already logged in', 'info')
    return redirect(url_for('user_profile', username=session['username']))

  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.verify_password(form.password.data):
      session['username'] = user.username
      flash('Logged in successfully', 'success')
      return redirect(url_for('user_profile', username=user.username))
    flash('Invalid username or password', 'danger')

  return render_template('login.html', form=form)

@app.route('/users/<username>')
@login_required
def user_profile(username):
  if 'username' not in session or session['username'] != username:
    flash("You are not authorized to view this page", "danger")
    return redirect(url_for('login'))
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('user_profile.html', user=user)

@app.route('/logout', methods=['POST'])
def logout():
  session.pop('username', None)
  flash('You have been logged out', 'info')
  return redirect(url_for('register'))

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
@login_required
def add_feedback(username):
  if 'username' not in session or session['username'] != username:
    flash("You  are not authorized to add feedback for this user", "danger")
    return redirect(url_for('login'))

  form = FeedbackForm()
  if form.validate_on_submit():
    feedback = Feedback(
      title=form.title.data,
      content=form.content.data,
      username=username
    )
    db.session.add(feedback)
    db.session.commit()
    flash('Feedback added successfully', 'success')
    return redirect(url_for('user_profile', username=username))

  return render_template('add_feedback.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404/html'), 404

@app.errorhandler(401)
def unauthorized(e):
  return render_template('401.html'), 401

if __name__ == '__main__':
  app.run(debug=True)