from flask import Blueprint
import dash
import dash_core_components as dcc
import dash_html_components as html
from sqlalchemy import desc, func
from . import app, db
from .models import Meal, user_favourite_meals

dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dummy/')

dash_app.layout = html.Div(children=[
    html.H1(children='Top Meals'),
    dcc.Graph(
        id='top-meals-graph',
        figure={
            'data': [
                {'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                # {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

bp = Blueprint('dashboards', __name__, url_prefix='/dashboards')


@bp.route('/top_meals', methods=['GET', 'POST'])
def top_meals():
    top_meals = (
        db.session
        .query(Meal, func.count(user_favourite_meals.c.user_id).label('total'))
        .join(user_favourite_meals).group_by(Meal)
        .order_by(desc('total')).limit(5).all()
    )
    count = []
    names = []
    for m in top_meals:
        names.append(m[0].name)
        count.append(m[1])
    print(names)
    print(count)
    return dash_app.index()
