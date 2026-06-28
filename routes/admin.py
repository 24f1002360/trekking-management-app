from flask import Blueprint , render_template, session, redirect, url_for

admin= Blueprint( 'admin', __name__ )

@admin.route('/admin/dashborad')
def dashboard():
    if session.get('role' ) != 'Admin':
        return redirect(url_for('auth.login'))
    return render_template('admin_dashboard.html')
