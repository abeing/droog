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
    sut = world.World(40, 40)
    assert sut
    assert sut.cols == sut.rows == 40
    assert sut.cell(Location(9, 9))


def test_valid_locations():
    """Test that an empty map has the right size."""
    sut = world.World(40, 40)
    assert sut.is_valid_location(Location(39, 39))
    assert not sut.is_valid_location(Location(39, 40))
    assert not sut.is_valid_location(Location(40, 39))


def test_glyph_at():
    """Test that a location within the map has a glyph."""
    sut = world.World(47, 45)
    glyph_44 = sut.glyph_at(Location(4, 4))
    assert glyph_44 == '.' or glyph_44 == '#'


def test_glyph_at_creature():
    """Test that the glyph at a location with the creature returns the
    creature's glyph."""
    sut = world.World(40, 40)
    monster = mock.Mock()
    monster.glyph = '$'
    sut.spawn_monster(monster)
    assert monster.loc
    assert sut.glyph_at(monster.loc) == '$'


def test_glyph_at_item():
    """Test that the glyph at a location with an item returns the item's
    glyph."""
    sut = world.World(40, 40)
    item = mock.Mock()
    item.glyph = '/'
    location = Location(4, 3)
    sut.add_item(location, item)
    assert sut.glyph_at(location) == item.glyph


def test_generate_city():
    """Test that generating a city works."""
    sut = world.World(40, 40)
    world.generate_city(sut)
    assert sut.glyph_at(Location(20, 20)) == 'G'


def test_generate_world():
    """Test the new genreation function."""
    sut = world.World(40, 40)
    pass  # TODO put an assertion here.


def test_create_junction_grid():
    grid = world._create_junction_grid(40, 45, 20)
    assert len(grid) == 2
    assert len(grid[0]) == 2


def test_create_random_junction():
    assert world._generate_random_junction(None, None, None, True)[3] == True
    assert world._generate_random_junction(None, None, False, True)[2] == False
    assert world._generate_random_junction(True, None, None, True)[0] == True
    assert world._generate_random_junction(True, None, None, True)[3] == True


def test_log_junction_grid():
    grid = world._create_junction_grid(200, 200, 20)
    world._log_junction_grid(grid)
    # This should not output anything unless the logging fails.
    # assert False

