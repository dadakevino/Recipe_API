"""Flask web app API - returns a list of value within
 a given radius of a UK postcode"""

import datetime

from flask import Flask, abort, request, jsonify
from flask_restful import Api, Resource, reqparse

from helper import import_recipes, import_recipes_id,\
    paginate_recipes, response_with_pagination
from app.config import app_config


application = Flask(__name__)
#config_name = os.getenv('APP_SETTINGS')
config_name = 'testing'
application.config.from_object(app_config[config_name])

api = Api(application)

@application.route('/recipe/<int:id>', methods=['GET'])
def get_recipe(id):
    """Return recipe in JSON format for a given recipe ID"""
    recipes = import_recipes_id(id)
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
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("title", type=str, location='json')
        self.reqparse.add_argument("calories_kcal", type=int, location='json')
        super(RecipeAPI, self).__init__()

    def put(self, id):
        """Updates a recipe for a given ID.
        Content type must be JSON."""
        recipes = import_recipes_id(id)
        if not recipes:
            abort(404)

        recipe = recipes[0]
        args = self.reqparse.parse_args()
        for key, value in args.items():
            if value is not None:
                recipe[key] = value

        dt_now = datetime.datetime.now()
        recipe['updated_at'] = dt_now.strftime('%d/%m/%Y %H:%M')

        return {'recipe': recipe}, 200

api.add_resource(RecipeAPI, '/recipez/<int:id>')
