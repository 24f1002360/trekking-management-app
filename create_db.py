from app import app
from models import db
from models import Admin 

with app.app_context():
    db.create_all()
    existing_admin=Admin.query.filter_by( email="admin@trek.com").first()
    if not existing_admin:
        admin=Admin(name='Admin', email='admin@trek.com', hash_password='admin8810')
        
        db.session.add(admin)
        db.session.commit()
        print('Admin Created ')
    print('Database Created' )    