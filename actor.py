class Actor(object):
    """The Actor class manages action points and acting in turn order."""

    def __init__(self):
        self.act_func = None

    def act(self):
        """The actor will act and return a number of action point he spent on
        his action."""
        return self.act_func()
