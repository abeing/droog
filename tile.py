class Tile:
	def __init__(self, glyph, description, walkable):
		self._glyph = glyph
		self._description = description
		self._walkable = walkable

	def walkable(self):
		return self._walkable

	def glyph(self):
		return self._glyph

def makeStreet():
	return Tile('#', "Street", True)

def makeEmpty():
	return Tile(' ', "Open Space", True)

def makeShield():
	return Tile('~', "Shield", False)

def makeShieldGenerator():
	return Tile('G', "Shield Generator", False)