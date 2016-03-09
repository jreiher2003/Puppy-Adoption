import unittest
import datetime
from base import BaseTestCase
from app import app,db
from app.models import Adoptors, Shelter, Puppy, Profile, AdoptorsPuppies


class TestModelCase(BaseTestCase):

    def test_adoptor_db(self):
        self.assertTrue(
            db.session.query(Adoptors).filter(Adoptors.name=='Testname').first()
            is not None)

    def test_model_update(self):
        """Model modification should modify model"""
        model = db.session.query(Adoptors).filter(Adoptors.name=='Testname').first()
        model.name ='New name'
        db.session.add(model)
        db.session.commit()
        self.assertTrue(
            db.session.query(Adoptors).filter(Adoptors.name=='New name').first()
            is not None)

    def test_model_tablenames(self):
        assert Adoptors.__tablename__== 'adoptors'
        assert Shelter.__tablename__ =='shelter'
        assert Puppy.__tablename__=='puppy'
        assert Profile.__tablename__ == 'profile'
        assert AdoptorsPuppies.__tablename__=='adoptors_puppies'


        