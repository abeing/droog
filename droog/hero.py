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
        self.ui = user_interface
        self.is_hero = True
        self.weapon = item.make_knife()
        self.inventory.append(item.make_knife())
        self.inventory.append(item.make_knife())
        self.inventory.append(item.make_knife())

    def __repr__(self):
        return "the hero %s" % self.name

    def act(self):
        command = self.ui.input()
        if command in self.ui.movements:
            delta_y, delta_x = self.ui.movements[command]
            return the.world.move_hero(delta_y, delta_x)
        if command == '/':
            self.ui.look(the.world)
            return 0
        if command == 'd':
            self.ui.drop(self, the.world)
        if command == '~':
            self.ui.wizard(the.world)
        if command == 'q':
            sys.exit(0)
        if command == '?':
            self.ui.help()
        return 0

    def melee_attack(self, target):
        """Performs a melee attack against the target."""
        return engine.attack(self, target, self.weapon.attack)

