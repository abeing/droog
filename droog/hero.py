"""Droog Hero class"""
import sys
import the
import engine
import creature
import item


class Hero(creature.Creature):
    """The Hero is an instance of a Creature with its act() method calling the
    user iterface to determine actions."""
    def __init__(self, name, user_interface):
        super(Hero, self).__init__('@', name)
        self.user_interface = user_interface
        self.is_hero = True
        self.weapon = item.make_knife()
        self.inventory.append(item.make_knife())
        self.inventory.append(item.make_knife())
        self.inventory.append(item.make_knife())

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
        if command == '?':
            self.user_interface.help()
        return 0

    def melee_attack(self, target):
        """Performs a melee attack against the target."""
        return engine.attack(self, target, self.weapon.attack)
