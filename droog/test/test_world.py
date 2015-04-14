"""Unittests for World class."""

import mock
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


def test_location_delta_to_x():
    """Test that delta_to() gives us the right direction in the X plane."""
    start = Location(5, 0)
    end = Location(5, 10)  # In the X (col) direction only.
    delta_se = start.delta_to(end)
    assert delta_se.row == 0
    assert delta_se.col == 1
    delta_es = end.delta_to(start)
    assert delta_es.row == 0
    assert delta_es.col == -1


def test_location_delta_to_y():
    """Test that delta_to() givse us the right direction in the Y plane."""
    start = Location(80, 100)
    end = Location(50, 100)  # In the Y (row) direction only.
    delta_se = start.delta_to(end)
    assert delta_se.row == -1
    assert delta_se.col == 0
    delta_es = end.delta_to(start)
    assert delta_es.row == 1
    assert delta_es.col == 0


def test_location_repr():
    """Test that Location has a human-readable representation."""
    loc = Location(42, 7)
    rep = "%r" % (loc)
    assert rep == "(42, 7)"


def test_location_ne():
    """Test that two different locations compare as not equal."""
    first = Location(1, 2)
    second = (1, 2)
    assert first != second


def test_random_delta():
    """Test that random_delta() returns a delta in the range [-1..1] for both
    row and column."""
    for _ in xrange(100):
        delta = world.random_delta()
        assert -1 <= delta.row <= 1
        assert -1 <= delta.col <= 1


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


def test_glyph_at_creature():
    """Test that the glyph at a location with the creature returns the
    creature's glyph."""
    sut = world.World(20, 20)
    monster = mock.Mock()
    monster.glyph = '$'
    sut.spawn_monster(monster)
    assert monster.loc
    assert sut.glyph_at(monster.loc) == '$'


def test_glyph_at_item():
    """Test that the glyph at a location with an item returns the item's
    glyph."""
    sut = world.World(20, 20)
    item = mock.Mock()
    item.glyph = '/'
    location = Location(4, 3)
    sut.add_item(location, item)
    assert sut.glyph_at(location) == item.glyph


def test_generation():
    """Test that generating a city works."""
    sut = world.World(10, 10)
    world.generate_city(sut)
    assert sut.glyph_at(Location(5, 5)) == 'G'
