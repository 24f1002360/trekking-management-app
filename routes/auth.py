from flask import Blueprint, render_template , request , redirect, flash , url_for , session
from werkzeug.security import generate_password_hash , check_password_hash
from models import db, Staff, Trekker , Admin
auth=Blueprint(
    'auth',
    __name__
)

@auth.route('/')
def home():
    return render_template('home.html')



@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    else :
        email=request.form[ 'email' ]
        password=request.form[ 'password' ]
        role= request.form[ 'role' ]

        if role == 'Admin':
            admin = Admin.query.filter_by(email=email ).first()
            if admin and check_password_hash(admin.hash_password, password):
                session[ 'admin_id' ]= admin.admin_id
                session[ 'role' ] = 'Admin'
                flash('Login Successful!', 'success')
                return   redirect( url_for( 'admin.dashboard') )
            else:
                flash('Invalid Email or Password.', 'danger')
                return redirect( url_for('auth.login'))

        if role == 'Staff':
            staff=Staff.query.filter_by(email = email).first()
            if staff and check_password_hash( staff.hash_password , password ):
                if staff.status != 'approved':
                    flash('Waiting for Admin Approval.', 'warning')
                    return redirect( url_for('auth.login') )
                session['staff_id']=staff.staff_id
                session['role'] = 'Staff'
                flash('Login Successful!','success')
                return redirect( url_for('staff.dashboard' ))
            else:
                flash('Invalid Email or Password.', 'danger')
                return redirect( url_for('auth.login'))

        if role == 'Trekker' :
            trekker=Trekker.query.filter_by(email =email).first()
            if trekker and  check_password_hash( trekker.hash_password, password ):
                if trekker.is_blacklisted :
                    flash('Your Account is Blacklisted.', 'danger')
                    return redirect( url_for('auth.login'))
                session['trekker_id'] = trekker.trekker_id
                session["role"]= 'Trekker'
                flash('Login Successful!','success')
                return redirect( url_for('user.dashboard'))
            else:
                flash("Invalid Email or Password.", 'danger')
                return redirect( url_for('auth.login'))
            
            
            

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    else :
        name =request.form['name']
        email=request.form['email']
        password =request.form['password']
        phone = request.form['phone']
        role = request.form['role'] 
        
        hash_password = generate_password_hash(password) 

        if role == 'Staff':
            existing_email=Staff.query.filter_by( email=email).first()
            existing_phone=Staff.query.filter_by( phone=phone).first()
            if existing_email or existing_phone:
                flash('Email or Phone already registred. ', 'danger')
                return redirect( url_for('auth.register'))
            new_staff= Staff(name=name, email=email, hash_password=hash_password, phone=phone, status='pending')
            db.session.add(new_staff)
            db.session.commit()
            flash('Registration Successful! Please wait for admin approval.', 'success')
            return redirect( url_for('auth.login' ) )
        
        if role == 'Trekker':
            existing_email=Trekker.query.filter_by( email=email).first()
            existing_phone=Trekker.query.filter_by( phone=phone).first()
            if existing_email or existing_phone:
                flash('Email or Phone already registred. ', 'danger')
                return redirect( url_for('auth.register'))
            new_trekker= Trekker( name=name , email=email, hash_password=hash_password, phone=phone, is_blacklisted=False)
            db.session.add( new_trekker )
            db.session.commit()
            flash('Registration Successful!', 'success')
            return redirect( url_for('auth.login' ) )
        
        
        
@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged Out Successfully.' , 'info')  
    return redirect(url_for('auth.home'))      
        
        