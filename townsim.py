import random
import math
from random import shuffle

hobbies = ["knitting", "ritual combat", "taking care of animals", "genetic engineering", "aliens", "playing the flute", "playing the violin", "playing the piano", "cloning cats", "gardening", "selling antiques"]
positive_feelings = ["happy", "content", "aroused", "inspired"]
negative_feelings = ["sad", "angry"]
feelings = positive_feelings + negative_feelings + ["neutral"]

class Person:
	"""A single townsperson!"""

	people = []

	def __init__(self, name, interests = []):
		self.name = name
		self.combat_skill = 1
		self.feeling = "neutral"
		self.interests = {}
		self.friends = []
		self.matespirits = []
		self.kismeses = []
		self.red_crushes = []
		self.black_crushes = []

		if not interests or interests == [""]:
			for i in range(0, 3):
				self.interests[random.choice(hobbies)] = 3
		else:
			for item in interests:
				self.interests[item] = 3

		#make other people know me
		for person in self.people:
			person.interests[self] = 3
			self.interests[person] = 3

		self.people.append(self)

	def spend_time(self):
		interest = pick_from_hat(self.interests)
		# print(self.interests)
		# print(interest)
		# self.feeling = random.choice(feelings)

		decide_feelings(self, interest)
		
		if interest == "ritual combat":
			engage_in_ritual_combat(self, random.choice(self.people))

		adjust_interest(self, interest)

		if isinstance(interest, Person):
			adjust_romance(self, self.feeling, interest)
			decide_feelings(interest, self)
			adjust_interest(interest, self)
			adjust_romance(interest, interest.feeling, self)
			if self.feeling == "aroused" and interest.feeling == "aroused":
				produce_child(self, interest)

		if isinstance(interest, str):
			print(self.name + " spent the last hour on " + interest + " and now feels " + self.feeling + ".")
		elif isinstance(interest, Person):
			print(self.name + " spent the last hour talking to " + interest.name + " and now feels " + self.feeling + ".")
			print(interest.name + " spent the last hour talking to " + self.name + " and now feels " + interest.feeling + ".")

		return interest

	def print_state(self):
		print("")
		print(self.name + " is " + self.feeling + "!")
		print("Interests: " + str(self.interests))
		print("Red crushes: " + str(self.red_crushes))
		print("Matespirits: " + str(self.matespirits))
		print("Black crushes: " + str(self.black_crushes))
		print("Kismeses: " + str(self.kismeses))

	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name
	def __repr__(self):
		return self.name

def produce_child(me, interest):
	print(me.name + " and " + interest.name + " had a child!")
	new_name = input("What will they name their child? ")
	while new_name in Person.people:
		print("There's already someone with that name in this town! That'll get confusing. :(")
		new_name = input("Please pick a different name: ")
	Person(new_name, list(me.interests.keys()) + list(interest.interests.keys()))

def decide_feelings(me, interest):
	if interest not in me.interests.keys():
		me.interests[interest] = 0
	if me.interests[interest] > 0:
		decider = random.randint(0, me.interests[interest])
		if decider == 0:
			me.feeling = random.choice(negative_feelings + ["neutral"])
		else:
			me.feeling = random.choice(positive_feelings)
	elif me.interests[interest] < 0:
		decider = random.randint(0, math.fabs(me.interests[interest]))
		if decider == 0:
			me.feeling = random.choice(positive_feelings + ["neutral"])
		else:
			me.feeling = random.choice(negative_feelings)
	else:
		me.feeling = random.choice(feelings)

def adjust_interest(me, interest):
	if me.feeling in positive_feelings:
		me.interests[interest] = me.interests[interest] + 1
	elif me.feeling in negative_feelings:
		me.interests[interest] = me.interests[interest] - 2
		if me.interests[interest] == 0:
			me.interests[interest] = -1

def adjust_romance(me, feeling, interest):
	if feeling == "aroused":
		if me.interests[interest] > 0 and interest not in me.red_crushes:
			me.red_crushes.append(interest)
		elif me.interests[interest] < 0 and interest not in me.black_crushes:
			me.black_crushes.append(interest)
	if interest in me.red_crushes and me in interest.red_crushes:
		if interest not in me.matespirits:
			me.matespirits.append(interest)
		if me not in interest.matespirits:
			interest.matespirits.append(me)
	if interest in me.black_crushes and me in interest.red_crushes:
		if interest not in me.kismeses:
			me.kismeses.append(interest)
		if me not in interest.kismeses:
			interest.kismeses.append(me)

def pick_from_hat(dict):
	if len(dict.keys()) > 1:
		total = 0
		range_dict = {}
		for item in dict.keys():
			range_dict[item] = (total, total + math.fabs(dict[item]) - 1)
			total = total + math.fabs(dict[item])

		# print(range_dict)
		decision = random.randint(0, total - 1)
		for item in range_dict.keys():
			if decision >= range_dict[item][0] and decision <= range_dict[item][1]:
				return item
			# else:
			# 	print("Error!")
			# 	print(decision)
	else:
		for item in dict.keys():
			return item

def engage_in_ritual_combat(person_one, person_two):
	winner = pick_from_hat({person_one: person_one.combat_skill, person_two: person_two.combat_skill})
	
	if winner == person_one:
		loser = person_two
	else:
		loser = person_one

	person_one.combat_skill = person_one.combat_skill + 1
	person_two.combat_skill = person_two.combat_skill + 1
	print(winner.name + " beat " + loser.name + " in ritual combat! They have both gained combat skill.")

def have_an_hour(hour):
	print("")

	print(Person.people)

	if hour == 12:
		print("It is noon.")
	else:
		print("It is " + str(hour % 12) + " o'clock.")

	busy = []
	shuffle(Person.people)
	for person in Person.people:
		if person not in busy:
			interest = person.spend_time()
			if isinstance(interest, Person):
				busy.append(interest)
			busy.append(person)

	hour = hour + 1
	return hour

def prompt_for_people():
	yn = input("Enter a name to create a person! Enter nothing to go back to the town. ")
	while yn != "":
		name = yn

		while name == "" or name in Person.people:
			if name == "":
				name = input("You can't name a person the empty string! Try again: ")
			elif name in Person.people:
				name = input("Someone else already has that name! Try again: ")
		
		interests = input("What is " + name + " interested in? (Please separate interests with commas.) ")
		interests = interests.split(", ")
		Person(name, interests)
		yn = input("Enter a name to create a person! Enter nothing to go back to the town. ")

def welcome():
	print("Welcome to the town!")
	print("Any time you want, you can press P to make more people,")
	print("S to see how your townspeople are doing,")
	print("and H to hear these commands again.")
	print("Any other key press will quit the townsim.")
	print("")

def play():
	hour = 9
	enter = input("Press enter to keep playing!")
	while enter == "":
		hour = have_an_hour(hour)
		enter = input()
		if enter == "P" or enter == "p":
			prompt_for_people()
			enter = input("Press enter to keep playing!")
		elif enter == "H" or enter == "h":
			welcome()
			enter = input("Press enter to keep playing!")
		elif enter == "S" or enter == "s":
			print(Person.people)
			for person in Person.people:
				person.print_state()
			enter = input("Press enter to keep playing!")

#main, but without the, yknow, actual function
welcome()
print("It's your first townsperson!")
prompt_for_people()
play()