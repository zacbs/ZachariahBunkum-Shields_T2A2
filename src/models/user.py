from init import db, ma
from marshmallow.validate import ValidationError
from marshmallow import fields, validates_schema

# List of valid study locations
VALID_LOCATIONS = ['On campus - Library', 'On Campus - Outdoor study','On campus - Study hall' , 'Online', 'NULL']

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    study_times = db.Column(db.String)
    study_location = db.Column(db.String)
    interests = db.Column(db.String)
    studying = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)


class UserSchema(ma.Schema):
    # @validates_schema()
    # def validate_study_location(self, data, **kwargs):
    #     study_location = [x for x in VALID_LOCATIONS if x.upper() == data['study_location'].upper()]
    #     if len(study_location) == 0:
    #         raise ValidationError(f'Location must be one of: {VALID_LOCATIONS}')

    #     data['study_location'] = study_location[0]
    class Meta:
        fields = ('name', 'email', 'password', 'study_times', 'study_location', 'interests', 'studying', 'is_admin')