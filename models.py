from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class Admin(db.Model):
    __tablename__= 'admin'
    admin_id=db.Column( db.Integer, primary_key = True )
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(120), nullable=False, unique=True )
    hash_password=db.Column(db.String(250),nullable=False)
    
    
class Staff(db.Model):
    __tablename__= "staff"
    staff_id=db.Column(db.Integer, primary_key=True)
    name=db.Column( db.String(100), nullable=False)
    email=db.Column(db.String(120), nullable=False, unique=True )
    hash_password=db.Column(db.String(250), nullable=False)
    phone=db.Column(db.String(15), nullable=False, unique=True)
    status= db.Column( db.String(20), default='pending' )
    assigned_treks=db.relationship('Trek',  backref='assigned_staff', lazy=True )
    
    
class Trekker(db.Model):
    __tablename__= 'trekkers'    
    trekker_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(120), nullable=False, unique=True)
    hash_password=db.Column(db.String(250), nullable=False)
    phone= db.Column( db.String(15), nullable=False, unique=True)
    is_blacklisted= db.Column(db.Boolean, default=False) 
    bookings=db.relationship('Booking', backref='trekker', lazy=True)  
    

class Trek(db.Model):
    __tablename__='treks'
    trek_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(150), nullable=False , unique=True)
    location=db.Column(db.String(150), nullable=False )
    difficulty = db.Column(db.String(20), nullable=False)   
    duration=db.Column(db.Integer, nullable=False )
    available_slots=db.Column(db.Integer, nullable=False)
    staff_id=db.Column(db.Integer, db.ForeignKey( 'staff.staff_id'))
    status = db.Column(db.String(20), default="pending")
    start_date=db.Column(db.Date, nullable=False)
    end_date=db.Column( db.Date, nullable=False)
    bookings=db.relationship('Booking', backref='trek', lazy=True)
    
    
class Booking(db.Model):
    __tablename__="bookings" 
    booking_id=db.Column(db.Integer, primary_key=True )
    trekker_id= db.Column(db.Integer, db.ForeignKey( 'trekkers.trekker_id' ))   
    trek_id=db.Column(db.Integer, db.ForeignKey( 'treks.trek_id') )
    booking_date=db.Column(db.DateTime, default=datetime.utcnow)
    status= db.Column(db.String(20), default='Booked' )
    