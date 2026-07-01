from flask import Blueprint , render_template, session, redirect, url_for, request , flash
from models import db , Staff, Trekker, Trek, Booking
from datetime import datetime
admin= Blueprint( 'admin', __name__ )

@admin.route('/admin/dashboard')
def dashboard():
    if session.get('role' ) != 'Admin':
        return redirect(url_for('auth.login'))
    total_staff = Staff.query.count()
    total_trekkers =Trekker.query.count()
    total_treks= Trek.query.count()
    total_bookings = Booking.query.count()
    
    pending_staff = Staff.query.filter_by(status='pending').count()
    return render_template(
        'admin_dashboard.html',
        total_staff=total_staff,
        total_trekkers=total_trekkers,
        total_treks=total_treks,
        total_bookings=total_bookings,
        pending_staff=pending_staff
    )
    
@admin.route('/admin/manage-staff')
def manage_staff():
    if session.get('role') != 'Admin':
        return redirect(url_for('auth.login'))
    staff_members= Staff.query.all()
    return render_template('manage_staff.html', staff_members=staff_members)
@admin.route('/admin/approve/<int:staff_id>')
def approve_staff(staff_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('auth.login'))
    staff=Staff.query.get_or_404(staff_id)
    staff.status='approved'
    db.session.commit()
    return redirect(url_for('admin.manage_staff'))
@admin.route( '/admin/deactivate/<int:staff_id>')
def deactivate_staff(staff_id):
    if session.get('role')!='Admin':
        return redirect(url_for('auth.login'))
    staff= Staff.query.get_or_404(staff_id)
    staff.status='deactivated'
    db.session.commit()
    flash('staff deactivated successfully!', 'warning')
    return redirect(url_for('admin.manage_staff'))
@admin.route('/admin/activate/<int:staff_id>')
def activate_staff(staff_id):
    if session.get('role')!= 'Admin':
        return redirect(url_for('auth.login'))
    staff= Staff.query.get_or_404(staff_id)
    staff.status='approved'
    db.session.commit()
    flash('staff activated successfully!', 'success')
    return redirect(url_for('admin.manage_staff'))


@admin.route('/admin/manage-treks')
def manage_treks():
    if session.get('role') !='Admin':
        return redirect(url_for("auth.login"))
    treks = Trek.query.all()
    staff_members= Staff.query.filter_by(status="approved").all()
    return render_template('manage_treks.html', treks=treks, staff_members=staff_members )
@admin.route("/admin/add-trek", methods=['GET', 'POST'])
def add_trek():
    if session.get('role') != 'Admin':
        return redirect(url_for('auth.login'))
    if request.method=='GET':
        staff_members= Staff.query.filter_by(status='approved').all()
        return render_template('add_trek.html', staff_members=staff_members)
    name=request.form["name"]
    location =request.form['location']
    difficulty= request.form['difficulty']
    duration= int(request.form['duration'])
    available_slots= int(request.form['available_slots'])
    staff_id = int(request.form['staff_id'])
    start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d" ).date()
    end_date= datetime.strptime(request.form['end_date'], "%Y-%m-%d").date()
    existing= Trek.query.filter_by(name=name).first()
    if existing:
        flash('Trek already exists.', 'danger')
        return redirect(url_for('admin.add_trek'))
    trek = Trek(name=name, location=location, difficulty=difficulty, duration=duration, available_slots=available_slots, staff_id=staff_id, status='open', start_date=start_date, end_date=end_date )
    db.session.add(trek)
    db.session.commit()
    
    flash('Trek added successfully!', "success")
    return redirect(url_for('admin.manage_treks'))
@admin.route('/admin/edit-trek/<int:trek_id>', methods=['GET', 'POST'])
def edit_trek(trek_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('auth.login'))
    trek = Trek.query.get_or_404(trek_id)
    if request.method =='GET':
        staff_members = Staff.query.filter_by(status='approved').all()
        return render_template('edit_trek.html', trek=trek , staff_members=staff_members)
    trek.name = request.form['name']
    trek.location = request.form['location']
    trek.difficulty = request.form['difficulty']
    trek.duration = int(request.form['duration'])
    trek.available_slots = int(request.form['available_slots'])
    trek.staff_id = int(request.form['staff_id'])
    trek.start_date = datetime.strptime(request.form['start_date'],'%Y-%m-%d').date()
    trek.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
    trek.status = request.form['status']
    db.session.commit()
    flash('Trek updated successfully!' , 'success')
    return redirect(url_for('admin.manage_treks'))
@admin.route('/admin/delete-trek/<int:trek_id>')
def delete_trek(trek_id):
    if session.get('role')!= 'Admin':
        return redirect(url_for('auth.login'))
    trek = Trek.query.get_or_404(trek_id)
    if trek.bookings:
        flash('Cannot delete a trek that has bookings.', 'danger')
        return redirect(url_for('admin.manage_treks'))
    db.session.delete(trek)
    db.session.commit()
    flash('Trek deleted successfully!', 'success')
    return redirect(url_for('admin.manage_treks'))



@admin.route('/admin/manage-trekkers')
def manage_trekkers():
    if session.get('role') != 'Admin':
        return redirect(url_for('auth.login'))
    trekkers= Trekker.query.all()
    return render_template('manage_trekkers.html', trekkers=trekkers)
@admin.route('/admin/blacklist/<int:trekker_id>')
def blacklist_trekker(trekker_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('auth.login'))
    trekker= Trekker.query.get_or_404(trekker_id)
    trekker.is_blacklisted= True
    db.session.commit()
    flash('Trekker blacklisted successfully!', 'success')
    return redirect(url_for('admin.manage_trekkers'))
@admin.route('/admin/unblacklist/<int:trekker_id>')
def unblacklist_trekker(trekker_id):
    if session.get('role') != 'Admin':
        return redirect(url_for('auth.login'))
    trekker =Trekker.query.get_or_404(trekker_id)
    trekker.is_blacklisted = False
    db.session.commit()
    flash('Trekker resorted successfully!', 'success')
    return redirect(url_for('admin.manage_trekkers'))



@admin.route('/admin/bookings')
def view_bookings():
    if  session.get('role')!= 'Admin':
        return redirect(url_for('auth.login'))
    bookings = Booking.query.all()
    return render_template('view_bookings.html', bookings=bookings )
