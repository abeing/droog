"""Unittests for World class."""

from .. import world
from ..world import Location


def test_location_offset_zero():
    """Test that Locations can be offset correctly."""
    loc = Location(10, 4)
    offset_loc = loc.offset(0, 0)
    assert offset_loc == loc


def test_location_offset():
    """Test that Locations can be offset correctly."""
    loc = Location(4, 3)
    offset_loc = loc.offset(2, -6)
    assert offset_loc.row == 6 and offset_loc.col == -3


def test_location_distance_to():
    """Test that distance_to returns the pythagorean theorem result."""
    start = Location(7, 11)
    end = start.offset(3, 4)  # 3**2 + 4**2 = 5**2
    assert start.distance_to(end) == 5
    assert end.distance_to(start) == 5


def test_location_delta_to():
    """Test that delta_to() gives us the right direction."""
    start = Location(5, 0)
    end = Location(5, 10)  # In the X (col) direction only.
    delta_se = start.delta_to(end)
    assert delta_se.row == 0
    assert delta_se.col == 1
    delta_es = end.delta_to(start)
    assert delta_es.row == 0
    assert delta_es.col == -1


def test_empty_map():
    """Test that an emtpy map works."""
    sut = world.World(10, 10)
    assert sut
    assert sut.cols == sut.rows == 10
    assert sut.cell(Location(9, 9))


def test_valid_locations():
    """Test that an empty map has the right size."""
    sut = world.World(5, 5)
    assert sut.is_valid_location(Location(4, 4))
    assert not sut.is_valid_location(Location(4, 5))
    assert not sut.is_valid_location(Location(5, 4))


def test_glyph_at():
    """Test that a location within the map has a glyph."""
    sut = world.World(7, 5)
    assert sut.glyph_at(Location(4, 4)) == '.'
