from flask import Blueprint, render_template

from forms import LoginForm


login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():              
    form = LoginForm()
    return render_template('login.html', title='Zaloguj', form = form)