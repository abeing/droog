import world
import random
import engine


class Ai:
    def __init__(self, creature, world):
        """Constructs an AI for a given creature in a given world.

        The creature's act_func will be set to the AI's act_func so that when
        the creature's turn comes up in the turn order, the AI will determine
        the creature's action.
        """
        self.creature = creature
        self.world = world
        # TODO self.creature.act_func = self.act_func

    def act_func(self):
        """Zombies use the following decision tree:

        1) If adjacent to the hero, bite her.
        2) If within 15 steps of the hero, move towards her.
        3) Otherwise, move randomly."""
        if self.creature.loc:
            (old_y, old_x) = self.creature.loc
            (hero_y, hero_x) = self.world.hero_location

            # 1) If adjacent to the hero, bite her.
            if world.distance_between(hero_y, hero_x, old_y, old_x) == 1:
                return engine.attack_bite(self.creature, self.world.hero)

            # 2) If within 15 steps of the hero, move towards her.
            elif world.distance_between(hero_y, hero_x, old_y, old_x) < 15:
                delta_y = 1 if (hero_y - old_y > 0) else -1
                delta_x = 1 if (hero_x - old_x > 0) else -1

            # 3) Otherwise, move randomly.
            else:
                delta_y = random.choice([-1, 0, 1])
                delta_x = random.choice([-1, 0, 1])
            cost = self.world.move_creature(old_y, old_x, delta_y, delta_x)
            if not cost == 0:
                return cost
        return 6  # If the creature fails to move, it stands around a while
