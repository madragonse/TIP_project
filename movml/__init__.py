from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '76ad25217b1d9a0ffb4f44f33223ea5a'

    from movml.views.home import home_bp
    from movml.views.login import login_bp
    from movml.views.register import register_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)

    return app