import unittest
import datetime
from base import BaseTestCase


class TestPuppyCase(BaseTestCase):

# Ensure that /new-puppy response is correct
    def test_new_puppy_page(self):
        response = self.client.get('/new-puppy', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Check a puppy in to a shelter', response.data)

    def test_add_new_puppy(self):
        response = self.client.post('/new-puppy', data=dict(name='Newpup', gender='male', picture="https://pixabay.com", shelter_id=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"<strong>Successfully</strong> Added Newpup to Testshelter", response.data)



        # , shelter_id=1,gender="male", picture="https://pixaby.com"
        # , breed='Testbreed', specialNeeds="None", description="Test puppy description", puppy_id=2

    def test_add_new_puppy_test_error(self):
        response = self.client.post('/new-puppy', data=dict(name=''), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)
