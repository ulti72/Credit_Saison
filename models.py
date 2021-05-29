from extension import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(50))
    card_type = db.Column(db.String(50))
    card_number = db.Column(db.String(50))
    scheme = db.Column(db.String(50))
    hit_count = db.Column(db.Integer)