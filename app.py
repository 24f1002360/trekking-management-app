from flask import Flask 
from models import db 
from routes.auth import auth 
from routes.admin import admin
from routes.staff import staff
from routes.user import user

app =  Flask( __name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SECRET_KEY'] = 'trekking-secret-key'

db.init_app(app)
app.register_blueprint(auth )
app.register_blueprint( admin)
app.register_blueprint( staff )
app.register_blueprint( user)
if __name__ =='__main__':
    app.run(debug=True)