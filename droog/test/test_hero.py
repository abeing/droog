import mock
from .. import hero


def test_hero_glyph():
    """Test that the her's glyph is a '@'."""
    sut = hero.Hero("Tester", mock.Mock())
    assert sut.glyph == '@'
