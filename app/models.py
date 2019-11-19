from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Student(UserMixin, db.Model):
    """
    Create an Student table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Student: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class University(db.Model):
    """
    Create a University table
    """

    __tablename__ = 'universities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    students = db.relationship('Student', backref='university',
                                lazy='dynamic')

    def __repr__(self):
        return '<University: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    students = db.relationship('Student', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Events(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    location = db.Column(db.String(40))
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    eventtype_id = db.Column(db.Integer, db.ForeignKey('eventtype.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    event_type = db.Column(db.String(20))
    students = db.relationship('Student', backref='events',
                                lazy='dynamic')

    def __repr__(self):
        return '<Event: {}>'.format(self.name)

class Rso(db.Model):
    """
    Create RSO table
    """
    __tablename__ = 'rso'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    def __repr__(self):
        return '<Rso: {}>'.format(self.name)

class Comments(db.Model):
    """
    Create Comments table
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    comment = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.Date)
    def __repr__(self):
        return '<Comments: {}>'.format(self.name)

class EventType(db.Model):
    """
    Create a Role table
    """
    __tablename__ = 'eventtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    def __repr__(self):
        return '<Eventtype: {}>'.format(self.name)