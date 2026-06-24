from flask import Flask 
from models import db 
app =  Flask( __name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SECRET_KEY'] = 'trekking-secret-key'

db.init_app(app)

if __name__ =='__main__':
    app.run(debug=True)