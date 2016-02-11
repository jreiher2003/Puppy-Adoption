import unittest
import datetime
from base import BaseTestCase
from app.models import Shelter


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_index_page_loads(self):
        response = self.client.get('/')
        self.assertIn(b'Welcome to our puppy adoption web app!', response.data)
        self.assertIn(b'Testshelter', response.data)

    # Ensure that the shelter profile loads correctly
    def test_shelter_profile_page_loads(self):
        response = self.client.get('/1/testshelter/page/1')
        self.assertIn(b'Testshelter', response.data)
        self.assertIn(b'123 Fake st.', response.data)
        self.assertIn(b'Fake', response.data)
        self.assertIn(b'http://test.com', response.data)
        self.assertIn(b'Testpup', response.data)
        shelter = Shelter.query.filter_by(name='Testshelter').first()
        self.assertTrue(str(shelter) == '<name>: Testshelter')

    # Ensure that puppy-profile correctly
    def test_puppy_profile(self):
        response = self.client.get('/1/testshelter/profile/1', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_puppy_profile_page_loads(self):
        response = self.client.get('/1/testshelter/profile/1')
        self.assertIn(b'Testshelter', response.data)
        self.assertIn(b'Testpup', response.data)
        self.assertIn(b'1', response.data)
        self.assertIn(b'Testbreed', response.data)
        self.assertIn(b'Testblind', response.data)
        self.assertIn(b'This is a test description', response.data)

    # Ensure that Flask was set up correctly
    def test_adopt_puppy_page(self):
        response = self.client.get('/1/testshelter/profile/1/adopt/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_adopt_puppy_page_loads(self):
        response = self.client.get('/1/testshelter/profile/1/adopt/')
        self.assertIn(b'Who do you want to adopt <u>Testpup</u>?', response.data)


    # Ensure that test adpot page 2 set up correctly
    def test_adopt_2_puppy_page(self):
        response = self.client.get('/1/testshelter/profile/2/adopt/2/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Are you sure you want <mark>Billpup</mark> to be adopted by <mark>Billtest</mark>?', response.data)
    
     
      # Ensure that list-adoptions response is correct
    def test_list_adoptions(self):
        response = self.client.get('/list-adoptions', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'List of past adoptions', response.data)
        self.assertIn(b'Testname</span></mark>\thas adopted  <mark><span class="text-success">Testpup</span></mark> from <mark><span class="text-danger">Testshelter', response.data)

   

     

    


   


        
