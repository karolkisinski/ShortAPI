import secrets
from app import db
from flask_bcrypt import Bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    urls = db.relationship(
                'ShortURL', order_by='ShortURL.id', cascade='all, delete-orphan'
    )

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def is_password_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()


class ShortURL(db.Model):

    __tablename__ = 'short_api'
    chars = "ABCDEFGHIJKLMNOQPRSTWUZXV"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    url = db.Column(db.String(255))
    short_url = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def shortest(self):
        chars = "ABCDEFGHIJKLMNOQPRSTWUZXV"
        s_url = "".join(secrets.choice(chars) for _ in range(8))
        


    def __init__(self, title, url, created_by):
        self.title = title
        self.url = url
        self.short_url = "".join(secrets.choice(self.chars) for _ in range(8))
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return ShortURL.query.all(created_by=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "".format(self.title, self.short_url, self.url)
    
