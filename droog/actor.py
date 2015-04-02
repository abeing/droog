class Actor(object):
    """The Actor class provides an act() interface the engine uses to have each
    actor act when their turn comes up."""

    DONE = -1

    def act(self):
        """Perform an action and return action cost. Children should override
        this method."""
        raise NotImplementedError("Actor.act() should be overridden.")
