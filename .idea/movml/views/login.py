from flask import Blueprint, render_template, redirect
from flask.helpers import flash, url_for
from flask_login import login_user

from forms import LoginForm
from movml import db, bcrypt
from movml.models import User, Friends



login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():              
    form = LoginForm()          
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Zalogowałeś się.", 'info')
            return redirect(url_for('home.home'))
        else:
            flash("Błędny login lub hasło.", 'info')
    return render_template('login.html', title='Zaloguj', form = form)