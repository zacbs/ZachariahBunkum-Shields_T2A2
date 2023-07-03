from init import db, ma
from marshmallow import fields

user_location = db.Table('user_location',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('locations.id')))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    study_times = db.Column(db.String)
    interests = db.Column(db.String)
    studying = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    study_locations = db.relationship('Location', secondary=user_location, back_populates='users_locations')

class UserSchema(ma.Schema):
    study_locations = fields.List(fields.Nested('LocationSchema', exclude=['users_locations']))
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'study_times', 'study_location', 'interests', 'studying', 'is_admin', 'study_locations')


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    users_locations = db.relationship('User', secondary=user_location, back_populates='study_locations')


class LocationSchema(ma.Schema):
    users_locations = fields.List(fields.Nested('UserSchema', exclude=['study_locations', 'password', 'email', 'is_admin']))
    class Meta:
        fields = ('id', 'name', 'description', 'users_locations')