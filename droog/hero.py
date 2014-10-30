import sys
import the
import creature


class Hero(creature.Creature):
    def __init__(self, name, ui):
        super(Hero, self).__init__('@', name, 2, 2, 2)
        self.ui = ui

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
        if command == '~':
            self.ui.wizard(the.world)
        if command == 'q':
            sys.exit(0)
        return 0
