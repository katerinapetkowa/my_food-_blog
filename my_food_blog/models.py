from flask_login import UserMixin
from . import db
from sqlalchemy.orm import relationship


user_favourite_meals = db.Table(
    "favourites",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("meal_id", db.Integer, db.ForeignKey("meals.id")),
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    favourites = db.relationship("Meal", secondary=user_favourite_meals)


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe = db.Column(db.Text, nullable=True)
    user_info = relationship('User', foreign_keys=[user_id],
                             primaryjoin='User.id == Meal.user_id')
    likes = db.relationship('User', secondary=user_favourite_meals)
