"""Unit test module for stores web app"""

import json

import pytest
from flask import url_for

from app.webapp import application


@pytest.fixture
def app():
    return application

@pytest.fixture(scope='session')
def client():
    application.config['TESTING'] = True
    return application.test_client()

class TestApp:
    valid_id = 1
    invalid_id = 99
    valid_cuisine = 'british'
    invalid_cuisine = ''


    def test_get_recipe(self, client):
        """Tests API can get recipe by ID"""
        with application.test_request_context():
            res = client.get(url_for('get_recipe', id=self.valid_id))
            result = json.loads(res.get_data())
            assert res.status_code == 200
            assert 'Sweet Chilli and Lime Beef' in result['title']

    def test_get_recipe_failure(self, client):
        """Tests API can return correct error status with invalid ID"""
        with application.test_request_context():
            res = client.get(url_for('get_recipe', id=self.invalid_id))
            assert res.status_code == 404

    def test_get_recipe_by_cuisine(self, client):
        """Tests get recipe by cuisine api returns correct status and json file
        for valid cuisine"""
        with application.test_request_context():
            res = client.get(url_for('get_recipe_by_cuisine',
                                     cuisine=self.valid_cuisine))
            result = json.loads(res.data)
            assert res.status_code == 200
            assert 3 == result['data'][0]['id']

    def test_get_recipe_by_cuisine_failure(self, client):
        """Tests get recipe by cuisine api returns correct status and json file
         for invalid cuisine"""
        with application.test_request_context():
            res = client.get(url_for('get_recipe_by_cuisine',
                                     cuisine=self.invalid_cuisine))
            assert res.status_code == 404

class TestRecipeAPI:

    def test_put(self, client):
        """Tests updating recipe returns correct fields"""
        test_data = {'title': 'changed'}
        with application.test_request_context():
            res = client.put('/recipez/1',
                             data=test_data,
                             content_type='application/json')
            result = json.loads(res.data)
            assert res.status_code == 200
            assert result['recipe']['title'] == 'changed'