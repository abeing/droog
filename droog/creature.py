
def make_zombie():
    return {"glyph": 'Z', "name": "a zombie", "str": 2, "dex": 2, "con": 2,
            "act_func": default_ai}


def default_ai():
    """Does nothing."""
    return 8
