from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_project"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'foo123'

@app.route('/')
def home():
  return "Hello, World"

if __name__ == '__main__':
  app.run(debug=True)