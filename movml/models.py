from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(27), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    state = db.Column(db.String(100), nullable=True)
    friends = db.relationship("User", secondary="friends", backref='friend', lazy=True, primaryjoin="User.id==friends.c.user1", secondaryjoin="User.id==friends.c.user2")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.state}', '{self.password}')"

# from movml import db
# from movml.models import User, Friends
# db.create_all()
# user_1 = User(username="maciejx", email="terst@mail.com", password="pass", state="active")
# db.session.add(user_1)
# db.session.commit()


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.user1}', '{self.user2}', '{self.state}')"
