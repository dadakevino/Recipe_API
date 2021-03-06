"""Flask web app API for recipes
Reads recipe data from a CSV, allows getting recipes
and updating recipe fields"""

import datetime

from flask import Flask, abort, request, jsonify
from flask_restful import Api, Resource, reqparse

from helper import import_recipes, import_recipes_by_id,\
    paginate_recipes, response_with_pagination
from app.config import app_config


application = Flask(__name__)
config_name = 'testing'
application.config.from_object(app_config[config_name])

api = Api(application)

@application.route('/recipe/<int:id>', methods=['GET'])
def get_recipe(id):
    """Return recipe in JSON format for a given recipe ID"""
    recipes = import_recipes_by_id(id)
    if not recipes:
        abort(404)

    return jsonify(recipes[0])

@application.route('/recipes/<cuisine>', methods=['GET'])
def get_recipe_by_cuisine(cuisine):
    """Returns a paginated list of recipes for
    a given cuisine, with 10 recipes per page
    Must include first, last, previous, next"""
    recipes = import_recipes()
    cuisine_recipes = recipes.loc[recipes['recipe_cuisine'] == cuisine,
                                  ['id', 'title', 'marketing_description']]
    recipes = cuisine_recipes.to_dict('records')
    if not recipes:
        abort(404)

    page = request.args.get('page', type=int, default=1)
    pagination = paginate_recipes(page, recipes, cuisine)
    response = response_with_pagination(pagination)

    return jsonify(response)


class RecipeAPI(Resource):

    def __init__(self):
        int_names = ['id', 'calories_kcal', 'protein_grams', 'fat_grams',
                     'carb_grams', 'preparation_time_minutes', 'shelf_life_days',
                     'gousto_reference']
        str_names = ['title', 'created_at', 'updated_at', 'slug', 'short_title',
                     'marketing_description', 'protein_grams', 'bulletpoint1',
                     'bulletpoint2', 'bulletpoint3', 'season', 'protein_source',
                     'equipment_needed', 'origin_country', 'recipe_cuisine',
                     'in_your_box']
        self.reqparse = reqparse.RequestParser()
        [self.reqparse.add_argument(i, type=int, location='json') for i in int_names]
        [self.reqparse.add_argument(i, type=str, location='json') for i in str_names]
        super(RecipeAPI, self).__init__()

    def put(self, id):
        """Updates a recipe for a given ID.
        Content type must be JSON."""
        recipes = import_recipes_by_id(id)
        if not recipes:
            abort(404)

        recipe = recipes[0]
        args = self.reqparse.parse_args()
        print(args)
        for key, value in args.items():
            if value is not None:
                recipe[key] = value

        dt_now = datetime.datetime.now()
        recipe['updated_at'] = dt_now.strftime('%d/%m/%Y %H:%M')

        return {'recipe': recipe}, 200

api.add_resource(RecipeAPI, '/recipe/<int:id>')
