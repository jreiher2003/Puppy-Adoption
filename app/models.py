import datetime # pragma: no cover
from app import db # pragma: no cover
from slugify import slugify # pragma: no cover
 
        
class Shelter(db.Model):

    __tablename__ = "shelter"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    address = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(20))
    zipCode = db.Column(db.String(10))
    website = db.Column(db.String)
    maximum_capacity = db.Column(db.Integer)
    current_capacity = db.Column(db.Integer)
    puppy = db.relationship("Puppy", cascade="save-update, merge, delete")
    
    def __init__(self,name,address,city,state,zipCode,website,maximum_capacity,current_capacity):
        self.name = name 
        self.address = address
        self.city = city 
        self.state = state 
        self.zipCode = zipCode
        self.website = website 
        self.maximum_capacity = maximum_capacity
        self.current_capacity = current_capacity    

    @property 
    def name_slug(self):
        return slugify(self.name)

    def __repr__(self):
        return '<name>: {}'.format(self.name)

class Puppy(db.Model):

    __tablename__ = "puppy"

    id = db.Column(db.Integer, primary_key=True)
    shelter_id = db.Column(db.Integer, db.ForeignKey('shelter.id'))
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(6), nullable = False)
    dateOfBirth = db.Column(db.Date)
    picture = db.Column(db.String)
    weight = db.Column(db.Numeric(10))
    show = db.Column(db.Boolean, default=True)
    shelter = db.relationship(Shelter)
    profile = db.relationship("Profile", uselist=False, back_populates="puppy", cascade="save-update, merge, delete")
    adoptor_puppies = db.relationship('AdoptorsPuppies', cascade="save-update, merge, delete")

    def __init__(self,shelter_id,name,gender,dateOfBirth,picture,weight,show):
        self.shelter_id = shelter_id
        self.name = name 
        self.gender = gender
        self.dateOfBirth = dateOfBirth
        self.picture = picture 
        self.weight = weight 
        self.show = show

    def __repr__(self):
        return '<name>: {}'.format(self.name)


class Profile(db.Model):

    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppy.id'))
    breed = db.Column(db.String(32))
    description = db.Column(db.String(500))
    specialNeeds = db.Column(db.String(500))
    puppy = db.relationship("Puppy", back_populates="profile")

    def __init__(self, puppy_id, breed, description,specialNeeds):
        self.puppy_id = puppy_id
        self.breed = breed
        self.description = description
        self.specialNeeds = specialNeeds

    def __repr__(self):
        return '<specialNeeds>: {}'.format(self.specialNeeds)
        

class Adoptors(db.Model):

    __tablename__ = "adoptors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(120))
    adoptor_puppies = db.relationship('AdoptorsPuppies', cascade="save-update, merge, delete")

    def __init__(self,name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<name>: {}'.format(self.name)


class AdoptorsPuppies(db.Model):
    __tablename__ = 'adoptors_puppies'
    
    adoptor_id = db.Column(db.Integer,db.ForeignKey('adoptors.id'), primary_key=True)
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppy.id'), primary_key=True)
    adopt_date = db.Column(db.Date, default=datetime.datetime.now())
    puppies = db.relationship(Puppy)
    adoptors = db.relationship(Adoptors)

    def __init__(self, adoptor_id,puppy_id):
        self.adoptor_id = adoptor_id
        self.puppy_id = puppy_id
       
    @property 
    def format_date(self):
        return '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=self.adopt_date)

    def __repr__(self):
        return '<date>: {}'.format(self.adopt_date)




