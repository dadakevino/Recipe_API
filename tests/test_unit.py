import json
from unittest.mock import patch

from pytest_mock import mocker
import pytest
from flask import url_for
import pandas as pd

from app.webapp import application

@pytest.fixture
def app():
    return application

@pytest.fixture(scope='session')
def client():
    application.config['TESTING'] = True
    return application.test_client()

class TestApp:
    recipes = [{'id': 1,
               'data': 'test',
               'cuisine': 'british'}]
    valid_id = 1


    def test_get_recipe(self, client, mocker):
        """Tests get api can get recipe by ID"""
        patch = mocker.patch('helper.import_recipes_by_id',
                             return_value=self.recipes)
        id = self.recipes[0]['id']

        with application.test_request_context():
            res = client.get(url_for('get_recipe', id=id))
            result = json.loads(res.get_data())

            patch.assert_called_with(id)
            assert res.status_code == 200
            assert 'test' in result


    def test_get_recipe_by_cuisine(self, client, mocker):
        """Tests get recipe by cuisine api returns correct status,
        paginated data, and links"""
        recipe_df = pd.DataFrame(self.recipes)
        patch = mocker.patch('helper.import_recipes',
                             return_value=recipe_df)
        cuisine = self.recipes[0]['cuisine']

        with application.test_request_context():
            res = client.get(url_for('get_recipe_by_cuisine',
                                     cuisine=cuisine),
                             query_string='page=1')

            result = json.loads(res.data)
            patch.assert_called_with(None)
            assert res.status_code == 200
            assert 1 == result['data'][0]['id']

            assert 'page=1' in result['links']['first']
            assert 'page=2' in result['links']['next']


    def test_put(self, client, mocker):
        """Tests updating recipe returns correct fields"""
        patch = mocker.patch('helper.import_recipes_by_id',
                             return_value=self.recipes)
        test_data = {'data': 'changed'}
        id = self.recipes[0]['id']

        with application.test_request_context():
            res = client.put('/recipe/1',
                             data=test_data,
                             content_type='application/json')
            result = json.loads(res.data)

            patch.assert_called_with(id)
            assert res.status_code == 200
            assert result['recipe']['data'] == 'changed'

