from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'foo123'

db.init_app(app)

@app.route('/')
def home():
  return render_template('home.html')

if __name__ == '__main__':
  app.run(debug=True)