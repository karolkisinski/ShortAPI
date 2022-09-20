import secrets
from app import db

class ShortURL(db.Model):

    __tablename__ = 'short_api'
    chars = "ABCDEFGHIJKLMNOQPRSTWUZXV"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    url = db.Column(db.String(255))
    short_url = db.Column(db.String(50))
    def shortest(self):
        chars = "ABCDEFGHIJKLMNOQPRSTWUZXV"
        s_url = "".join(secrets.choice(chars) for _ in range(8))
        


    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.short_url = "".join(secrets.choice(self.chars) for _ in range(8))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ShortURL.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "".format(self.title, self.short_url, self.url)
    
