from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    name_place = db.Column(db.String(200), unique=True, nullable=False)
    name_country = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    link_photo = db.Column(db.String(255), nullable=True)  # صورة أو لينك الصورة
    flag = db.Column(db.String(255), nullable=True)  # علم الدولة
    link_pa = db.Column(db.String(255), nullable=True)  # رابط إضافي لو عايز تضيفه
    details_url = db.Column(db.String(255), nullable=True)  # رابط التفاصيل للمكان

    def __repr__(self):
        return f"<Place {self.name_place}>"
