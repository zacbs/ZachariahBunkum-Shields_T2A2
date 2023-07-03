from flask_jwt_extended import jwt_required
from init import db
from models.user import LocationSchema, Location
from flask import Blueprint, request


locations_bp = Blueprint('locations', __name__, url_prefix='/locations')

# List all locations
@locations_bp.route('/')
@jwt_required()
def all_locations():
    stmt = db.select(Location)
    locations = db.session.scalars(stmt)
    return LocationSchema(many=True).dump(locations)

# Get one location
@locations_bp.route('/<int:location_id>')
@jwt_required()
def one_location(location_id):
  stmt = db.select(Location).filter_by(id=location_id)
  location = db.session.scalar(stmt)
  if location:
    return LocationSchema().dump(location)
  else:
    return {'error': 'Card not found'}, 404

# UPDATE location details
@locations_bp.route('/<int:id>/', methods=['PUT','PATCH'])
@jwt_required()
def update_one_location(id):
    try:
        stmt = db.select(Location).filter_by(id=id)
        location = db.session.scalar(stmt)

        data = LocationSchema().load(request.json, partial=True)
        
        if location: 
            location.name = data.get('name'),
            location.description = data.get('description')
            db.session.commit()      
            return LocationSchema().dump(location)
        else:
            return {'error': f'location not found with location id {id}.'}, 404
    except:
       return {'error': 'Missing data fields'}


# Delete a location
@locations_bp.route('/<int:location_id>', methods=['DELETE'])
@jwt_required()
def delete_location(location_id):
  stmt = db.select(Location).filter_by(id=location_id)
  location = db.session.scalar(stmt)
  if location:
    db.session.delete(location)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'Card not found'}, 404