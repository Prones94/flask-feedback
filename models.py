from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'

  username = db.Column(db.String(20), primary_key=True, unique=True)
  password_hash = db.Column(db.Text, nullable=False)
  email = db.Column(db.String(50), nullable=False, unique=True)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)

  @property
  def password(self):
    raise AttributeError('Password is not a readable attribute')

  @password.setter
  def password(self, plaintext_password):
    self.password_hash = generate_password_hash(plaintext_password)

  def verify_password(self, plaintext_password):
    return check_password_hash(self.password_hash, plaintext_password)
