import time, os, json, random, fnmatch, sys

dirPath = os.path.realpath(__file__).split("\\")
dirPath.pop()
temp = ""
for i in dirPath:
    temp += (f"{i}/")
dirPath = temp
gameOver = False
breakPrompt = False
selectedAdventure = ""
adventureProgress = 0
cursorMoved = False
weapons = {}
armors = {}
consumables = {}
equipment = {}
races = {}
equippedWeapon = ""
playerRace = False
adventureCommands = {}
enemies = {}
activeEnemies = {}

#Initialize dictionary variables for the player inventory.
inventory = {
    "weapons": [],
    "consumables": {},
    "equipment": [],
    "armor": []
    }
playerStats = {
    "health": 20,
    "maxHealth": 20,
    "AC": 10   
    }

#Empty the runtime folder
def clearRuntime():
    fileList = os.listdir(f"{dirPath}runtime")
    
    for f in fileList:
        os.remove(f"{dirPath}runtime/{f}")

class weapon():
    def __init__(self, name, desc, damageDice, hitDice, weight):
        self.name = name
        self.desc = desc
        self.damageDice = damageDice
        self.hitDice = hitDice
        self.weight = weight
        print(f"{self.name} loaded")

    def attack(self, target, mode="player"):

        if mode == "player":

            print(f"!! Rolling hit dice with {equippedWeapon}...")
            time.sleep(0.5)

            x = 0
            hitDice = 0
            while x < int(self.hitDice.split("d")[0]):
                hitDice += random.randint(1, int(self.hitDice.split("d")[1]))
                x += 1

            print(f"!! You rolled {hitDice}")
            time.sleep(0.5)

            if hitDice > int(enemies[target].AC):
                print("!! That hits!")
                time.sleep(1)
                
                print("!! Rolling damage dice...")
                time.sleep(0.5)

                x = 0
                damageDice = 0
                while x < int(self.damageDice.split("d")[0]):
                    damageDice += random.randint(1, int(self.damageDice.split("d")[1]))
                    x += 1

                modifier = int(races[playerRace].strength / 3)
                print(f"!! You rolled {damageDice} + {modifier}")
                time.sleep(0.5)
                return damageDice + modifier

            else:
                print("!! You miss!")
                time.sleep(1)
                return False

        elif mode == "enemy":
            
            print(f"!! {target} is attacking!")
            time.sleep(1)
            print(f"!! {target} is rolling hit dice with {self.name}...")
            time.sleep(1)
            x = 0
            hitDice = 0
            while x < int(self.hitDice.split("d")[0]):
                hitDice += random.randint(1, int(self.hitDice.split("d")[1]))
                x += 1
            print(f"!! {target} rolled {hitDice}")
            time.sleep(1)

            if hitDice > playerStats["AC"]:
                print("!! Ouch, that hits!")
                time.sleep(1)

                print(f"!! {target} is rolling damage dice...")
                time.sleep(1)
                x = 0
                damageDice = 0
                while x < int(self.damageDice.split("d")[0]):
                    damageDice += random.randint(1, int(self.damageDice.split("d")[1]))
                    x += 1
                print(f"!! {target} rolled {damageDice}")
                time.sleep(1)
                return damageDice
            
            else:
                print(f"!! {target} missed!")
                time.sleep(1)
                return False

class armor():
    def __init__(self, name, desc, ACmod, weight):
        self.name = name
        self.desc = desc,
        self.ACmod = ACmod,
        self.weight = weight
        print(f"{self.name} loaded")

class consumable():
    def __init__(self, name, desc, effect):
        self.name = name
        self.desc = desc
        self.effect = effect
        print(f"{self.name} loaded")

    def use(self):
        if self.effect.startswith("H"):
            
            global playerStats
            
            healthBuff = int(self.effect.split("+")[1])
            if playerStats["health"] + healthBuff <= playerStats["maxHealth"]:

                playerStats["health"] += healthBuff
                print(f"!! Used {self.name}.")
                time.sleep(1)
                print(f"!! Health now {playerStats['health']} HP")

            else:
                print("!! Cannot heal more. Health too high")
                time.sleep(1)
                return True # Return true to tell runCombat script to begin reprompt user
        
        return False # Tell runCombat it can keep going with the loop

class equipmentClass():
    def __init__(self, name, desc, effect):
        self.name = name
        self.desc = desc
        self.effect = effect
        print(f"{self.name} loaded")

class enemy():
    def __init__(self, name, desc, ascii, health, AC, weapon):
        self.name = name
        self.desc = desc
        self.ascii = ascii
        self.health = health
        self.AC = AC
        self.weapon = weapon
        print(f"{self.name} loaded")

    def displayAscii(self):
        printASCII(self.ascii)

    def attack(self):
        result = weapons[self.weapon].attack(self.name, "enemy")

        if result:
            playerStats["health"] -= result
            print(f"!! You now have {playerStats['health']} HP")

        if playerStats["health"] <= 0:
            print("!! You died!")
            global gameOver
            gameOver = True
            time.sleep(1)

class room():
    def __init__(self, name):
        self.name = name
        self.floorItems = {}
        self.commands = {}
        self.shopItems = {}

    def displayFloorItems(self, type):

        if type == "all":
            for item in self.floorItems.keys():
                print(f"ii {item}")
                time.sleep(0.5)

activeRoom = room("No room") # Initialize the active room as an empty room with no features

class race():
    def __init__(self, name, health, AC, intelligence, dexterity, strength):
        self.name = name
        self.health = 20 + health
        self.AC = 10 + AC
        self.intelligence = 10 + intelligence
        self.dexterity = 10 + dexterity
        self.strength = 10 + strength
        print(f"{self.name} loaded...")

#Main loop
def main():
    print("!! Text adventure Engine !!")
    time.sleep(1)
    scroll()
    time.sleep(0.5)
    
    clearRuntime()

    newLoad = False
    while newLoad != "new" and newLoad != "load":
        print("!! Please select an option to continue:")
        newLoad = input("new / load >> ")

    if newLoad == "new":
        printAdventures()
        
        adventure = False
        while not adventure:
            adventure = loadAdventure(input("Select one of the above adventures >> "))
        scroll()
        i = loadStory(adventure)
        scroll()
        i = runStory(adventure, i + 1)
        print("!! The story has come to an end")
        time.sleep(1)

    elif newLoad == "load":
        printSaves()
        adventure = False
        while not adventure:
            adventure = loadSave(input("!! Select a save file from the list >> "))
        runStory(adventure, adventureProgress)

#Handle saving of non-runtime things
def saveGame(saveName, supressPrompts=False):

    saveData = {
        "selectedAdventure": selectedAdventure,
        "storyPos": adventureProgress,
        "inventory": inventory,
        "room": {
            "name": activeRoom.name,
            "floorItems": activeRoom.floorItems,
            "roomCommands": activeRoom.commands
        },
        "equippedWeapon": equippedWeapon,
        "playerRace": playerRace,
        "activeEnemies": activeEnemies
    }

    with open(f"{dirPath}saves/{saveName}.json", "w") as outFile:
        json.dump(saveData, outFile, indent=4)

    if not supressPrompts:
        print(f"Saved current progress as {saveName}")

#Game over
def endGame():
    global gameOver
    gameOver = True

#Move the line you're running from to another line
def setCursor(cursorPos):
    global cursorMoved
    global adventureProgress
    cursorMoved = True

    if cursorPos.isnumeric():
        adventureProgress = int(cursorPos)
    else:
        adventureFile = loadAdventure(selectedAdventure)
        i = 0
        for line in adventureFile:
            if line.startswith("#") and cursorPos == line.replace("#", ""):
                adventureProgress = i
            i += 1

#Remove file extension
def removeFileExtention(file, extention):
    return file.replace(extention, "")

#Print text
def displayText(text):
    print(text)

#Print Ascii art
def printASCII(filePath):
    with open(f"{dirPath}adventures/{selectedAdventure}/ascii/{filePath}.txt") as TXT:
        print(TXT.read())

#Cancel a prompt to the player
def setBreakPrompt():
    global breakPrompt
    breakPrompt = True

#Get user input
def prompt(text):
    global breakPrompt

    if breakPrompt:
        breakPrompt = False
        return

    def runPrompt(k, v):
        multiWordFill = False
        splitCommand = k.split(" ")
        
        if len(INsplit) < len(splitCommand):
            return
        
        if "<?" in k:
            
            i = 0
            variableIndex = 0
            for x in splitCommand:
                if INsplit[i] == x:
                    commandFound = True
                elif x == "<?>":
                    variableIndex = i
                    commandFound = True
                elif x == "<?":
                    if k == "pick up <?":
                        print("Converted variable space to variable")
                    variableIndex = i
                    commandFound = True
                    multiWordFill = True
                else:
                    commandFound = False
                    break
                i += 1

            if commandFound and multiWordFill == False:

                for x in v:
                    if "<?>" in x:
                        command = x.replace("<?>", INsplit[variableIndex])
                    else:
                        command = x

                    if command.startswith("!"):
                        runCommand(command)

            elif commandFound and multiWordFill:
                i = variableIndex
                multiWord = ""
                while i < len(INsplit):
                    multiWord += INsplit[i] + " "
                    i += 1
                multiWord = multiWord[:-1]
                
                for x in v:
                    if "<?" in x:
                        command = x.replace("<?", multiWord)
                    else:
                        command = x
                    if command.startswith("!"):
                        runCommand(command)

        else:
            i = 0
            commandFound = True
            for x in INsplit:
                if x == splitCommand[i]:
                    commandFound = True
                else:
                    commandFound = False
                    break
                i += 1
            
            if commandFound:
                for x in v:
                    if x.startswith("!"):
                        runCommand(x)
    
    IN = input(text)

    if not IN:
        return

    INsplit = IN.split(" ")

    if IN == "help":
        print("!! Available commands:\n")

        for command in adventureCommands.keys():
            time.sleep(0.5)
            print(f">> {command}")
        for command in activeRoom.commands.keys():
            time.sleep(0.5)
            print(f">> {command}")
    else:
        for k, v in adventureCommands.items():
            runPrompt(k, v)

        for k, v in activeRoom.commands.items():
            runPrompt(k, v)

    prompt(text)

#Wait
def sleep(secs):
    time.sleep(float(secs))

#Print empty lines
def scroll(lines=5, delay=0.1):
    i = 0
    while i < int(lines):
        print("")
        i += 1
        time.sleep(delay)

#Interpret a line in the script file.
def getCommand(commandString):
    commandString = commandString[1:]
    commandString = commandString.split(" //")[0]
    return commandString.split(" : ")

#Handle commands in the script
def runCommand(command):
    if command.startswith("!") and " : " not in command: # Seperate handler for commands without variables
        command = command.replace("!", "")
        command = commands.get(command, None)
        if command:
            command()

    elif command.startswith("!"): # Seperate handler for commands with variables
        commandList = getCommand(command)
        command = commands.get(commandList[0], None)
        if command:
            command(commandList[1])

    elif command.startswith("-"): # Seperate handler for supressed commands (Command will not print anything in the terminal)
        commandList = getCommand(command)
        command = commands.get(commandList[0], None)
        if command:
            command(commandList[1], True)

#Display available adventures to the player
def printAdventures():
    print("Loading adventures...")
    time.sleep(0.5)
    adventures = os.listdir(f"{dirPath}adventures")

    for i in adventures:
        print(f"|| {i}")
        time.sleep(0.1)

#Display available savefiles to the player
def printSaves():
    print("Loading saves...")
    time.sleep(0.5)
    saves = os.listdir(f"{dirPath}saves")

    for i in saves:
        print(f"|| {removeFileExtention(i, '.json')}")
        time.sleep(0.1)

#Load adventure from assets folder
def loadAdventure(adventure):
    global selectedAdventure
    selectedAdventure = adventure
    try:
        with open(f"{dirPath}adventures/{adventure}/main.ta") as f:
            data = f.read().splitlines()
        return data
    except:
        return False

#Load save into memory and runtime.
def loadSave(saveName):
    try:
        save = False
        with open(f"{dirPath}saves/{saveName}.json") as f:
            save = json.load(f)
        adventure = loadAdventure(save["selectedAdventure"])
        global inventory
        global equippedWeapon
        global playerRace
        global activeEnemies
        global activeRoom
        global adventureProgress
        inventory = save["inventory"]
        equippedWeapon = save["equippedWeapon"]
        playerRace = save["playerRace"]
        activeEnemies = save["activeEnemies"]
        activeRoom = room(save["room"]["name"])
        if "floorItems" in save["room"]:
            activeRoom.floorItems = save["room"]["floorItems"]
        if "roomCommands" in save["room"]:
            activeRoom.commands = save["room"]["roomCommands"]
        adventureProgress = int(save["storyPos"])
        i = 0
        while True:
            if adventure[i] == "init:":
                print("Initializing...")
                runInit(adventure, i + 1)
                break
            i += 1

        return adventure
    except:
        return False

#Run commands from the story scope.
def loadStory(story, i=0):
    while i < len(story):
        if story[i] == "init:":
            print("Initializing...")
            i = runInit(story, i + 1)

        elif story[i] == "story:":
            return i

        i += 1

#Run commands from the init scope.
def runInit(story, i):
    while True:
        if story[i].startswith("!"):
            commandList = getCommand(story[i])
            command = initCommands.get(commandList[0], None) or commands.get(commandList[0], None)
            if command:
                command(commandList[1])
                time.sleep(0.3)

        elif story[i] == ":init":
            print("Initialization complete...")
            selectRace()
            return i

        i += 1

#Let the player pick a race to play as
def selectRace():
    global playerRace
    if playerRace:
        return

    scroll()
    global races
    if races:
        print("!! Please select a race: ")
        counter = 0
        for x in races.keys():
            print(f"{counter} {x}")
            time.sleep(0.5)
            counter += 1
        
        IN = ""
        while not IN.isnumeric() or playerRace == False:
            IN = input(">> ")

            keysList = []
            for x in races.keys():
                keysList.append(x)
            if int(IN) < len(keysList):
                playerRace = races[keysList[int(IN)]].name
            print(playerRace)

    else:
        print("There are no races to use")
    time.sleep(2)

#Load assets from assets
def loadAssetData(data):
    if "weapons" in data:
        print("Loading weapons...")
        for k, v in data["weapons"].items():
            weapons[k] = weapon(k, v["desc"], v["damageDice"], v["hitDice"], v["weight"])
    
    if "consumables" in data:
        print("Loading consumables...")
        for k, v in data["consumables"].items():
            consumables[k] = consumable(k, v["desc"], v["effect"])

    if "equipment" in data:
        print("Loading equipment...")
        for k, v in data["equipment"].items():
            equipment[k] = equipmentClass(k, v["desc"], v["effect"])

    if "commands" in data:
        print("Loading commands...")
        for k, v in data["commands"].items():
            adventureCommands[k] = v
            print(k)

    if "enemies" in data:
        print("Loading enemies...")
        for k, v in data["enemies"].items():
            enemies[k] = enemy(k, v["desc"], v["ascii"], v["health"], v["AC"], v["weapon"])
    
    if "races" in data:
        print("Loading races...")
        for k, v in data["races"].items():
            races[k] = race(k, v["health"], v["AC"], v["intelligence"], v["dexterity"], v["strength"])

    if "armor" in data:
        print("Loading armor...")
        for k, v in data["armor"].items():
            armors[k] = armor(k, v["desc"], v["ACmod"], v["weight"])

#Load a room from runtime, or from assets if it's not available.
def loadRoom(selectedRoom):
    global activeRoom
    #unless the player isnt in a room, save the previous room to the runtime
    if activeRoom.name != "No room": 
        roomData = {
            "floorItems": activeRoom.floorItems,
            "roomCommands": activeRoom.commands
        }

        with open(f"{dirPath}runtime/{activeRoom.name}.json", "w") as outFile:
            json.dump(roomData, outFile, indent=4)

    #If the room exists in the runtime, load that, else load from assets.
    
    if os.path.exists(f"{dirPath}runtime/{selectedRoom}.json"):
        with open(f"{dirPath}runtime/{selectedRoom}.json", "r") as JSON:
            data = json.load(JSON)

    else:
        with open(f"{dirPath}adventures/{selectedAdventure}/rooms/{selectedRoom}.json") as JSON:
            data = json.load(JSON)

    
    activeRoom = room(selectedRoom)

    if "floorItems" in data:
        activeRoom.floorItems = data["floorItems"]
    if "roomCommands" in data:
        activeRoom.commands = data["roomCommands"]
    if "shopItems" in data:
        activeRoom.shopItems = data["shopItems"]

#Display items that are on the floor.
def displayFloorItems(type):
    activeRoom.displayFloorItems(type=type)

#Importing mods as JSON and return it as a dictionary.
def loadMod(modName):
    print("Importing mods...")
    with open(f"{dirPath}mods/{modName}.json") as JSON:
        data = json.load(JSON)

    loadAssetData(data)

#Importing assets as JSON and return it as a dictionary.
def loadAsset(assetName):
    print("Importing asset...")
    with open(f"{dirPath}adventures/{selectedAdventure}/assets/{assetName}.json") as JSON:
        data = json.load(JSON)

    loadAssetData(data)

#Run the player through the story
def runStory(story, i):
    global adventureProgress 
    global cursorMoved
    while True:
        

        if gameOver:
            return i
        elif story[i] == ":story":
            return i

        runCommand(story[i])


        if cursorMoved:
            i = adventureProgress
            cursorMoved = False
        else:
            i += 1
            adventureProgress = i

#Handle the playing picking up items
def pickup(item, supressPrompts=False):

    #If its a weapon that exists, add it to the player's weapon list.
    if item in weapons.keys() and item in activeRoom.floorItems.keys():
        if item in inventory["weapons"]:
            print(f"!! You already have that, you don't need another one.")
        else:
            if not supressPrompts:
                print(f"!! Picked up {weapons[item].desc}")
            inventory["weapons"].append(item)
            activeRoom.floorItems[item]["amount"] -= 1

    #If its a consumable that exists, add it to the player's consumable list.
    elif item in consumables.keys() and item in activeRoom.floorItems.keys():
        if not supressPrompts:
            print(f"!! Picked up {consumables[item].desc}")

        if item in inventory["consumables"].keys():
            inventory["consumables"][item]["amount"] += 1
        else:
            inventory["consumables"][item] = {
                "amount": 1
            }
        time.sleep(0.5)
        if not supressPrompts:
            print(f"!! You now have {inventory['consumables'][item]['amount']} {item}s")
        activeRoom.floorItems[item]["amount"] -= 1

    #If its an equipment that exists, add it to the player's equipment list.
    elif item in equipment.keys() and item not in inventory["equipment"] and item in activeRoom.floorItems.keys():
        if not supressPrompts:
            print(f"!! Picked up {equipment[item].desc}")

        inventory["equipment"].append(item)
        activeRoom.floorItems[item]["amount"] -= 1

    #If its an armor that exists, add it to the player's armor list.
    elif item in armors.keys() and item in activeRoom.floorItems.keys():
        if not supressPrompts:
            print(f"!! Picked up {armors[item].desc}")

        inventory["armors"].append(item)
        activeRoom.floorItems[item]["amount"] -= 1

    #If nothing seems to work, tell the player it can't
    else:
        if not supressPrompts:
            print(f"!! Cannot pick up {item}")

    #Delete the item key if amount is 0
    if item in activeRoom.floorItems.keys() and activeRoom.floorItems[item]["amount"] <= 0:
        del activeRoom.floorItems[item]

#Handle the player equipping items
def equipWeapon(weapon, supressPrompts=False):
    if weapon in inventory["weapons"]:
        global equippedWeapon
        equippedWeapon = weapon
        if not supressPrompts:
            print(f"!! {weapon} equipped")

    else:
        print("!! You do not have a weapon with that name")

#Display the player's inventory
def displayInventory(type):
    print("!! Opening inventory...")
    scroll()
    print("!! Weapons:")
    time.sleep(0.5)
    for weapon in inventory["weapons"]:
        if weapon == equippedWeapon:
            print(f"ii {weapon}  ** Equipped **")
        else:
            print(f"ii {weapon}")
        time.sleep(0.5)
    print("!! consumables:")
    time.sleep(0.5)
    for consumable in inventory["consumables"].keys():
        print(f"ii {inventory['consumables'][consumable]['amount']} {consumable}/s")
        time.sleep(0.5)
    print("!! equipment:")
    time.sleep(0.5)
    for equipment in inventory["equipment"]:
        print(f"ii {equipment}")
        time.sleep(0.5)

#Load Ascii art of enemy
def displayEnemy(enemy):
    enemies[enemy].displayAscii()

#Spawn an enemy as part of the next combat sequence.
def spawnEnemy(enemy, supressPrompts=False):
    if enemy in enemies.keys():
        global activeEnemies
        activeEnemies[enemy] = {
            "health": enemies[enemy].health
        }
        
        if not supressPrompts:
            print(f"!! {enemy} is attacking you")
        time.sleep(1)

#Add an item to the player's inventory.
def giveItem(item):
    itemType = item.split(" ")[0]
    itemName = item.split(" ")
    itemName.pop(0)
    itemName = " ".join(itemName)
    global inventory

    if itemType == "weapon" and itemName in weapons.keys():
        inventory["weapons"].append(itemName)
    else:
        print("!! Sorry, that item can't be given")

#Start a combat sequence.
def runCombat():
    global activeEnemies

    if len(activeEnemies) < 1:
        return

    while not gameOver:

        scroll()
        time.sleep(0.5)
        print("!! Please select an action:")
        time.sleep(1)
        print("-- attack")
        time.sleep(0.5)
        print("-- use <consumable name>")
        time.sleep(0.5)
        print("-- flee")
        time.sleep(0.5)
        IN = input(">> ")

        if fnmatch.fnmatch(IN, "attack *"):
            enemyName = IN.split(" ")
            del enemyName[0]
            enemyName = " ".join(enemyName)
            print(enemyName)
            result = weapons[equippedWeapon].attack(enemyName)

            if result:
                activeEnemies[enemyName]['health'] -= result
                print(f"!! {enemyName}'s health is now {activeEnemies[enemyName]['health']}")
                time.sleep(1)

                if activeEnemies[enemyName]['health'] <= 0:
                    del activeEnemies[enemyName]

        elif fnmatch.fnmatch(IN, "use *"):
            useCommand = IN.split(" ")

            del useCommand[0]
            consumableName = " ".join(useCommand)

            if consumableName in inventory["consumables"].keys():
                if inventory["consumables"][consumableName]["amount"] > 0:
                    if consumables[consumableName].use():
                        continue
                else:
                    print("!! You do not have more of that consumable")
                    time.sleep(1)
                    continue
            else:
                print("!! You do not have that consumable")
                time.sleep(1)
                continue

            time.sleep(2)
        
        elif IN == "flee":
            print("!! You attempt to flee...")
            time.sleep(1)
            fleeCheck = random.randint(0, 1)
            if fleeCheck:
                print("!! You got away!")
                time.sleep(0.5)
                return
            else:
                print(f"!! The enemies caught up to you")
                time.sleep(0.5)

        else:
            continue # Prompt a response from the user again, if no action was done
        
        if len(activeEnemies) < 1:
            time.sleep(0.5)
            scroll()
            time.sleep(0.1)
            print(f"!! You have defeated all the enemies")
            time.sleep(0.5)
            return

        for k, v in activeEnemies.items():
            enemies[k].attack()

#Display a shop's items and prices.
def checkShopItems(type):
        if type == "all":
            for key, value in activeRoom.shopItems.items():
                print(f"|| {key} : {value['price']} gold")

#Defining script commands for the init scope.
initCommands = {
    "importMod": loadMod,
    "importAsset": loadAsset
    }

#Defining script commands for the story scope.
commands = {
    "displayText": displayText,
    "sleep": sleep,
    "scroll": scroll,
    "prompt": prompt,
    "loadRoom": loadRoom,
    "displayFloorItems": displayFloorItems,
    "pickup": pickup,
    "equipWeapon": equipWeapon,
    "displayInventory": displayInventory,
    "displayEnemy": displayEnemy,
    "spawnEnemy": spawnEnemy,
    "runCombat": runCombat,
    "giveItem": giveItem,
    "printASCII": printASCII,
    "saveGame": saveGame,
    "endGame": endGame,
    "setCursor": setCursor,
    "breakPrompt": setBreakPrompt,
    "checkShopItems": checkShopItems
    }

#Testing whether the file is ran or imported
if __name__ == "__main__":
    main()