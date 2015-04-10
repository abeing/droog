"""Unittests for World class."""

from .. import world


def test_empty_map():
    """Test that an emtpy map works."""
    sut = world.World(10, 10)
    assert sut
    assert sut.width == sut.height == 10
    assert sut.is_empty(9, 9)


def test_valid_locations():
    """Test that an empty map has the right size."""
    sut = world.World(5, 5)
    assert sut.is_valid_location(4, 4)
    assert not sut.is_valid_location(4, 5)
    assert not sut.is_valid_location(5, 4)


def test_glyph_at():
    """Test that a location within the map has a glyph."""
    sut = world.World(7, 5)
    assert sut.glyph_at(4, 4) == '.'


def test_glyph_at_out_of_bounds():
    """Test that any illegal location is the force field glyph."""
    sut = world.World(5, 5)
    assert sut.glyph_at(4, -1) == '~'  # negative y
    assert sut.glyph_at(-4, 3) == '~'  # negative x
    assert sut.glyph_at(4, 5) == '~'  # out of range y
    assert sut.glyph_at(54, 3) == '~'  # out of range x