class Ai:
    def __init__(self, creature, world):
        """Constructs an AI for a given creature in a given world.

        The creature's act_func will be set to the AI's act_func so that when
        the creature's turn comes up in the turn order, the AI will determine
        the creature's action.
        """
        self.creature = creature
        self.world = world
        self.creature.act_func = self.act_func

    def act_func(self):
        """Does nothing."""
        return 8
