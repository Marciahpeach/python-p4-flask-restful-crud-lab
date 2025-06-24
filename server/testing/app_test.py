import json
import pytest

from server.app import app
from server.config import db
from server.models import Plant

class TestPlant:
    '''Flask application in app.py'''

    @pytest.fixture(autouse=True)
    def setup_method(self):
        '''Run before each test'''
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True

        with app.app_context():
            db.create_all()

            aloe = Plant(
                name="Aloe",
                image="./images/aloe.jpg",
                price=11.50,
                is_in_stock=True
            )

            db.session.add(aloe)
            db.session.commit()

        self.client = app.test_client()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = self.client.get('/plants/1')
        assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = self.client.get('/plants/1')
        data = json.loads(response.data.decode())

        assert isinstance(data, dict)
        assert data["id"] == 1
        assert data["name"] == "Aloe"

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        response = self.client.patch(
            '/plants/1',
            json={"is_in_stock": False}
        )
        data = json.loads(response.data.decode())

        assert isinstance(data, dict)
        assert data["id"] == 1
        assert data["is_in_stock"] is False

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''deletes a plant and returns 204 status at "/plants/<int:id>".'''
        with app.app_context():
            lo = Plant(
                name="Live Oak",
                image="https://example.com/oak.jpg",
                price=250.00,
                is_in_stock=False,
            )
            db.session.add(lo)
            db.session.commit()
            plant_id = lo.id

        response = self.client.delete(f'/plants/{plant_id}')
        assert response.status_code == 204
        assert response.data == b''
