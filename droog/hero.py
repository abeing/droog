"""Droog Hero class"""
import sys
import the
import creature


class Hero(creature.Creature):
    """The Hero is an instance of a Creature with its act() method calling the
    user iterface to determine actions."""
    def __init__(self, name, user_interface):
        super(Hero, self).__init__('@', name)
        self.user_interface = user_interface
        self.is_hero = True

    def __repr__(self):
        return "the hero %s" % self.name

    def act(self):
        command = self.user_interface.input()
        if command in self.user_interface.movements:
            delta_y, delta_x = self.user_interface.movements[command]
            return the.world.move_hero(delta_y, delta_x)
        if command == '/':
            self.user_interface.look(the.world)
            return 0
        if command == '~':
            self.user_interface.wizard(the.world)
        if command == 'q':
            sys.exit(0)
        return 0
