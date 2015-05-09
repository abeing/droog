# Iteration 5

Scheduled 2 stories worth 10 points.
Velocity WAS 15. [14, 13, 15, 19]
Pylint score WAS 8.87.

## Add items to character creation. [5]

We want to be able to have items generated at character creation, so when the hero selects them in the dialog, they are added to his inventory.

We can change how choices are done in one of several ways.

1. Allow the player to select his weapon, then generate the appropriate-length lists of supporting items. This allows the player two choices, first for weapon, then for items.
2. Generate appropriate-length lists of weapon with supporting items and give the player one choice of one list which contains their entire starting inventory.

- Pick one of the scenarios for starting inventory selection.
- Create a function, or set of functions, to generate the sets of starting choices.
- Create a funtion to populate the starting inventory from the choices.

## Add ammunition. [5]

We want pistols to use ammunition when they fire and be reloadable.

- Add consumption of ammunition to firing the pistol.
	- Give the pistol a capacity of six shots
	- Each shot exhausts one bullet
- Add 9mm clips
	- Give the hero two clips to begin with
- Add a reload command `r`
	- When executed, allow the user to select an item in his inventory, similar to dropping an item.
	- If there exists in the hero's inventory an item capable of reloading the selected item, reset that item's current charges to maximum.

## Add porter. [5]

We want a local teleporter. There are two ways the hero might selected a destination.

1. Directly picking a location within range (possibly we can allow choosing locations the hero cannot currently see).
2. Selecting a general direction and having fate deside on the exact landing location.

We could have both availble with different energy costs.

- Add porter item calss.
- Add porter item to character creation.
	- Do this after we wire up item selection in character creation.
- Create target selection UI
	- Location selection or direction selection.
- Tweak FOV for better gameplay with porter.
	- We might want to be able to see father, for example.


# Backlog

- Add medical kit
- Add invisibility cloak
- Add batteries
- Add rifle
- Add lazer
- Add burning condition?
- Add bionic armor
- Add battle armor
- Invent third useful item
- Invent third armor type
- Make keys rebindable
- Monster spawning over time
- Clean up death
- Clean up UI updates
- Add line to target selection UI

# Iteration 4

Scheduled 3 stories worth 14 points.
Completed 3 stories worth 14 points.
Velocity is 15. [14, 13, 15, 19]
Pylint score is 8.87.

Complete stories
- Release 1. [3]
- Add pickup command. [3]
- Add pistol. [8]

# Iteration 3

Scheduled 4 stories worth 17 points.
Completed 3 stories worth 13 points.
Velocity is 15. [13, 15, 19]
Pylint score is 8.75.

Complete stories
  - Add character creation [5]
  - Generate city buildings. [8]
  - Write user manual [2]

Incomplete stories
  - Update zombies to use sight rather than scent. [2] Abandoned due to poor gameplay.

# Iteration 2

Scheduled 5 stories worth 23 points.
Completed 3 stories worth 15 points.
Velocity is 17. [15, 19]

Complete stories
  - Create a release [2]
  - Implement fog of war [8]
  - Add a death screen [5]

Incomplete stories:
  - Add character creation [5], moved to Iteration 3
  - Update zombies to use sight rather than scent. Moved to Iteration 3

# Iteration 1

Scheduled 12 stories worth 19 points.
Completed 12 stories worth 19 points.
Velocity is 19. [19]

Complete stories:
  - Add Knives [3]
  - Add unarmed attack [2]
  - Add bite attack [1]
  - Add stunned condition [3]
  - Add bleeding condition [3]
  - Add diseased condition [1]
  - Write a vision statement [0]
  - Update melee mechanics [1]
  - Improve the character sheet [1]
  - Have the message screen reset each player's turn [2]
  - Normalize hobbled and weakened mechanic. [1]
  - Clean up chat messages [1]
