import engine


class Actor(object):
    """The Actor class manages action points and acting in turn order."""

    def __init__(self, dex):
        """Creates and actor with specified dexterity.

        The dexterity, if non-zero, is used by the engine to determine any
        modification to make to the action point cost of each action taken."""
        self._dex = dex
        self.act_func = None

    def act(self):
        """The actor will act and return a number of action point he spent on
        his action."""
        ap_cost = self.act_func()
        return engine.ap_mod(ap_cost, self._dex)
