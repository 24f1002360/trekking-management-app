from flask import Blueprint , render_template, session, redirect, url_for
user = Blueprint( 'user' , __name__ )

@user.route("/user/dashboard")
def dashboard():
    if session.get('role') != 'Trekker':
        return redirect(url_for('auth.login'))
    return render_template('user_dashboard.html')
    