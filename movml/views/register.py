from flask import Blueprint, render_template, redirect
from flask.helpers import flash, url_for

from forms import RegistrationForm


register_bp = Blueprint('register', __name__, template_folder='templates')


@register_bp.route('/register', methods=['GET', 'POST'])
def register():    
    form = RegistrationForm()          
    if form.validate_on_submit():
        #TODO register to database
        flash("Brawo {}, stworzyłeś konto.".format(form.username.data), 'info')
        return redirect(url_for('home.home'))
    return render_template('register.html', title='Zarejestruj', form = form)
