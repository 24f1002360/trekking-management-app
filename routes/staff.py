from flask import Blueprint , render_template, session, redirect , url_for, request, flash
from models import db, Staff, Trekker, Trek , Booking 
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
    bookings= Booking.query.filter_by(trek_id=trek_id).all()
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
    db.session.commit()
    flash("Trek status updated successfully!", 'success')
    return redirect(url_for('staff.trek_details', trek_id=trek_id))

