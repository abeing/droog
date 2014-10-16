import world
import random


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
        """If within 15 steps of the hero, moves towards them, otherwise moves
        randomly."""
        if self.creature.loc:
            (old_y, old_x) = self.creature.loc
            (hero_y, hero_x) = self.world.hero_location
            if world.distance_between(hero_y, hero_x, old_y, old_x) < 15:
                delta_y = 1 if (hero_y - old_y > 0) else -1
                delta_x = 1 if (hero_x - old_x > 0) else -1
            else:
                delta_y = random.choice([-1, 0, 1])
                delta_x = random.choice([-1, 0, 1])
            if self.world.move_creature(old_y, old_x, delta_y, delta_x):
                return 1
        return 8
