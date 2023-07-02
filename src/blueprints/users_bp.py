from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required, admin_or_user_required
from init import db, bcrypt
from models.user import UserSchema, User
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
import json

users_bp = Blueprint('users', __name__, url_prefix='/users')

# List all users
@users_bp.route('/')
@jwt_required()
def all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

# Get one user
@users_bp.route('/<int:card_id>')
@jwt_required()
def one_user(user_id):
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  if user:
    return UserSchema().dump(user)
  else:
    return {'error': 'Card not found'}, 404

# UPDATE (requires admin or owner)
@users_bp.route('/<int:id>/', methods=['PUT'])
@jwt_required()
def update_one_user(id):
    admin_or_user_required(id)
    try:
        stmt = db.select(User).filter_by(id=id)
        user = db.session.scalar(stmt)

        data = UserSchema().load(request.json, partial=True)
        
        if user: 
            user.name = data.get('name') or user.name
            user.email = data.get('email') or user.email
            user.password = bcrypt.generate_password_hash(data.get('password')).decode('utf8') or user.password
            user.study_times = data.get('study_times') or user.study_times
            user.study_location = data.get('study_location') or user.study_location
            user.interests = data.get('interests') or user.interests
            user.studying = data.get('studying') or user.studying

            db.session.commit()      
            return UserSchema(exclude=['password']).dump(user)
        else:
            return {'error': f'User not found with user id {id}.'}, 404
    except IntegrityError:
       return {'error': 'Cannot have duplicate email addresses'}
    except:
       return {'error': 'Missing data fields'}

# Update a specific entry using PATCH
@users_bp.route('/<int:user_id>', methods=['PATCH'])
def update_entry(user_id):
    updated_fields = request.json

    entry = User.query.get(user_id)
    if not entry:
        response = {'error': 'Entry not found'}
        return json.dumps(response), 404, {'Content-Type': 'application/json'}

    # Update only the provided fields
    for field, value in updated_fields.items():
        if hasattr(entry, field):
            setattr(entry, field, value)

    db.session.commit()

    response = {
        'id': entry.id,
        'name': entry.name,
        'email': entry.email,
        'password': bcrypt.generate_password_hash(entry.password).decode('utf8') or entry.password,
        'study_times': entry.study_times,
        'study_location': entry.study_location,
        'interests': entry.interests,
        'studying': entry.studying,
        'is_admin': entry.is_admin
    }
    return json.dumps(response), 200, {'Content-Type': 'application/json'}
