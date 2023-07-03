from flask import Blueprint
from init import db, bcrypt
from models.user import User, Location


cli_bp = Blueprint('db', __name__)

# Drop all tables and create new tables i.e. reseting db
@cli_bp.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("Tables created successfully")

# Seed database with random test data
@cli_bp.cli.command("seed")
def seed_db():
    users = [
        User(
            name='John Paul',
            email='jpaul5@fakeemail.com',
            password=bcrypt.generate_password_hash('password123').decode('utf-8'),
            study_times='After 5pm',
            studying='Information technology',
        ),
        User(
            name='Arden Kayley',
            email='akayl2@realemail.com',
            password=bcrypt.generate_password_hash('greatpass44').decode('utf-8'),
            study_times='Anytime weekends only',
            interests='Animals, hiking',
            studying='Civil Engineering'
        ),
        User(
            name='Leslie Doris',
            email='ldori9@fakeemail.com',
            password=bcrypt.generate_password_hash('notfake20').decode('utf-8'),
            study_times='Anytime',
            interests='computers, video games',
            studying='Computer Science'
        ),
        User(
            name='Camden Gilbert',
            email='cgilb2@gmail.com',
            password=bcrypt.generate_password_hash('reallygoodpass@1').decode('utf-8'),
            study_times='Anytime on weekdays',
            interests='Hanging out with friends',
        ),
        User(
            name='Kev Braidy',
            email='kbraid10@anemail.com.au',
            password=bcrypt.generate_password_hash('realpass21').decode('utf-8'),
            is_admin=True
        ),
    ]

    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()
    locations = [
        Location(
            name='On campus - library',
            description='campus library study area'
        ),
        Location(
            name='On campus - outdoor study',
            description='main entrance study area, outdoor seating'
        )
    ]

    db.session.query(Location).delete()
    db.session.add_all(locations)
    db.session.commit()

    users[0].study_locations.append(locations[0])
    users[1].study_locations.append(locations[1])
    users[2].study_locations.append(locations[1])
    users[3].study_locations.append(locations[0])
    db.session.commit()
    print("Data seeded successfully")