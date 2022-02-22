from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Meal
from flask_login import login_required, current_user
from . import cache

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=600)
def index():
    meals = Meal.query.all()
    return render_template('index.html', meals=meals)


@main.route('/profile')
@login_required
def profile():
    user_id = current_user.get_id()
    meals = Meal.query.filter_by(user_id=user_id).all()
    return render_template('profile.html', meals=meals)


@main.route('/add_meal')
@login_required
def add_meal():
    return render_template('add_meal.html')


@main.route('/add_meal', methods=['POST'])
@login_required
def add_meal_post():
    name = request.form.get('name')
    recipe = request.form.get('recipe')
    if current_user.is_authenticated:
        user_id = current_user.get_id()
    new_meal = Meal(name=name, recipe=recipe, user_id=user_id)
    print(new_meal)
    db.session.add(new_meal)
    db.session.commit()
    return redirect(url_for('main.profile'))


@main.route('/meal_details/<int:meal_id>')
def meal_details(meal_id):
    meal = Meal.query.filter_by(id=meal_id).first()
    return render_template('meal_details.html', meal=meal)


@main.route('/favourites')
@login_required
def favourites():
    return render_template('profile.html', meals=current_user.favourites)


@main.route('/add_to_favourites/<int:meal_id>')
@login_required
def add_to_favourites(meal_id):
    meal = Meal.query.filter_by(id=meal_id).first()
    current_user.favourites.append(meal)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('main.favourites'))


@main.route('/search')
def search():
    query = request.args.get('query')
    meals = []
    if query:
        meals = Meal.query.filter(Meal.name.like(query))
    return render_template('search.html', meals=meals)
