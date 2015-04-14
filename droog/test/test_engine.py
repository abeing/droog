import mock
from .. import engine
from .. import the

the.world = mock.Mock()
the.hero = mock.Mock()


def test_generator_init():
    """Test that a freshly-created generator has three hit points."""
    generator = engine.Generator()
    assert generator.health == 3


def test_generator_deactivate():
    """Test that deactivating a generator three times results in a win."""
    generator = engine.Generator()
    generator.deactivate()
    assert generator.health == 2
    generator.deactivate()
    assert generator.health == 1
    generator.deactivate()
    assert generator.health == 0
    assert the.hero.is_dead
