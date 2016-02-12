import unittest
import datetime
from base import BaseTestCase

from app.models import Puppy


class TestPuppyCase(BaseTestCase):
# Ensure that /new-puppy response is correct
    def test_puppy_page(self):
        response = self.client.get('/new-puppy', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Check a puppy in to a shelter', response.data)

    def test_puppy_database(self):
        puppy = Puppy.query.filter_by(id=1).one()
        self.assertEqual(puppy.id, 1)
        self.assertEqual(puppy.name, 'Testpup')
        self.assertEqual(puppy.gender, 'male')
        self.assertEqual(puppy.picture, 'http://testpup.com')
        self.assertEqual(puppy.weight, 1)
        self.assertEqual(puppy.show, True)
        self.assertEqual(puppy.shelter_id, 1)
        self.assertEqual(puppy.shelter.name, 'Testshelter')
        self.assertEqual(puppy.profile.breed, 'Testbreed')
        self.assertEqual(puppy.profile.description, "This is a test description")
        self.assertEqual(puppy.profile.specialNeeds, "Testblind")
        
    def test_puppy_add_new(self):
        response = self.client.post('/new-puppy', data=dict(name='Newpup', breed=None, specialNeeds=None, gender='male',picture="https://pixabay.com", shelter=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>Successfully</strong> Added <u>Newpup</u> to Testshelter', response.data)
        
    def test_puppy_add_new_test_error(self):
        response = self.client.post('/new-puppy', data=dict(name=''), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_puppy_edit_page(self):
        response = self.client.post('/1/testshelter/profile/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit a puppy', response.data)

    def test_puppy_edit_post(self):
        response = self.client.post('/1/testshelter/profile/1/edit/', data=dict(name='Newpupedit', breed=None, specialNeeds=None, gender='male',picture="https://pixabay.com", shelter=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>Newpupedit</strong> was successfully edited!', response.data)

    def test_puppy_delete_page(self):
        response = self.client.get('/1/testshelter/profile/1/delete/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Do you want to delete <mark>Testpup</mark>?', response.data)

    def test_puppy_delete_post(self):
        response = self.client.post('/1/testshelter/profile/1/delete/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>Testpup</strong>&nbsp;was just put to sleep!', response.data)
