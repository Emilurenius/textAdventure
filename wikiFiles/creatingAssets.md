# How to create assets / mods

Since the textAdventure engine is built to be as customizable as possible, all assets and mods are defined in JSON files.
This allows for infinite amounts of customization within the set boundaries of the game engine's capabilities.

This wiki page will go through everything an asset / mod can contain, and how to set it up.

## Difference between assets and mods:

Inside the JSON files there are no distinguishable features between assets and mods.
The difference is in where the files are found.

Assets are tied to the adventure they are created for, being found in the adventure's `assets` folder

Mods on the other hand can be used by any adventure if imported, and can be found in the game engine's `mods` folder

## Defining weapons:

Weapons have 5 attributes:
* desc
* damageDice
* hitDice
* damageType
* weight

### desc:

`desc` is the description of the weapon.

A description can be for example: `A shiny and pointy sword`

### damageDice:

`damageDice` is the diceroll that is made by the game engine when dealing damage with the weapon

The damagedice is written like this: `1d20`

This roll will be one 20 sided dice. As you can see, you can define both how many rolls to make, and how many sides the dice has.
There is no limiting factors on the types of dice you create. The two numbers can be whatever you want, as long as they are separated by a `d`

### hitDice:

`hitDice` works the same way as damageDice, but instead of dealing damage, it is used to check if the attack hits.

### damageType:

`damageType` defines what kind of damage the weapon does. Currently this is not used by the game engine in any way, so you could define this as anything you like.
When damagetypes are implemented, the types of damage supported by the game engine will be listed here.

### weight:

`weight` decides how heavy the weapon is. The weight is defined in grams

### Example:
```
{
    weapons: {
        sword: {
            "desc": "A shiny and pointy sword",
            "damageDice": "1d8",
            "hitDice" : "1d20",
            "damageType": "slashing",
            "weight": 800
        }
    }
}
```
In this exaple, I have defined a sword that deals `1d8` damage, with a `1d20` hit dice, doing `slashing` damage

## Defining consumables:

Consumables have 2 attributes:
* desc
* effect

### desc:

`desc` is the description of the consumable

A description can be for example: `A potion that gives +5 to health`

### effect:

`effect` tells the game engine what happens when this consumable is used.

## Example:
```
{
    "consumables": {
        "health potion" : {
            "desc": "A potion that gives +5 to health",
            "effect": "H+5"
        }
    }
}
```
In this example I have created a `health potion` that heals the player by `5 HP` upon consuming it.

Here is a list of available effects:
* H+`number` (Heals the player by the amount given in `number`)

## Defining equipment:

`!!NOTICE!!` Equipment is currently under development, and can't have any effect on gameplay yet.

Equipment have 2 attributes:
* desc
* effect

### desc:

`desc` is the description of the consumable

A description can be for example: `A bright torch. Might reveal things in dark places`

### effect:

`effect` tells the game engine what effect equipping the equipment has. For example a torch could light up things.

### Example:
```
{
    "equipment": {
        "torch": {
            "desc": "A bright torch. Might reveal things in dark places",
            "effect": "setAtt : light"
        }
    }
}
```
In this example I made a `torch` that creates an attribute called `light`

## Defining armor:

Armor have 3 attributes:
* desc
* ACmod
* weight

### desc:

`desc` is the description of the armor

A description can be for example: `A worn but sturdy set of leather armor`

### ACmod:

`ACmod` is the plus to armor class that the armor gives the player. This value is defined as a number, and can be negative

### weight:

`weight` decides how heavy the armor is. The weight is defined in grams

### Example:
```
{
    armor: {
        "leather armor": {
            "desc": "A worn but sturdy set of leather armor",
            "ACmod": 3,
            "weight": 3000
        },
    }
}
```
In this example I have created `leather armor` that gives `+3` to `armor class`, and weighs `3kg`

## Defining enemies:

Enemies have 5 attributes:
* desc
* ascii
* health
* AC
* weapon

### desc

`desc` is the description of the enemy

A description can be for example: `Impossible to reason with, these dark grey monsters are out for blood.`

### ascii

`ascii` defines the path to the ascii file containing an image of the enemy. This path starts at `adventureName/ascii/enemies`

This means that the path has to be continued fromt he `enemies` folder inside your adventure's `ascii` folder.

### health

`health` defines how many hit points the enemy has. This is how much damage the player has to deal to kill the enemy.

### AC

`AC` is the value that has to be matched by a weapon's `hit roll` to be able to hit the enemy.

### weapon

`weapon` is the weapon that your enemy uses. This weapon has to be defined either in the same asset / mod, or be imported with another asset / mod.

The name given here has to match the key value of the weapon where it is defined.

### Example:
```
{
    "enemies": {
        "dark orc": {
            "desc": "Impossible to reason with, these dark grey monsters are out for blood.",
            "ascii": "dark_orc",
            "health": 18,
            "AC": 9,
            "weapon": "club"
        }
    }
}
```
In this example I have created a `dark orc`, with it's ascii file located at `ascii/enemies/dark_orc`, `18 health`, an `AC of 9` and has a `club` for a weapon.

## Defining commands:

Commands have just one attribute: `a list`

A command is created by making the key value, what the player has to write in the terminal, and the list, the .ta scripting that happens when the command is issued.

Yes, I said .ta scripting. When creating a command, you use the same scripting as when you make the main.ta file for your adventure. This means you can make a command do anything.

Here is an example of a command:
```
{
    "commands": {
        "check ground": ["!displayFloorItems : all"]
    }
}
```
This command will be available to the player when a prompt command is run. The command displays all floor items in the currently loaded room

## Defining races:

Races have 5 attributes:
* health
* AC
* intelligence
* dexterity
* strength

All these attributes are modifier, modifying the standard values defined by the game engine.

All these values are normally set to 10. Both positive and negative values can be used to modify this standard value

### health:

`health` modifies the amount of damage that has to be dealt to the player before he/she dies. 

### AC:

`AC` modifies the armor class of the player character without armor on.

This can be used to make it easier or harder for the enemies to hit the player.

### intelligence:

`intelligence` modifies the intelligence of the player character

### dexterity:

`dexterity` modifies the dexterity of the player character

### strength:

`strength` modifies the strength of the player character

Strength is used as a modifier for damage dealt with weapons. `strength` gives a bonus to damage equal to `strength divided by 3`

### Example:
```
{
    Races: {
        "orc": {
            "health": 4,
            "AC": 2,
            "intelligence": -5,
            "dexterity": -4,
            "strength": 5
        }
    }
}
```
In this example I have created an orc with `+4 to health`, `+2 to AC`, `-5 to intelligence`, `-4 to dexterity`, and `+5 to strength`

# More asset types will be explained!