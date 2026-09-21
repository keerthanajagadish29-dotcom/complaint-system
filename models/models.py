from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """
    User Model representing standard users (Students, Faculty, Staff)
    who register to log complaints and track resolution.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-Many Relationship: One User -> Multiple Complaints
    complaints = db.relationship('Complaint', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Hashes and sets the user password using Werkzeug."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the plain-text password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name} ({self.email})>'


class Admin(db.Model):
    """
    Admin Model representing system administrators who oversee complaints,
    update status, provide resolution remarks, and manage users.
    """
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), default='System Administrator')
    email = db.Column(db.String(120), default='admin@cms.com')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Hashes and sets admin password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies admin password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'


class Complaint(db.Model):
    """
    Complaint Model storing submitted issues, auto-generated unique ID,
    category, priority level, resolution status, and admin remarks.
    """
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    complaint_number = db.Column(db.String(25), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Technical, Academic, Infrastructure, Service, Other
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='Medium') # Low, Medium, High
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, In Progress, Resolved, Rejected
    admin_remark = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Complaint {self.complaint_number} - Status: {self.status}>'
