from random import randint # pragma: no cover
import logging
import datetime # pragma: no cover
import random # pragma: no cover
import us # pragma: no cover

from app import app, db, mail # pragma: no cover

 
from flask import render_template, url_for, flash, redirect, request # pragma: no cover
from flask_mail import Message # pragma: no cover

from forms import CreatePuppy, CreateShelter, CreateAdoptor, CreateProfile # pragma: no cover
from app.models import Shelter, Puppy, Profile, Adoptors, AdoptorsPuppies # pragma: no cover
from app.utils import * # pragma: no cover




@app.route('/', methods=["GET", "POST"]) # pragma: no cover
def index():
	SHELTERS = Shelter.query.all()
	""" front page of site that lists all shelters"""
	shelter = Shelter.query.order_by(Shelter.current_capacity.desc()).all()
	error = None
	form = CreateAdoptor()
	if form.validate_on_submit():
		newadoptor = Adoptors(name=form.name.data,email=form.email.data)
		db.session.add(newadoptor)
		db.session.commit()
		logging.debug('Just created %s-%s', newadoptor.name,newadoptor.email)
		flash('<strong>Just created</strong> a new adoptor named <u>%s</u>.<br>\
			Go Checkout the shelter pages to adopt a puppy!' % newadoptor.name, 'info')
		return redirect(url_for('adoptor_list'))
	return render_template('index.html', 
							shelter=shelter, 
							SHELTERS=SHELTERS, 
							form=form, 
							error=error)


##  CRUD for Shelter class  ##
@app.route('/<int:shelter_id>/<path:shelter_name>/page/<int:page>') # pragma: no cover
def shelter_profile(shelter_id,shelter_name, page=1):
	SHELTERS = Shelter.query.all()
	PUPPY = Puppy.query.filter(Puppy.shelter_id==shelter_id).all()
	shelter_profile = Shelter.query.filter_by(id=shelter_id).one()
	puppy = Puppy.query.filter(db.and_(Puppy.shelter_id==shelter_id, Puppy.show==True)).paginate(page,4,False)
	return render_template('shelter_profile.html', 
							shelter_id=shelter_id,
							shelter_name=shelter_name,
							shelter_profile=shelter_profile,
						    puppy=puppy,
						    SHELTERS=SHELTERS,
						    PUPPY=PUPPY)


@app.route('/new-shelter', methods=['GET', 'POST']) # pragma: no cover
def new_shelter():
	SHELTERS = Shelter.query.all()
	error = None
	form = CreateShelter()
	if form.validate_on_submit():
		newshelter = Shelter(name=form.name.data, 
							 address=form.address.data,
							 city=form.city.data,
							 state=form.state.data,
							 zipCode=form.zipCode.data,
							 website=form.website.data,
							 maximum_capacity=form.maximum_capacity.data,
							 current_capacity=form.current_capacity.data
							 )
		db.session.add(newshelter)
		db.session.commit()
		flash("<strong>Congrats</strong> You just created a new shelter named <u>%s</u>." % newshelter.name, 'warning')
		return redirect(url_for('index'))
	return render_template('create_shelter.html', 
							form=form, 
							error=error,
							SHELTERS=SHELTERS)


@app.route('/<int:shelter_id>/<path:shelter_name>/edit/', methods=['GET','POST']) # pragma: no cover
def edit_shelter(shelter_id,shelter_name):
	SHELTERS = Shelter.query.all()
	editshelter = Shelter.query.filter_by(id=shelter_id).one()
	form = CreateShelter(obj=editshelter)
	if form.validate_on_submit():
		editshelter.name = form.name.data
		editshelter.address = form.address.data
		editshelter.city = form.city.data
		editshelter.state = form.state.data
		editshelter.zipCode = form.zipCode.data
		editshelter.website = form.website.data
		editshelter.maximum_capacity = form.maximum_capacity.data
		editshelter.current_capacity = form.current_capacity.data
		db.session.add(editshelter)
		db.session.commit()
		counting_shows()
		flash("<strong>Update</strong>&nbsp; on <u>%s</u>." % editshelter.name, 'info')
		return redirect(url_for('index'))
	return render_template('edit_shelter.html', 
							editshelter=editshelter, 
							form=form,
							SHELTERS=SHELTERS)


@app.route('/<int:shelter_id>/<path:shelter_name>/delete/', methods=['GET', 'POST']) # pragma: no cover
def delete_shelter(shelter_id, shelter_name):
	SHELTERS = Shelter.query.all()
	deleteshelter = Shelter.query.filter_by(id=shelter_id).one()
	if request.method == "POST":
		db.session.delete(deleteshelter)
		db.session.commit()
		flash('<strong>Successfully</strong> deleted shelter <u>%s</u>.' % deleteshelter.name, 'danger')
		return redirect(url_for('index'))
	return render_template('delete_shelter.html', 
							deleteshelter=deleteshelter,
							SHELTERS=SHELTERS)


###  CRUD for Puppy  ######
@app.route('/<int:shelter_id>/<path:shelter_name>/profile/<int:puppy_id>') # pragma: no cover
def puppy_profile(shelter_id,shelter_name,puppy_id):
	SHELTERS = Shelter.query.all()
	puppy = Puppy.query.filter_by(id=puppy_id).one()
	return render_template('puppy_profile.html', 
							puppy=puppy,
							SHELTERS=SHELTERS)


## create 
@app.route('/new-puppy', methods=['GET', 'POST']) # pragma: no cover
def new_puppy():
	SHELTERS = Shelter.query.all()
	shelterq = Shelter.query.all()
	form = CreatePuppy()
	form1 = CreateProfile()
	form.shelter.choices = [(i.id,i.name) for i in shelterq]
	if form.validate_on_submit() and form1.validate_on_submit:
		newpuppy = Puppy(name=form.name.data, gender=form.gender.data, dateOfBirth=create_random_age(), picture=form.picture.data, shelter_id=form.shelter.data, weight=create_random_weight(), show=True)
		db.session.add(newpuppy)
		db.session.commit()
		newprofile = Profile(breed=form1.breed.data, specialNeeds=form1.specialNeeds.data, description=descriptions(), puppy_id=newpuppy.id)
		db.session.add(newprofile)
		db.session.commit()
		if overflow(newpuppy.shelter_id):
			db.session.commit()
			counting_shows()
			flash('<strong>Successfully</strong> Added '+ '<u>' + newpuppy.name + '</u>' +  ' to ' + newpuppy.shelter.name, 'success')
			return redirect(url_for('index'))
		else:
			flash('<div class="text-capitalize"><strong>%s</strong></div> has too many puppies try another shelter!' % newpuppy.shelter.name, 'danger')
			db.session.rollback()
			counting_shows()
			return redirect(url_for('index'))
			
	return render_template('create_puppy.html', 
							form=form,
							form1=form1,
							SHELTERS=SHELTERS)


@app.route('/<int:shelter_id>/<path:shelter_name>/profile/<int:puppy_id>/edit/', methods=['GET','POST']) # pragma: no cover
def edit_puppy(shelter_id,shelter_name,puppy_id):
	SHELTERS = Shelter.query.all()
	shelterq = Shelter.query.all()
	editpuppy= Puppy.query.filter_by(id=puppy_id).one()
	editprofile = Profile.query.filter_by(puppy_id=editpuppy.id).one()
	form = CreatePuppy(obj=editpuppy)
	form1 = CreateProfile(obj=editprofile)
	form.shelter.choices = [(i.id,i.name) for i in shelterq]
	if form.validate_on_submit():
		editpuppy.name = form.name.data
		editpuppy.gender = form.gender.data
		editpuppy.picture = form.picture.data
		editpuppy.weight = form.weight.data
		editpuppy.shelter_id = form.shelter.data
		editpuppy.weight = form.weight.data
		
		editprofile.breed = form1.breed.data
		editprofile.specialNeeds = form1.specialNeeds.data
		editprofile.description = form1.description.data 
		db.session.add(editpuppy)
		db.session.add(editprofile)
		if overflow(editpuppy.shelter_id):
			db.session.commit()
			counting_shows()
			flash('<strong>%s</strong> was successfully edited!' % editpuppy.name, 'info')
			return redirect(url_for('puppy_profile', 
								shelter_id=shelter_id,
								shelter_name=shelter_name,
								puppy_id=puppy_id
								))
		else:
			flash('<strong>%s</strong> has too many puppies try another.'% editpuppy.shelter.name, 'danger')
			db.session.rollback()
			counting_shows()
			return redirect(url_for('puppy_profile', 
								shelter_id=shelter_id,
								shelter_name=shelter_name,
								puppy_id=puppy_id))
	return render_template("edit_puppy_profile.html", 
							editpuppy=editpuppy, 
							form=form,
							form1=form1,
							SHELTERS=SHELTERS)


@app.route('/<int:shelter_id>/<path:shelter_name>/profile/<int:puppy_id>/delete/', methods=['GET','POST']) # pragma: no cover
def delete_puppy(shelter_id, shelter_name, puppy_id):
	SHELTERS = Shelter.query.all()
	deletepuppy = Puppy.query.join(Profile, Puppy.id==Profile.puppy_id).filter(Puppy.id==puppy_id).one()
	if request.method == 'POST':
		db.session.delete(deletepuppy)
		db.session.commit()
		counting_shows()
		flash('<strong>%s</strong>&nbsp;was just put to sleep!' % deletepuppy.name, 'danger')
		return redirect(url_for('index'))
	return render_template('delete_puppy_profile.html', 
							deletepuppy=deletepuppy,
							SHELTERS=SHELTERS)

	
# CRUD adoptor ######################
@app.route('/adoptors', methods=['GET', 'POST']) # pragma: no cover
def adoptor_list():
	SHELTERS = Shelter.query.all()
	adoptors = Adoptors.query.order_by(Adoptors.id.desc()).all()
	return render_template('adoptor_list.html', 
							adoptors=adoptors,
							SHELTERS=SHELTERS)


@app.route('/new-adoptor', methods=['GET', 'POST']) # pragma: no cover
def new_adoptor():
	SHELTERS = Shelter.query.all()
	error = None
	form = CreateAdoptor()
	if form.validate_on_submit():
		newadoptor = Adoptors(name=form.name.data, email=form.email.data)
		db.session.add(newadoptor)
		db.session.commit()
		logging.debug('A new adoptor was created named %s-%s', newadoptor.name, newadoptor.email)
		flash('<strong>Just created</strong> a new adoptor named <u>%s</u>' % newadoptor.name, 'info')
		return redirect(url_for('adoptor_list'))
	return render_template('create_adoptor.html', 
							form=form, 
							error=error,
							SHELTERS=SHELTERS)


@app.route('/adoptors/profile/<int:adoptor_id>/edit/', methods=['GET','POST']) # pragma: no cover
def edit_adoptor(adoptor_id):
	SHELTERS = Shelter.query.all()
	editadoptor = Adoptors.query.filter_by(id=adoptor_id).one()
	form = CreateAdoptor(obj=editadoptor)
	if form.validate_on_submit():
		editadoptor.name = form.name.data
		editadoptor.email = form.email.data
		db.session.add(editadoptor)
		db.session.commit()
		logging.debug('A new adoptor was edited named %s', editadoptor.name)
		flash('<strong>Successful</strong> edit of this adoptor who is now named <u>%s</u>' % editadoptor.name, 'info')
		return redirect(url_for('adoptor_list'))
	return render_template('edit_adoptor.html', 
							editadoptor=editadoptor, 
							form=form,
							SHELTERS=SHELTERS)


@app.route('/adoptors/profile/<int:adoptor_id>/delete/', methods=['GET','POST']) # pragma: no cover
def delete_adoptor(adoptor_id):
	SHELTERS = Shelter.query.all()
	deleteadoptor = Adoptors.query.filter_by(id=adoptor_id).one()
	if request.method == 'POST':
		db.session.delete(deleteadoptor)
		db.session.commit()
		logging.debug('An adoptor was deleted named %s', deleteadoptor.name)
		flash('<strong>You just</strong> deleted <u>%s</u>' % deleteadoptor.name, 'danger')
		return redirect(url_for('adoptor_list'))
	return render_template('delete_adoptor.html', 
							deleteadoptor=deleteadoptor,
							SHELTERS=SHELTERS)


### CRUD for adopting a puppy
@app.route('/<int:shelter_id>/<path:shelter_name>/profile/<int:puppy_id>/adopt/', methods=['GET','POST']) # pragma: no cover
def adoptions(shelter_id,shelter_name,puppy_id):
	SHELTERS = Shelter.query.all()
	puppy = Puppy.query.filter_by(id=puppy_id).one()
	adoptors = db.session.query(Adoptors).all()
	if request.method == 'POST':
		adoptorid = request.form.get('pupadopt')
		return redirect(url_for('adoption_success',
								 shelter_id=puppy.shelter.id,
								 shelter_name=puppy.shelter.name_slug,
								 puppy_id=puppy.id,
								 adoptor_id=adoptorid))
	return render_template('adopt_puppy.html',  
							puppy=puppy, 
							adoptors=adoptors)


@app.route('/<int:shelter_id>/<path:shelter_name>/profile/<int:puppy_id>/adopt/<int:adoptor_id>/', methods=['GET','POST']) # pragma: no cover
def adoption_success(shelter_id,shelter_name,puppy_id,adoptor_id):
	SHELTERS = Shelter.query.all()
	puppy = Puppy.query.filter_by(id=puppy_id).one()
	adoptor = Adoptors.query.filter_by(id=adoptor_id).one()
	if request.method == 'POST':
		adoption = AdoptorsPuppies(puppy_id=request.form['puppyname'], adoptor_id=request.form['adoptorname'])
		puppy.show = False
		db.session.add(adoption)
		db.session.add(puppy)
		db.session.commit()
		counting_shows()
		message = twilio_cred().sms.messages.create(to="+19415853084", from_="+19414515401", body=adoptor.name +" just adopted " + puppy.name + " from " + puppy.shelter.name + ".  Congrats!", media_url=[puppy.picture] )
		send_email(adoptor.name + " just adopted " + puppy.name, "me@jeffreiher.com", ["jreiher2003@yahoo.com"], render_template('email.txt', puppy=puppy, adoptor=adoptor), render_template('email.html', puppy=puppy, adoptor=adoptor))
		flash('<strong>Successful</strong> adoption', 'success')
		return redirect(url_for('list_adoptions'))
	return render_template('adoption_success.html', 
							puppy=puppy, 
							adoptor=adoptor,
							SHELTERS=SHELTERS)


@app.route('/list-adoptions', methods=['GET', 'POST']) # pragma: no cover
def list_adoptions():
	SHELTERS = Shelter.query.all()
	adoptions = AdoptorsPuppies.query.order_by(AdoptorsPuppies.adopt_date.desc()).all()
	return render_template('list_adoptions.html', 
							adoptions=adoptions,
							SHELTERS=SHELTERS)



@app.route('/sms')
def send_sms():
	message = twilio_cred().sms.messages.create(to="+19415853084", from_="+19414515401", body="yo mama? test send")
	return message.sid
