import unittest
from base import BaseTestCase
from app.models import Shelter

class TestShelterCase(BaseTestCase):

    def test_shelter_new_page(self):
        response = self.client.get('/new-shelter', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a shelter', response.data)

    def test_shelter_add_new(self):
        response = self.client.post('/new-shelter', data=dict(name='Greatshelter', address="321 Notreal st.", city="Nocity", state="Alabama", zipCode=54321, website="http://www.notreal.com", maximum_capacity=6, current_capacity=2), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<strong>Congrats</strong> You just created a new shelter named <u>Greatshelter</u>.", response.data)
        
    def test_shelter_add_new_error(self):
        response = self.client.post('/new-shelter', data=dict(name='Greatshelter'),follow_redirects=True)
        self.assertIn(b"This field is required.", response.data)

    def test_shelter_database(self):
        shelter = Shelter.query.filter_by(id=1).one()
        self.assertEqual(shelter.id, 1)
        self.assertEqual(shelter.name, 'Testshelter')
        self.assertEqual(shelter.address, '123 Fake st.')
        self.assertEqual(shelter.city, 'Fake')
        self.assertEqual(shelter.state, 'Florida')
        self.assertEqual(shelter.zipCode, '12345')
        self.assertEqual(shelter.website, 'http://test.com')
        self.assertEqual(shelter.maximum_capacity, 10)
        self.assertEqual(shelter.current_capacity, 5)

    def test_shelter_edit_page(self):
        response = self.client.get('/1/testshelter/edit/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit a shelter', response.data)

    def test_shelter_edit_post(self):
        response = self.client.post('/1/testshelter/edit/', data=dict(name="Testshelter", address="123 Fake st.", city="Fake", state="Florida", zipCode="12345", website="http://test.com", maximum_capacity=10, current_capacity=6), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>Update</strong>&nbsp; on <u>Testshelter</u>.', response.data)

    def test_shelter_delete_page(self):
        response = self.client.get('/1/testshelter/delete/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Are you sure you want to close down <mark>Testshelter</mark>?', response.data)

    def test_shelter_delete_post(self):
        response = self.client.post('/1/testshelter/delete/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>Successfully</strong> deleted shelter <u>Testshelter</u>.', response.data)

    

