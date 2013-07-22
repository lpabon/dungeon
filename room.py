
import sys
import random


class Treasure:

	types = [ 'Gold',
			'Sword',
			'Wand',
			'Armor',
			'Puppy',
			'Healing Potion']

	def __init__(self):
		self.my_type = self.types[ int(random.random()*len(self.types)) ]

class GamePiece:

	def __init__(self, life=0):
		if life == 0:
			self.life = int(random.random()*100)
		else:
			self.life = life

	def hit(self, points):
		self.life -= points

	def heal(self, points):
		self.life += points

	def life_points(self):
		return self.life

	def kill(self):
		self.life = 0

	def is_alive(self):
		if self.life > 0:
			return True
		else:
			return False


class Monster(GamePiece):

	types = ['Minator', 
			'Fire Dragon', 
			'Goblin', 
			'Orc', 
			'Tiny Toilet', 
			'Gigantic Ant', 
			'Supid Cato', 
			'Momo the Giant Elf']

	def __init__(self):
		self.my_type = self.types[ int(random.random()*len(self.types)) ]
		GamePiece.__init__(self)

class Hero(GamePiece):

	def __init__(self, name, life):
		self.my_name = name
		GamePiece.__init__(self, life)


class Room:

	def __init__(self):
		if 45 > int(random.random()*100):
			self.monster = Monster()
		else:
			self.monster = None

		if 75 > int(random.random()*100):
			self.treasure = Treasure()
		else:
			self.treasure = None

	def status(self):
		if None != self.monster:
			return "A %s is attacking you with %d life" % (self.monster.my_type, self.monster.life_points())
		else:
			return "...eerie silence..."

	def is_there_a_monster(self):
		if self.monster != None:
			return self.monster.is_alive()
		else:
			return False

	def is_there_treasure(self):
		return self.treasure != None

	def is_empty(self):
		return not self.is_there_a_monster() and not self.is_there_treasure()



h = Hero('Leia', 2000)

for i in range(200):
	print "Stepping into a new room %d...[%s:%d]" % (i, h.my_name, h.life_points())
	r = Room()
	print r.status()
	while r.is_there_a_monster():
		if r.monster.my_type == 'Supid Cato':
			myhit = int(random.random()*100)
		else:
			myhit = int(random.random()*20)
		print "%s hits %s with %d points" % (h.my_name, r.monster.my_type, myhit) 
		r.monster.hit(myhit)
		if not r.monster.is_alive():
			print "Hooray! %s is dead" % (r.monster.my_type)

			myheals = int(random.random()*50)
			h.heal(myheals)
			print "Killing the moster has made you awesomenerr by %d points" % (myheals)

		else:
			if r.monster.my_type == 'Fire Dragon':
				myhit = int(random.random()*500)
			else:
				myhit = int(random.random()*20)
			print "%s hits %s with %d points" % (r.monster.my_type, h.my_name, myhit) 
			h.hit(myhit)

			if not h.is_alive():
				print "Aaaarrrrgggghhhhhhhh!!!"
				sys.exit(0)

				
	if r.is_there_treasure():
		print "You got a %s!" % (r.treasure.my_type)
		if r.treasure.my_type == 'Healing Potion':
			myheals = int(random.random()*500)
			h.heal(myheals)
			print "Your thirst has been quenched by %d points" % (myheals)
		elif r.treasure.my_type == 'Puppy':
			print "He licks you all over healing you 100 points"
			h.heal(100)
	else:
		print "You cry and cry, but you still get nothin"




