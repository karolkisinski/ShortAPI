from app import db

class ShortURL(db.Model):

    __tablename__ = 'short_api'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    url = db.Column(db.String(255))
    short_url = db.Column(db.String(50))

    def __init__(self, title, url, short_url):
        self.title = title
        self.url = url
        self.short_url = short_url

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
    
