from flask import Blueprint , render_template, session, redirect , url_for
staff = Blueprint( 'staff', __name__)

@staff.route('/staff/dashboard')
def dashboard():
    if session.get("role") != 'Staff':
        return redirect(url_for('auth.login'))
    return render_template('staff_dashboard.html')
