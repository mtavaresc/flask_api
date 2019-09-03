from passlib.hash import pbkdf2_sha256 as sha256

from app import db


class User(db.Model):
    """This class represents the user table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, username, password):
        """initialize with name"""
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, _hash):
        return sha256.verify(password, _hash)

    def __repr__(self):
        return f'<User: {self.name}>'
