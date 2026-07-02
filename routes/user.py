from flask import Blueprint , render_template, session, redirect, url_for, request, flash 
from werkzeug.security import generate_password_hash
from models import db , Trekker, Trek , Booking
user = Blueprint( 'user' , __name__ )

@user.route("/user/dashboard")
def dashboard():
    if session.get('role') != 'Trekker':
        return redirect(url_for('auth.login'))
    trekker = Trekker.query.get(session['trekker_id'])
    total_bookings = Booking.query.filter_by(trekker_id = trekker.trekker_id, status='Booked').count()
    upcoming = Booking.query.join(Trek).filter(Booking.trekker_id == trekker.trekker_id,
                                               Booking.status == 'Booked',
                                               Trek.status == 'open').count()
    completed = Booking.query.join(Trek).filter(
        Booking.trekker_id == trekker.trekker_id, 
        Trek.status == 'completed'
    ).count()
    
    return render_template('user_dashboard.html',
                           trekker=trekker,
                           total_bookings=total_bookings,
                           upcoming=upcoming,
                           completed=completed)
    
    
    
@user.route('/user/browse-treks')
def browse_treks():
    if session.get('role')!='Trekker':
        return redirect(url_for('auth.login'))
    search = request.args.get('search', '')
    if search :
        treks = Trek.query.filter(Trek.status=='open', Trek.name.ilike(f'%{search}%')).all()
    else:
        treks=Trek.query.filter_by(status='open').all()
    return render_template('browse_treks.html', treks=treks, search=search )
@user.route('/user/book/<int:trek_id>')
def book_trek(trek_id):
    if session.get('role')!= 'Trekker':
        return redirect(url_for('auth.login'))
    trekker= Trekker.query.get(session['trekker_id'])   
    trek= Trek.query.get_or_404(trek_id)   
    if trek.status !='open':
        flash('Booking is closed.', 'danger')
        return redirect(url_for('user.browse_treks'))
    if trek.available_slots <=0:
        flash('No slots available.', 'danger')
        return redirect(url_for('user.browse_treks'))
    existing = Booking.query.filter_by(trekker_id=trekker.trekker_id, trek_id=trek.trek_id, status='Booked').first()
    if existing:
        flash('You have already booked this trek.', 'warning')
        return redirect(url_for('user.browse_treks'))
    booking = Booking(trekker_id= trekker.trekker_id, trek_id= trek_id, status='Booked')
    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()
    flash('Trek booked successfully!', 'success')
    return redirect(url_for('user.my_bookings'))
    


@user.route('/user/my-bookings')
def my_bookings():
    if session.get('role')!= 'Trekker':
        return redirect(url_for('auth.login'))  
    bookings = Booking.query.filter_by(trekker_id=session['trekker_id']).all()
    return render_template('my_bookings.html', bookings=bookings) 

@user.route('/user/cancel-booking/<int:booking_id>')
def cancel_bookings(booking_id):
    if session.get('role')!= 'Trekker':
        return redirect(url_for('auth.login'))
    booking= Booking.query.get_or_404(booking_id)
    if booking.trekker_id != session['trekker_id']:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('user.my_bookings'))
    if booking.status == 'Cancelled':
        flash('Booking already cancelled.', 'warning')
        return redirect(url_for('user.my_bookings'))
    booking.status='Cancelled'
    booking.trek.available_slots +=1 
    db.session.commit()
    flash('Booking cancelled successfully!', 'success')
    return redirect(url_for('user.my_bookings'))
    

@user.route('/user/profile')    
def profile():
    if session.get('role') != 'Trekker':
        return redirect(url_for('auth.login'))
    trekker = Trekker.query.get(session['trekker_id'])
    return render_template('profile.html', trekker=trekker)
@user.route('/user/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if session.get('role') != 'Trekker':
         return redirect(url_for('auth.login'))
    trekker= Trekker.query.get(session['trekker_id'])
    if request.method =='GET':
        return render_template('edit_profile.html', trekker=trekker)
    trekker.name= request.form['name']
    trekker.phone= request.form['phone']
    password = request.form['password']
    if password:
        trekker.hash_password= generate_password_hash(password)
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('user.profile'))
            