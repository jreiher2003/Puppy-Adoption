import datetime
from flask.ext.testing import TestCase
from app import app, db
from app.models import Shelter, Puppy, Profile, Adoptors, AdoptorsPuppies


class BaseTestCase(TestCase):
    """A base test case."""
 
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Adoptors(name='Testname'))
        db.session.add(Adoptors(name='Billtest'))
        db.session.add(Shelter(name="Testshelter", address="123 Fake st.", city="Fake", state="Florida", zipCode="12345", website="http://test.com", maximum_capacity=10, current_capacity=5))
        db.session.add(Puppy(name="Testpup", shelter_id=1, gender="male", dateOfBirth=datetime.datetime.now(),picture="http://testpup.com",weight=1, show=True))
        db.session.add(Profile(puppy_id=1, breed="Testbreed",description="This is a test description", specialNeeds="Testblind"))
        
        db.session.add(Puppy(name="Billpup", shelter_id=1, gender="male", dateOfBirth=datetime.datetime.now(),picture="http://billpup.com",weight=2, show=True))
        db.session.add(Profile(puppy_id=2, breed="Testbreed",description="This is a test description1", specialNeeds="Testdeaf"))

        db.session.add(AdoptorsPuppies(adoptor_id=1, puppy_id=1))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()