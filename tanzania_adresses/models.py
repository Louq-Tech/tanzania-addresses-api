from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Regions(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(3))

    def __repr__(self) -> str:
        return f'<Region> {self.name}>'
