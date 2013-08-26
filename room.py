
import sys
import random
from optparse import OptionParser
import pygame
import time


class Treasure:

	types = [ 'Gold',
			'Sword',
			'Wand',
			'Armor',
			'Puppy',
			'Healing Potion',
			'Sloppy Oreos']

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
			'Momo the Giant Elf',
			'Silly Nannies']

	def __init__(self):
		self.my_type = self.types[ int(random.random()*len(self.types)) ]
		GamePiece.__init__(self)

class Hero(GamePiece):

	def __init__(self, name, life):
		self.my_name = name
		GamePiece.__init__(self, life)


class Room:

	types = ['Desert',
			'Jungle',
			'Really Cool and Snowy Room',
			'Kids Play Area',
			'Disco',
			'Gothic',
			'Cubicle O Death',
			'Candy Shop']

	def __init__(self):
		if 45 > int(random.random()*100):
			self.monster = Monster()
		else:
			self.monster = None

		if 75 > int(random.random()*100):
			self.treasure = Treasure()
		else:
			self.treasure = None

		self.my_type = self.types[ int(random.random()*len(self.types)) ]

	def status(self):
		print "You walk into a %s room" % (self.my_type)
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

	def hero_bufs(self):
		buf_rooms = ['Kids Play Area',
				'Jungle', 'Candy Shop']
		debuf_rooms = [ 'Cubicle O Death', 'Disco']

		if self.my_type in buf_rooms:
			return int(random.random()*50)
		elif self.my_type in debuf_rooms:
			return -1*int(random.random()*50)
		else:
			return 0

	def monster_bufs(self):
		buf_rooms = [ 'Gothic',
				'Cubicle O Death',
				'Desert' ]
		debuf_rooms = [ 'Kids Play Area',
				'Jungle']

		if self.my_type in buf_rooms:
			return int(random.random()*50)
		elif self.my_type in debuf_rooms:
			return -1*int(random.random()*50)
		else:
			return 0

def play(filename):
	if pygame.mixer.music.get_busy():
		pygame.mixer.music.queue(filename)
	else:
		pygame.mixer.music.load(filename)
		pygame.mixer.music.play()

################## MAIN ##################

# Create the parameters

pygame.mixer.init()
parser = OptionParser()
parser.add_option("-H", "--hero", dest="hero_name", type="string", default="Leia",
		help="Your hero name")
parser.add_option("-l", "--hero-life", dest="hero_life", type="int", default=2000,
		help="The amount of life your hero has")
parser.add_option("-r", "--number-of-rooms", dest="number_of_rooms", type="int", default=200,
		help="The amount of rooms the hero has to get through")
parser.add_option("-s", "--simulate", dest="simulate", action="store_true", default=False,
		help="Do you want to simulate the dungeon crawl")

(options, args) = parser.parse_args()

h = Hero(options.hero_name, options.hero_life)

for i in range(options.number_of_rooms):
	print ""
	print 60*"-"
	play('Rolling_Switch.ogg')
	print "Stepping into a new room %d...[%s:%d]" % (i, h.my_name, h.life_points())
	r = Room()
	print r.status()
	if r.is_there_a_monster():
		monster_buf = r.monster_bufs()
		if monster_buf > 0:
			print "%s feels real good by %d" % (r.monster.my_type, monster_buf)
		elif monster_buf < 0:
			print "%s looks kinda small by %d" % (r.monster.my_type, monster_buf)

	hero_buf = r.hero_bufs()
	if hero_buf > 0:
		print "%s says taa-daa I feel jacked by %d" % (h.my_name, hero_buf)
	elif hero_buf < 0:
		print "%s coughs up blood and strength weakens by %d" % (h.my_name, hero_buf)

	while r.is_there_a_monster():
		if r.monster.my_type == 'Supid Cato':
			myhit = int(random.random()*100)
		else:
			myhit = int(random.random()*50)

		# Adjust myhit according to the room bufs
		myhit += hero_buf
		if myhit < 0:
			myhit=0

		print "%s hits %s with %d points" % (h.my_name, r.monster.my_type, myhit)
		play('Slash8-Bit.ogg')
		r.monster.hit(myhit)
		if not r.monster.is_alive():
			if r.monster.my_type == 'Fire Dragon':
				play('BossDeath.ogg')
			else:
				play('EnemyDeath.ogg')
			print "Hooray! %s is dead" % (r.monster.my_type)

			myheals = int(random.random()*50)
			h.heal(myheals)
			print "Killing the moster has made you awesomenerr by %d points" % (myheals)

		else:
			if r.monster.my_type == 'Fire Dragon':
				myhit = int(random.random()*500)
			else:
				myhit = int(random.random()*50)

			# Adjust monster hit accoring to room bufs
			myhit += monster_buf
			if myhit < 0:
				myhit=0
			print "%s hits %s with %d points" % (r.monster.my_type, h.my_name, myhit)
			play('Crush8-Bit.ogg')
			h.hit(myhit)

			if not h.is_alive():
				play('Death.ogg')
				print "Aaaarrrrgggghhhhhhhh!!!"
				time.sleep(1)
				sys.exit(0)
		time.sleep(1)

				
	if r.is_there_treasure():
		print "You got a %s!" % (r.treasure.my_type)
		if r.treasure.my_type == 'Healing Potion':
			myheals = int(random.random()*500)
			h.heal(myheals)
			play('Heal8-Bit.ogg')
			print "Your thirst has been quenched by %d points" % (myheals)
		elif r.treasure.my_type == 'Puppy':
			play('Heal8-Bit.ogg')
			print "He licks you all over healing you 100 points"
			h.heal(100)
		elif r.treasure.my_type == 'Sloppy Oreos':
			myhit = int(random.random()*60)
			print "Oh crap, my teeth hurt!  You lose %d points of health" % (myhit)
			h.hit(myhit)
		else:
			play('Powerup.ogg')

		if not h.is_alive():
			play('Death.ogg')
			print "Son of a gun, the treasure killed me..arrgh"
			time.sleep(1)
			sys.exit(0)
	else:
		print "You cry and cry, but you still get nothin"

	if not options.simulate:
		raw_input("press enter to continue")
	time.sleep(1)

print "%s You've slayed all dem monsters. You exit the dungeon with %d life" \
		 % (h.my_name, h.life_points())




