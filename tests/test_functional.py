import unittest 
import datetime

from base import BaseTestCase 
from app.models import Shelter, Puppy, Profile, Adoptors


class TestFunctionalCase(BaseTestCase):
    # Ensure that the login page loads correctly
    def test_index_page_loads(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to our puppy adoption web app!', response.data)
        self.assertIn(b'Testshelter', response.data)

    # Ensure that the shelter profile loads correctly
    def test_index_shelter_profile_page_loads(self):
        response = self.client.get('/1/testshelter/page/1', content_type='html/text')
        self.assertIn(b'Testshelter', response.data)
        self.assertIn(b'123 Fake st.', response.data)
        self.assertIn(b'Fake', response.data)
        self.assertIn(b'http://test.com', response.data)
        self.assertIn(b'Testpup', response.data)
        self.assertEqual(response.status_code, 200)
        shelter = Shelter.query.filter_by(name='Testshelter').first()
        self.assertTrue(str(shelter) == '<name>: Testshelter')
        

    # Ensure that the login page loads correctly
    def test_index_puppy_profile_page_loads(self):
        response = self.client.get('/1/testshelter/profile/1')
        self.assertIn(b'Testshelter', response.data)
        self.assertIn(b'Testpup', response.data)
        self.assertIn(b'1', response.data)
        self.assertIn(b'Testbreed', response.data)
        self.assertIn(b'Testblind', response.data)
        self.assertIn(b'This is a test description', response.data)
        puppy = Puppy.query.filter_by(name='Testpup').first()
        self.assertTrue(str(puppy) == '<name>: Testpup')
        profile = Profile.query.filter_by(id=puppy.id).first()
        self.assertTrue(str(profile) == '<specialNeeds>: Testblind')

    # Ensure that Flask was set up correctly
    def test_index_adopt_puppy_page(self):
        response = self.client.get('/1/testshelter/profile/2/adopt/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Who do you want to adopt <u>Billpup</u>?', response.data)


    def test_index_adopt_puppy_post(self):
        response = self.client.post('/1/testshelter/profile/2/adopt/', data=dict(pupadopt=2))
        self.assertEqual(response.status_code, 302)
        response1 = self.client.get('/1/testshelter/profile/2/adopt/2/', content_type='html/text')
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b'Are you sure you want <mark>Billpup</mark> to be adopted by <mark>Billtest</mark>?', response1.data)


    def test_index_adopt_2_puppy_post(self):
        response = self.client.post('/1/testshelter/profile/2/adopt/2/', data=dict(puppyname='2', adoptorname='2'))
        self.assertEqual(response.status_code, 302)
        response1 = self.client.get('/list-adoptions', content_type='html/text')
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b'<strong>Successful</strong> adoption', response1.data)
        self.assertIn(b'List of past adoptions', response1.data)
        self.assertIn(b'Billtest</span></mark>\thas adopted  <mark><span class="text-success">Billpup</span></mark> from <mark><span class="text-danger">Testshelter', response1.data)
        self.assertIn(b'Testname</span></mark>\thas adopted  <mark><span class="text-success">Testpup</span></mark> from <mark><span class="text-danger">Testshelter', response1.data)



   

     

    


   


        
