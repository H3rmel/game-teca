from gameteca import db

class Users(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name