from flask import url_for
from pathlib import Path

import pandas as pd


def import_recipes():
    """Imports recipe CSV data to df"""
    filename = Path.cwd() / 'recipe-data.csv'
    return pd.read_csv(filename, index_col=None)

def import_recipes_id(id):
    """Imports recipe CSV data to df and returns
   a recipe list' for a given id"""
    recipes = import_recipes()
    this_recipe = recipes.loc[recipes['id'] == id]
    return this_recipe.to_dict('records')


def paginate_recipes(page, recipes_list, cuisine):
    """Paginates a list of recipes for a given page
    Items per page defined in config"""
    per_page = 2

    pagination = {}
    pagination['recipes'] = recipes_list[(page - 1) * per_page: page * per_page]

    if page != 1:
        pagination['previous_page'] = paginate_link(page - 1, cuisine)
    else:
        pagination['previous_page'] = None
    last_page = round(len(recipes_list)/per_page)
    if page != last_page:
        pagination['next_page'] = paginate_link(page + 1, cuisine)
    else:
        pagination['next_page'] = None
    pagination['first_page'] = paginate_link(1, cuisine)
    pagination['last_page'] = paginate_link(last_page, cuisine)

    return pagination


def response_with_pagination(pagination):
    """Make a http response for get requests."""
    output = {
        "meta": {"total_pages": len(pagination['recipes'])},
        "data": pagination['recipes'],
        "links": {"first": pagination['first_page'],
                  "prev": pagination['previous_page'],
                  "next": pagination['next_page'],
                  "last": pagination['last_page']}
    }
    return output


def paginate_link(page, cuisine):
    """Returns link for get_recipe_by_cuisine for
    a given page"""
    return url_for('get_recipe_by_cuisine',
                   cuisine=cuisine,
                   page=page,
                   _external=True)
