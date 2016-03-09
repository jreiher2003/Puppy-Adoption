import random

breed = ["Bulldog", "Collie", "Boston Terrier", "Chihuahua", "German Shepherd", "Greyhound", "Labrador Retriever", "Maltese", "Schnauzer", "Pug", "Saint Bernard", "Shih-Tzu", "Siberian Husky", "Whippet"]


puppy_adj = ["active", 'good', "affectionate", "alert", "athletic", "brave", "bright-eyed", "crafty", "cuddly", 
            "cute", "energetic", "fluffy", "frisky", "gentle", "goofy", "happy", "huggable", "mischievous", "potty-trained", "zippy", "wonderful", "well-trained", "wagging", "unique", "trusty", "tough", "smart"]

puppy_verb = ["adore", "beg", "care for", "cuddle", "defend", "dig", "do tricks", "greet", "heel", "hunt", "kiss", "love", "obey", "pamper", "perform tricks", "roll", "roll over", "run", "run and play", "shake", "sit", "snuggle"]

sp_needs = ['Blind', 'Deaf', '3 legged', 'None', 'None','None', 'None', 'None','None', 'None','None']


def descriptions():
    vowels = ('a','e','i','o','u','A','E','I','O','U')
    x = random.choice(puppy_adj)
    v = random.choice(puppy_verb)
    if x.startswith(vowels):
        z = " is an " + x
        return "This " + z + ' dog that will ' + v + " you and your family."
    else:
        z = " is a " + x
        return "This " + z + ' dog that will ' + v + " you and your family."


def special_needs():
    return random.choice(sp_needs)


def breeds():
    return random.choice(breed)



