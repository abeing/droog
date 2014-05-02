class Creature:
	def __init__(self, glyph, name, str, dex, con):
		"""Creates a creature."""
		self.glyph = glyph
		self.name = name
		self.str = 2
		self.dex = 2
		self.con = 2

def make_hero():
	return Creature('@', "the hero", 2, 2, 2)

def make_zombie():
	return Creature('Z', "a zombie", 2, 2, 2)

def make_dog():
	return Creature('d', "a zombie dog", 2, 3, 1)

def make_cop():
	return Creature('C', "a COP", 4, 1, 2)
