An outline of the 15 steps to writing a roguelike from Rouge Basin.
See: http://www.roguebasin.com/index.php?title=How_to_Write_a_Roguelike_in_15_Steps

[X] Step 1 - Decide to write a game
[X] Step 2 - Hello world
[X] Step 3 - It's a boy!
[X] Step 4 - The map
[ ] Step 6 - It's alive! Alive!
    [ ] Implement other creatures (monsters) and time. 
    [X] Add a single monster to begin with.
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
    [ ] Add ites. For start, just objects you can pick up -- no properties.
    [ ] Gradually give them properties, kinds, stats, etc.
    [ ] Implement inventory
    [ ] Implement picking up and dropping.
    [ ] Equipping and using (no effects yet)
    [ ] Also add stacking
    [ ] Containers (if you want them), etc?
[ ] Step 10 - Magic
    [ ] Add item effects.
    [ ] Add special monster attacks
    [ ] Add spells (abilities)
    [ ] Add items and monsters to test them.
[ ] Step 11 - Simple game
    [ ] Try to make a simple, hard-coded game.
    [ ] Play it and give it to your friends.
    [ ] Test the mechanics you've implemented so far.
    [ ] See if the game is fun.
    [ ] Change everything you need to change.
    [ ] Don't forget to test a lot.
    [ ] Always ask someone to test the game's 'fun factor', or test it yourself after a while;
        it's hard to notice some things right away.
[ ] Step 12 - Levels
    [ ] Write your level generators.
    [ ] Add more monsters and items, with their effects, as needed.
[ ] Step 14 - Citizens
    [ ] Add NPCs, shopkeepers, and simple quests if you need them.
[ ] Step 15 - Free at last
    [ ] Start adding and testing all the 'unique' features you thought were so cool months (years?) ago,
        when you started the whole thing.
    [ ] Revise your opinions of them and see if they fit the game.
    [ ] Write your pet random plot generator, factions system, infinite wilderness generator,
        neural network AI, or other unique feature, since you can now test it in a working game.
