from flask_wtf import Form 
from wtforms import TextField, RadioField, BooleanField, TextAreaField, SelectField, IntegerField, SubmitField, SelectMultipleField, StringField
from wtforms.validators import DataRequired, Length, URL, NumberRange, Regexp, Email
from wtforms.fields.html5 import EmailField
import us
import re
from app import db
from app.models import Shelter


class CreateAdoptor(Form):
	name = TextField('Name', validators=[DataRequired()])
	email = EmailField('Email address', validators=[DataRequired(), Email()])
	submit = SubmitField('Create')


class CreateShelter(Form):
	name = TextField('Name', validators=[DataRequired()])
	address = TextField('Address', validators=[DataRequired(),Length(max=128,message=(u'Too Long of an Address'))])
	city = TextField('City', validators=[DataRequired(),Length(max=40,message=(u'Try a shorter City name'))])
	state = SelectField('State', choices = [(i.name,i.name) for i in us.states.STATES])
	zipCode = StringField('Zip', validators=[Regexp('^[0-9]{5}(?:-[0-9]{4})?$', message="Not a valid zip code")])
	website = TextField('Website', validators=[DataRequired(), URL(message="Make sure to include HTTP://")])
	maximum_capacity = IntegerField('Max Capacity', validators=[DataRequired(), NumberRange(min=5, max=100)])
	current_capacity = IntegerField('Current Capacity', validators=[NumberRange(min=0, max=100)])
	submit = SubmitField('Create')


class CreatePuppy(Form):
	shelter = SelectField('Shelter', coerce=int)
	name = TextField('Name', validators=[DataRequired()])
	gender = RadioField('Gender', choices=[('female', 'Female'), ('male', 'Male')])
	picture = TextField('Photo-Url', validators=[DataRequired(), URL(message="Make sure to include HTTP://")])
	weight = IntegerField('Weight', validators=[NumberRange(min=1, max=75)])
	submit = SubmitField('Create')


class CreateProfile(Form):

	specialNeeds = SelectField('Special Needs', choices=[('None','None'),('3-legged', '3-legged'), ('Blind', 'Blind'),('Deaf', 'Deaf')])
	description = TextAreaField('Description', validators=[Length(max=500)])
	breed = SelectField('Breed', choices=[('None','None'),('Bulldog','Bulldog'),('Boston Terrier','Boston Terrier'),('Chihuahua', 'Chihuahua'),('German Shepherd', 'German Shepherd'),("Greyhound","Greyhound"),("Labrador Retriever","Labrador Retriever"),("Maltese","Maltese"),("Schnauzer","Schnauzer"),("Pug","Pug"),("Saint Bernard","Saint Bernard"),("Shih-Tzu","Shih-Tzu"),("Siberian Husky","Siberian Husky"),("Whippet","Whippet")])



