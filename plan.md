An outline of the 15 steps to writing a roguelike from Rouge Basin.
See: http://www.roguebasin.com/index.php?title=How_to_Write_a_Roguelike_in_15_Steps

[X] Step 1 - Decide to write a game
[X] Step 2 - Hello world
[ ] Step 3 - It's a boy!
    [ ] Make the routines that display map characters, status lines and messages.
        [ ] I should check to make sure that my message routines work correctly.
[ ] Step 4 - The map
    [ ] Maybe make a look command?
    [ ] Maybe add doors and open/close commands
[ ] Step 6 - It's alive! Alive!
    [ ] Implement other creatures (monsters) and time.
    [ ] Add a single monster to begin with.
    [ ] Give him some simple AI (like, say, stay still, or maybe move randomly).
    [ ] Start with my turn-your turn, then implment the time system you want
        (or, usually, a simplification of it and gradually make it more complicated later.)
[ ] Step 7 - Interaction
    [ ] Add stats for your creatures. A simplification of the ones you envisioned, probably.
        It's best to add stats as they are needed, not because they 'look cool', but you might not
        be able to resist.
    [ ] Make the creatures notice each other -- bump, attack, etc. Gradually improve their AIS,
        so that they can chase the player.
    [ ] Implement and test the combat system -- without equipment for now, just hardcode the values.
[ ] Step 8 - Data files
    [ ] Move the creature, map features, etc. definitions to data files. Forget about scripting for
        now. If something cannot be moved -- just leave it for now.
[ ] Step 9 - Items
