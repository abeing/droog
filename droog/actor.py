class Actor(object):
    """The Actor class provides an act() interface the engine uses to have each
    actor act when their turn comes up."""

    def act(self):
        """Perform an action and return action cost. Children should override
        this method, the default implementation does nothing and returns a
        large cost."""
        raise NotImplementedError("Actor.act() should be overridden.")
