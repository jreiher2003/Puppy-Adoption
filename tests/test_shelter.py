import unittest
from base import BaseTestCase

from app.models import Shelter


class TestShelterCase(BaseTestCase):

	 # Ensure that /new-shelterresponse is correct
    def test_new_shelter_page(self):
        response = self.client.get('/new-shelter', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a shelter', response.data)

    def test_add_new_shelter(self):
        response = self.client.post('/new-shelter', data=dict(name='Greatshelter', address="321 Notreal st.", city="Nocity", state="Alabama", zipCode=54321, website="http://www.notreal.com", maximum_capacity=6, current_capacity=2), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<strong>Congrats</strong> You just created a new shelter named <u>Greatshelter</u>.", response.data)
        
    def test_add_new_shelter_error(self):
        response = self.client.post('/new-shelter', data=dict(name='Greatshelter'),follow_redirects=True)
        self.assertIn(b"This field is required.", response.data)

    

