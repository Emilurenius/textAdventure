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
story:
Hello





World
```

As you can see, you can decide how many lines you want to scroll. 

This lets you do everything from adding one line between something, to scrolling everything off the screen before the story continues.

Some other commands available will automatically call this command with a set amount of lines that get scrolled

### !prompt:

The prompt command is used to tell the game engine that you want the player to interact with the world before going any further.

You cannot use this command to get an answer to a question, or let the player make a desicion.

Commands available for the player are defined in assets and mods that are imported. 

Example:
```
story:
!displayText : A prompt lets you interact with the world around you
!prompt : >> 
```
Terminal output:
```
A prompt lets you interact with the world around you
>> 
```
You can define how the prompt will look, and can add custom text, or use different symbols. This means that the prompt command works like the displayText command, but it asks for input from the player afterwards.

### !loadRoom:

loadroom is used to load a json defined room. These rooms are used 

# More commands will be explained soon!