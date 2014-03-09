import curses
import map
import renderer

class Hero:
    pass

render = renderer.Renderer()
theMap = map.Map(renderer.MAP_ROWS, renderer.MAP_COLUMNS)

# draw the map
render.map(theMap)

command = ' '

while command != ord('q'):
    command = render.input()
#    old_hero_x, old_hero_y = hero.x, hero.y
#    if command == ord('h'):
#        hero.x -= 1
#    elif command == ord('l'):
#        hero.x += 1
#    elif command == ord('j'):
#        hero.y += 1
#    elif command == ord('k'):
#        hero.y -= 1
#    elif command == ord('y'):
#        hero.x -= 1
#        hero.y -= 1
#    elif command == ord('u'):
#        hero.x += 1
#        hero.y -= 1
#    elif command == ord('b'):
#        hero.x -= 1
#        hero.y += 1
#    elif command == ord('n'):
#        hero.x += 1
#        hero.y += 1
    
#    if not theMap.isEmpty(hero.y, hero.x):
#        hero.x = old_hero_x
#        hero.y = old_hero_y
        
    # draw the hero
#    map_window.addch(old_hero_y, old_hero_x, ord(' '))
#    map_window.addch(hero.y, hero.x, ord("@"))
#    map_window.move(hero.y, hero.x)

render.shutdown()