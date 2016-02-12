import unittest
import datetime
from base import BaseTestCase
from app.models import Adoptors, Shelter, Puppy, Profile, AdoptorsPuppies


class TestModelCase(BaseTestCase):

	def test_model_tablenames(self):
		# adoptor = Adoptors.query.all()
		assert Adoptors.__tablename__== 'adoptors'
		assert Shelter.__tablename__ =='shelter'
		assert Puppy.__tablename__=='puppy'
		assert Profile.__tablename__ == 'profile'
		assert AdoptorsPuppies.__tablename__=='adoptors_puppies'


	# def test_model_repr(self):
		