class Tile:
	def __init__(self, glyph, description, walkable):
		self.glyph = glyph
		self.description = description
		self.walkable = walkable

def make_street():
	return Tile('#', "Street", True)

def make_empty():
	return Tile(' ', "Open Space", True)

def make_shield():
	return Tile('~', "Shield", False)

def make_shield_generator():
	return Tile('G', "Shield Generator", False)