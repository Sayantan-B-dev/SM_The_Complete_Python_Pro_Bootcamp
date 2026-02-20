from . import db

class Cafe(db.Model):
    __tablename__ = 'cafe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    map_url = db.Column(db.String(200))
    img_url = db.Column(db.String(200))
    location = db.Column(db.String(100))
    has_sockets = db.Column(db.String(5))      # 'TRUE' or 'FALSE'
    has_toilet = db.Column(db.String(5))
    has_wifi = db.Column(db.String(5))
    can_take_calls = db.Column(db.String(5))
    seats = db.Column(db.String(20))
    coffee_price = db.Column(db.String(10))    # stored as string, e.g., "2.40"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}