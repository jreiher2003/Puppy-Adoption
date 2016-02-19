from random import randint # pragma: no cover
import datetime # pragma: no cover
import random # pragma: no cover
from app import app, db, mail # pragma: no cover
from flask_mail import Message # pragma: no cover
from twilio.rest import TwilioRestClient # pragma: no cover
from app.models import Shelter, Puppy, Profile # pragma: no cover


puppy_images = ["https://pixabay.com/static/uploads/photo/2015/11/17/13/13/bulldog-1047518_960_720.jpg", "https://pixabay.com/static/uploads/photo/2015/03/26/09/54/pug-690566__180.jpg","https://pixabay.com/static/uploads/photo/2014/03/05/19/23/dog-280332__180.jpg","https://pixabay.com/static/uploads/photo/2015/02/05/12/09/chihuahua-624924__180.jpg","https://pixabay.com/static/uploads/photo/2016/01/05/17/57/dog-1123026__180.jpg","https://pixabay.com/static/uploads/photo/2014/03/14/20/07/painting-287403__180.jpg","https://pixabay.com/static/uploads/photo/2016/01/05/17/51/dog-1123016__180.jpg","https://pixabay.com/static/uploads/photo/2014/07/05/08/50/puppy-384647__180.jpg","https://pixabay.com/static/uploads/photo/2015/12/23/14/29/puppies-1105730__180.jpg","https://pixabay.com/static/uploads/photo/2015/11/17/12/42/puppy-1047454__180.jpg"] # pragma: no cover


breed = ["Bulldog", "Collie", "Boston Terrier", "Chihuahua", "German Shepherd", "Greyhound", "Labrador Retriever", \
		"Maltese", "Schnauzer", "Pug", "Saint Bernard", "Shih-Tzu", "Siberian Husky", "Whippet"] # pragma: no cover

puppy_adj = ["active", 'good', "affectionate", "alert", "athletic", "brave", "bright-eyed", "crafty", "cuddly", \
 			"cute", "energetic", "fluffy", "frisky", "gentle", "goofy", "happy", "huggable", "mischievous", "potty-trained", "zippy", "wonderful", "well- trained", "wagging", "unique", "trusty", "tough", "smart"] # pragma: no cover

puppy_verb = ["adore", "beg", "care for", "cuddle", "defend", "dig", "do tricks", "greet", "heel", "hunt", "kiss", "love", "obey", "pamper", "perform tricks", "roll", "roll over", "run", "run and play", "shake", "sit", "snuggle"] # pragma: no cover


def descriptions():
	vowels = ('a','e','i','o','u','A','E','I','O','U')
	x = random.choice(puppy_adj)
	y = random.choice(breed)
	v = random.choice(puppy_verb)
	if x.startswith(vowels):
		z = " is an " + x
		return "This " + z + ' dog that will ' + v + " you and your family."
	else:
		z = " is a " + x
		return "This " + z + ' dog that will ' + v + " you and your family." 

def create_random_age():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def create_random_weight():
	return random.uniform(1.0, 75.0)

# Query the current occupancy of a specific shelter. 
def get_shelter_occupancy(shel_id):
	# return Shelter.query.filter(db.and_(Puppy.shelter_id==Shelter.id, Shelter.id == shel_id)).count()
	return db.session.query(Puppy, Shelter).join(Shelter).filter(Shelter.id == shel_id).count()

# Query the capacity for a shelter by it's ID.
def get_shelter_capacity(shel_id):
	return db.session.query(Shelter.maximum_capacity).filter(Shelter.id == shel_id).one()[0]

# A Query that determines which Shelter to place a puppy in.
def add_puppy_to_shelter():
	arr = [1,2,3,4,5]
	while len(arr) > 0:
		shelter_id = random.choice(arr)
		if (get_shelter_occupancy(shelter_id) < get_shelter_capacity(shelter_id)):
			return shelter_id
		else:
			arr.remove(shelter_id)
			
def counting_shows():
	""" returns a number. counts all show = True from Puppy and is == current_capacity"""
	update_capacity = db.session.query(Shelter).all()
	for shel in update_capacity:
		shel.current_capacity = db.session.query(Puppy, Shelter).join(Shelter).filter(db.and_(Shelter.id == shel.id, Puppy.show==True)).count()
		db.session.add(shel)
		db.session.commit()
	
def overflow(shelter_id):
	""" checks to see if current_capacity is less than maximum_capacity """
	shelter = Shelter.query.filter(Shelter.id == shelter_id).one()
	if shelter.current_capacity < shelter.maximum_capacity:
		return True
	else:
		return False

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def twilio_cred():
	client = TwilioRestClient(
		app.config['ACCOUNT_SID'], 
		app.config['AUTH_TOKEN']
		)
	return client