from flask import Blueprint , render_template, session, redirect , url_for, request, flash
from models import db, Staff, Trekker, Trek , Booking 
from werkzeug.security import generate_password_hash
staff = Blueprint( 'staff', __name__)

@staff.route('/staff/dashboard')
def dashboard():
    if session.get("role") != 'Staff':
        return redirect(url_for('auth.login'))
    staff_member = Staff.query.get(session['staff_id'])
    assigned_treks= Trek.query.filter_by(staff_id = staff_member.staff_id).all()
    total_assigned = len(assigned_treks)
    upcoming = Trek.query.filter_by( staff_id = staff_member.staff_id, status='open').count()
    completed = Trek.query.filter_by( staff_id = staff_member.staff_id, status='completed').count()
    return render_template('staff_dashboard.html', staff=staff_member, total_assigned= total_assigned, upcoming= upcoming, completed=completed)


@staff.route('/staff/assigned-treks')
def assigned_treks():
    if session.get('role')!= 'Staff':
        return redirect(url_for('auth.login'))
    treks = Trek.query.filter_by(staff_id = session['staff_id']).all()
    return render_template('assigned_treks.html', treks=treks)
@staff.route('/staff/trek/<int:trek_id>')
def trek_details(trek_id):
    if session.get('role')!= 'Staff':
        return redirect(url_for('auth.login'))
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != session['staff_id']:
        flash("Unauthorized Access", 'danger')
        return redirect(url_for('staff.assigned_treks'))
    bookings = Booking.query.filter_by( trek_id=trek_id ).order_by(Booking.booking_date).all()
    return render_template('trek_details.html', trek=trek, bookings=bookings)
@staff.route('/staff/update-status/<int:trek_id>', methods=['POST'])
def update_status(trek_id):
    if session.get('role')!= 'Staff':
        return redirect(url_for('auth.login'))
    trek=Trek.query.get_or_404(trek_id)
    if trek.staff_id != session['staff_id']:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('staff.assigned_treks'))
    trek.status = request.form['status']
    if trek.status == "completed":
        for booking in trek.bookings:
            if booking.status == "Booked":
                booking.status = "Completed"
    db.session.commit()
    flash("Trek status updated successfully!", 'success')
    return redirect(url_for('staff.trek_details', trek_id=trek_id))
@staff.route('/staff/update-slots/<int:trek_id>', methods=['POST'])
def update_slots(trek_id):
    if session.get('role') != 'Staff':
        return redirect(url_for('auth.login'))
    trek= Trek.query.get_or_404(trek_id)
    if trek.staff_id != session['staff_id']:
        flash('Unauthorized Access', 'danger')
        return redirect('staff.assigned_treks')
    slots= int(request.form['available_slots'])
    if slots <0 :
        flash('Slots cannot be negative.', 'danger')
        return redirect(url_for('staff.trek-details', trek_id=trek_id))
    trek.available_slots= slots 
    db.session.commit()
    flash('Available slots updated successfully!', 'success')
    return redirect(url_for('staff.trek_details', trek_id=trek_id))

    
    

@staff.route('/staff/profile')
def profile():
    if session.get('role') != 'Staff':
        return redirect(url_for('auth.login'))
    staff_member = Staff.query.get(session['staff_id'])
    return render_template('staff_profile.html', staff=staff_member)
@staff.route('/staff/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if session.get('role')!= 'Staff':
        return redirect(url_for('auth.login'))
    staff_member = Staff.query.get(session['staff_id'])
    if request.method =='GET':
        return render_template('edit_staff_profile.html', staff=staff_member)
    staff_member.name= request.form['name']
    staff_member.phone = request.form['phone']
    password = request.form['password']
    if password:
        staff_member.hash_password= generate_password_hash(password)
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('staff.profile'))