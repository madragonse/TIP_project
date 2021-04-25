from flask import Blueprint, render_template, redirect
from flask.helpers import flash, url_for

from forms import LoginForm


login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():              
    form = LoginForm()          
    if form.validate_on_submit():
        #TODO featch from database
        flash("Zalogowałeś się.", 'info')
        return redirect(url_for('home.home'))
    return render_template('login.html', title='Zaloguj', form = form)