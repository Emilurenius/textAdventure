# .ta (textAdventure) scripting language file

The .ta file extention is used by the textAdventure scripting language. These files are interpreted by the game engine.

This wiki file will go through the different commands, and syntax of a .ta file, and how you can use it to create your own text adventure!

There will be no indepth explanainations of how to set up an adventure folder with all required files. Another wiki file will be written with that info.

For now, you can look at the premade tutorial for some hints at how it is set up.

## init scope:

The init scope is defined like this:
```
init:
// init commands here
:init
```
Notice that the init has a starting and an ending keyword. These are used to tell the interpreter where initialization starts, and where it ends

Insite the init scope is where you would import assets and mods. Importing these will not be possible after initialization is complete.

The interpereter also only supports one init scope per .ta file.

## init commands:

There are currently two init exclusive commands. These commands can only be used inside an init scope, because they usually need to be run before everything else.

### !importAsset:

`!importAsset` is used to import assets found inside the "assets folder" for the adventure.

Here is an example of how you would import an asset with the name "items":
```
init:
!importAsset : items
:init
```

### !importMod:

`!importMod` is used to import mods in the game engine's mods folder.

Here is an example of how you would import a mod with the name "extraItems":
```
init:
!importMod : extraItems
:init
```

## story scope:

The story scope is defined like this:
```
story:
// story commands
:story
```

The story scope is where you script the text adventure. Here everything the player interacts with, fights and picks up is defined.

Like the init scope, it has a starting and an ending keyword. 

Init exclusive commands are not available here. Only normal commands can be used, letting you display text, prompt a response from the player, and set up rooms and encounters.

## Commands:

The following commands are available in both the story scope and the init scope

These commands are what you will use to build your game's story and pacing.

### !displayText:

the displayText command is the most basic command available. It is used to display text in the terminal like this:

`!displayText : Hello world`

Terminal output: `Hello world`

The command is used to print one line of text, and printing several lines require several command calls like this:

```
!displayText : Hello
!displayText : World
```

Terminal output:
```
Hello
World
```

### !sleep:

The sleep command is used to put a delay between other commands you write.

For example if you want to print two lines in the terminal, but you want to give the player a chance to read the first one before the next one comes.

Here is an example:
```
story:
!displayText : This is a story about delay
!sleep : 2
!displayText : You just waited two seconds
:story
```
As you can see, you can decide how many seconds the sleep command delays your script.

This command also supports floating points, meaning `!sleep 0.3` is a viable command call.

### !scroll:

The scroll command lets you scroll text in the terminal up, leaving blank space before whatever is displayed next. 

The scroll command has a builtin delay between every line it scrolls, giving it a little more smooth feel.

Here is an example:

```
story:
!displayText : Hello
!scroll : 5
!displayText : World
:story
```

Terminal output:
```
Hello





World
```

As you can see, you can decide how many lines you want to scroll. 

This lets you do everything from adding one line between something, to scrolling everything off the screen before the story continues.

Some other commands available will automatically call this command with a set amount of lines that get scrolled

### !prompt:

The prompt command is used to tell the game engine that you want the player to interact with the world before going any further.

You can use this command to give players the chance to influence, interact with, and move around in your world.

Commands available for the player are defined in assets, mods and rooms that are imported, room commands only available to the player when they're in the corresponding room.

Example:
```
story:
!displayText : A prompt lets you interact with the world around you
!prompt : >> 
:story
```
Terminal output:
```
A prompt lets you interact with the world around you
>> 
```
You can define how the prompt will look, and can add custom text, or use different symbols. This means that the prompt command works like the displayText command, but it asks for input from the player afterwards.

Therefore, this is also valid:

Example:
```
story:
!displayText : Prompts can display anything in the terminal!
!prompt : Enter command: 
:story
```
Terminal output: 
```
Prompts can display anything in the terminal!
Enter command:
```

### !loadRoom:

loadroom is used to load a json defined room. These rooms are used to define what is around the player, 
and can contain items and commands.

Rooms are also where shops selling items to the player are defined.

The loadRoom command is written like this:

```
story:
!loadRoom : mainRoom
:story
```

This command will load a room with the name mainRoom.

When a room is loaded, all commands defined under "roomCommands" in the JSON file, will be executable after the player is prompted for a response.

To load another room later, simply just write the same command with the name of the new room.

### !displayFloorItems:

displayFloorItems is strongly connected to loadRoom, as it displays items on the floor, defined by the currently loaded room.

For this example, the loaded room JSON looks like this:

mainRoom.json:
```
{
    "floorItems": {
        "sword": {
            "ref": "assets/items",
            "amount": 1
        },
        "health potion": {
            "ref": "assets/items",
            "amount": 1
        },
        "torch": {
            "ref": "assets/items",
            "amount": 1
        }
}
```

To display the floor items, you write this in the .ta file:
```
story:
!loadRoom : mainRoom
!displayFloorItems : all
:story
```

Terminal output:
```
ii sword
ii health potion
ii torch
```

Currently displayFloorItems only has one mode: `all`, but more modes are coming, Like for example, only displaying weapons.

### !pickup

This command lets you select an item on the ground to add to the player's inventory. The command will also automatically delete it from the list of floor items.

This means that, like displayFloorItems, this command is dependant on the loadRoom command.

I will again use this JSON file as a room example:
mainRoom.json:
```
{
    "floorItems": {
        "sword": {
            "ref": "assets/items",
            "amount": 1
        },
        "health potion": {
            "ref": "assets/items",
            "amount": 1
        },
        "torch": {
            "ref": "assets/items",
            "amount": 1
        }
}
```

To pick up the sword for the player, write this in the .ta file:
```
story:
!loadRoom : mainRoom
!pickup : sword
:story
```

### !equipWeapon

This command is used to equip a weapon that the player has in his/her inventory

Let's look at an example:

In this example, the player's inventory looks like this:
```
inventory = {
    "weapons": ["sword"],
    "consumables": {},
    "equipment": [],
    "armor": []
    }
```

This is how you would equip the sword:
```
story:
!equipWeapon : sword
:story
```

Terminal output : 
```
equipped A shiny and pointy sword
```

The sword will now be used during combat until another weapon is equipped.

### !displayInventory

This command displays the items in the player's inventory

The list printed out by this command will change automatically when items are added to the player's inventory

The command takes one variable, that currently only can have one valid value: `all`. In the future, this variable will be used to decide what inventory items to display.

In this example, the player's inventory looks like this:
```
inventory = {
    "weapons": ["unarmed", "sword"],
    "consumables": {
        "health potion": {
            "amount": 2
        }
    },
    "equipment": [],
    "armor": []
    }
```

This is how you would write the script:
```
main:
!displayInventory : all
:main
```

Terminal output:
```
!! Weapons:
ii unarmed
ii sword
!! consumables:
ii 2 health potion/s
!! equipment:
```

!displayInventory can also show what weapon you have equipped. Because of this, running the previously explained command first would be reflected:

Example:
```
main:
!equipWeapon : sword
!displayInventory : all
:main
```

Terminal output:
```
!! Weapons:
ii unarmed
ii sword ** Equipped **
!! consumables:
ii 2 health potion/s
!! equipment:
```

### !spawnEnemy
!spawnEnemy spawns an enemy into the game for the player to fight against. 

Example:
```
story:
!spawnEnemy : skeleton
:story
```
Terminal output:
```
!! skeleton is attacking you
```

The command only displays the text, and adds the enemy to the next encounter, but does not begin combat. That is done with a seperate command called `!runCombat`

### !runCombat

!runCombat begins combat with all enemies spawned beforehand with `!spawnEnemy`

All combat actions are handled in the engine, so all you have to do to initialize a fight with a skeleton in your game is this:
```
story:
!displayEnemy : skeleton
!spawnEnemy : skeleton
!runCombat
:story
```
Terminal output:
```
                              _.--""-._
  .                         ."         ".
 / \    ,^.         /(     Y             |      )\
/   `---. |--'\    (  \__..'--   -   -- -'""-.-'  )
|        :|    `>   '.     l_..-------.._l      .'
|      __l;__ .'      "-.__.||_.-'v'-._||`"----"
 \  .-' | |  `              l._       _.'
  \/    | |                   l`^^'^^'j
        | |                _   \_____/     _
        j |               l `--__)-'(__.--' |
        | |               | /`---``-----'"1 |  ,-----.
        | |               )/  `--' '---'   \'-'  ___  `-.
        | |              //  `-'  '`----'  /  ,-'   I`.  \
      _ L |_            //  `-.-.'`-----' /  /  |   |  `. \
     '._' / \         _/(   `/   )- ---' ;  /__.J   L.__.\ :
      `._;/7(-.......'  /        ) (     |  |            | |
      `._;l _'--------_/        )-'/     :  |___.    _._./ ;
        | |                 .__ )-'\  __  \  \  I   1   / /
        `-'                /   `-\-(-'   \ \  `.|   | ,' /
                           \__  `-'    __/  `-. `---'',-'
                              )-._.-- (        `-----'
                             )(  l\ o ('..-.
                       _..--' _'-' '--'.-. |
                __,,-'' _,,-''            \ \
               f'. _,,-'                   \ \
              ()--  |                       \ \
                \.  |                       /  \
                  \ \                      |._  |
                   \ \                     |  ()|
                    \ \                     \  /
                     ) `-.                   | |
                    // .__)                  | |
                 _.//7'                      | |
               '---'                         j_| `
                                            (| |
                                             |  \
                                             |lllj
                                             |||||
!! skeleton is attacking you
```
After this terminal output, combat will automatically start, and your script will be resumed after combat is over.


### !displayEnemy

!displayEnemy displays the ascii stored in a .txt file referred to by the JSON file that defines the enemy.

This ascii can include any letters found on the keyboard. Support for further letters is sketchy, but experimentation is encouraged.

Here is an example displaying a skeleton after spawning it:
```
story:
!spawnEnemy : skeleton
!displayEnemy : skeleton
:story
```
Terminal output:
```
!! skeleton is attacking you
                              _.--""-._
  .                         ."         ".
 / \    ,^.         /(     Y             |      )\
/   `---. |--'\    (  \__..'--   -   -- -'""-.-'  )
|        :|    `>   '.     l_..-------.._l      .'
|      __l;__ .'      "-.__.||_.-'v'-._||`"----"
 \  .-' | |  `              l._       _.'
  \/    | |                   l`^^'^^'j
        | |                _   \_____/     _
        j |               l `--__)-'(__.--' |
        | |               | /`---``-----'"1 |  ,-----.
        | |               )/  `--' '---'   \'-'  ___  `-.
        | |              //  `-'  '`----'  /  ,-'   I`.  \
      _ L |_            //  `-.-.'`-----' /  /  |   |  `. \
     '._' / \         _/(   `/   )- ---' ;  /__.J   L.__.\ :
      `._;/7(-.......'  /        ) (     |  |            | |
      `._;l _'--------_/        )-'/     :  |___.    _._./ ;
        | |                 .__ )-'\  __  \  \  I   1   / /
        `-'                /   `-\-(-'   \ \  `.|   | ,' /
                           \__  `-'    __/  `-. `---'',-'
                              )-._.-- (        `-----'
                             )(  l\ o ('..-.
                       _..--' _'-' '--'.-. |
                __,,-'' _,,-''            \ \
               f'. _,,-'                   \ \
              ()--  |                       \ \
                \.  |                       /  \
                  \ \                      |._  |
                   \ \                     |  ()|
                    \ \                     \  /
                     ) `-.                   | |
                    // .__)                  | |
                 _.//7'                      | |
               '---'                         j_| `
                                            (| |
                                             |  \
                                             |lllj
                                             |||||
```

You might notice that the name of the enemy is defined for both commands. This is because the commands are independent. Meaning you could display an enemy that is not currently spawned.

### !giveItem

!giveItem can be used to give a player an item that isn't available to pick up in the currently loaded room.

For example if you want to have an NPC that gives your player an item

Example:
```
story:
!displayText : It's dangerous to go alone!
!displayText : Take this.
!giveItem : sword
:story
```
Terminal output:
```
It's dangerous to go alone!
Take this.
!! Picked up A shiny and pointy sword
```

You do not need to define what type of item it is. Just give the name of the item, and as long as some type of item with that name exists, it will be added to the player's inventory.

# More commands will be explained soon!