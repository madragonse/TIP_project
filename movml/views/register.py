from flask import Blueprint, render_template, redirect
from flask.helpers import flash, url_for
from wtforms.validators import Email

from forms import RegistrationForm
from movml import bcrypt, db
from movml.models import User, Friends

register_bp = Blueprint('register', __name__, template_folder='templates')


@register_bp.route('/register', methods=['GET', 'POST'])
def register():    
    form = RegistrationForm()          
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, state="active")
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            flash("Użytkownik o nazwie {} juz istnieje!".format(form.username.data), 'info')
            return render_template('register.html', title='Zarejestruj', form = form)
        flash("Brawo {}, stworzyłeś konto.".format(form.username.data), 'info')
        return redirect(url_for('home.home'))
    return render_template('register.html', title='Zarejestruj', form = form)
