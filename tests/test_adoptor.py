import unittest
from base import BaseTestCase
from app.models import Adoptors


class TestAdoptorCase(BaseTestCase):
	 # Ensure that /adoptors response correctly
    def test_adoptors(self):
        response = self.client.get('/adoptors', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A list of potenial Adoptors', response.data)
        self.assertIn(b'Testname', response.data)

    # Ensure that the /adoptors page loads correctly
    def test_adoptors_page_loads(self):
        response = self.client.get('/adoptors',content_type='html/text')
        self.assertIn(b'A list of potenial Adoptors', response.data)
        self.assertIn(b'Testname', response.data)

      # Ensure that /new-shelterresponse is correct
    def test_adoptors_new_adoptor_page_loads(self):
        response = self.client.get('/new-adoptor', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Become an Adoptor', response.data)

    def test_adoptors_add_new(self):
        response = self.client.post('/new-adoptor', data=dict(name='Jefftest'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>Just created</strong> a new adoptor named <u>Jefftest</u>', response.data)


    def test_adoptors_from_index_add_new(self):
        response = self.client.post('/', data=dict(name='Jefftest1'), follow_redirects=True)
        self.assertIn(b'<strong>Just created</strong> a new adoptor named <u>Jefftest1</u>', response.data)

    def test_adoptors_from_index_add_new_test_error(self):
        response = self.client.post('/', data=dict(name=''), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_adoptors_delete_status(self):
        response = self.client.get('/adoptors/profile/1/delete/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Do you want to delete <mark>Testname</mark>?', response.data)

    def test_adoptors_delete_post(self):
        response = self.client.post('/adoptors/profile/1/delete/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>You just</strong> deleted <u>Testname</u>', response.data)
        

    def test_adoptors_edit_status(self):
        response = self.client.get('/adoptors/profile/1/edit/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit an Adoptor', response.data)

    def test_adoptors_edit_post(self):
        response = self.client.post('/adoptors/profile/1/edit/', data=dict(name='Editname'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>Successful</strong> edit of this adoptor who is now named <u>Editname</u>', response.data)
