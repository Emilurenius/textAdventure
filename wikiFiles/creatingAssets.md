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

# More asset types will be explained!