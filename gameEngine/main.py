import time, os, json, random, fnmatch, sys, re
from pick import pick
from benedict import benedict

#region custom errors
class noStringError(Exception):
    pass
#endregion custom errors

#region Initialize global variables
dirPath = os.path.realpath(__file__)
if '\\' in dirPath:
    dirPath = dirPath.split('\\')
elif '/' in dirPath:
    dirPath = dirPath.split('/')
dirPath.pop()
temp = ""
for i in dirPath:
    temp += (f"{i}/")
dirPath = temp

runtime = {
    'dirPath': dirPath,
    'gameOver': False,
    'breakPlayerAction': False,
    'selectedAdventure': '',
    'adventureProgress': 0,
    'cursorMoved': False,
    'equippedWeapon': '',
    'playerRace': False,
    'activeEnemies': {},
    'cosmeticChoice': False,
    'codeVars': {},
    'textScroll': {
        'active': False,
        'delay': 0.1
    }
}

dirPath = None
temp = None

assetData = {
    'weapons': {},
    'armors': {},
    'consumables': {},
    'equipment': {},
    'races': {},
    'adventureCommands': {},
    'shopCommands': {},
    'enemies': {},
    'cosmetics': {},
    'characters': {}
}

#Initialize dictionary variables for the player inventory.
inventory = {
    "weapons": [],
    "consumables": {},
    "equipment": [],
    "armor": [],
    "gold": 0
    }
playerStats = {
    "health": 20,
    "maxHealth": 20,
    "AC": 10   
    }
#endregion Initialize global variables

#Empty the runtime folder
def clearRuntime():
    #print(runtime)
    fileList = os.listdir(f"{runtime['dirPath']}runtime")
    
    for f in fileList:
        if f != ".gitignore":
            os.remove(f"{runtime['dirPath']}runtime/{f}")

#region gameEngine classes

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

            print(f"!! Rolling hit dice with {runtime['equippedWeapon']}...")
            time.sleep(0.5)

            x = 0
            hitDice = 0
            while x < int(self.hitDice.split("d")[0]):
                hitDice += random.randint(1, int(self.hitDice.split("d")[1]))
                x += 1

            print(f"!! You rolled {hitDice}")
            time.sleep(0.5)

            if hitDice > int(assetData["enemies"][target].AC):
                print("!! That hits!")
                time.sleep(1)
                
                print("!! Rolling damage dice...")
                time.sleep(0.5)

                x = 0
                damageDice = 0
                while x < int(self.damageDice.split("d")[0]):
                    damageDice += random.randint(1, int(self.damageDice.split("d")[1]))
                    x += 1

                modifier = int(assetData["races"][runtime['playerRace']].strength / 3)
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
                return True # Return true to tell runCombat script to begin reprompting user
        
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
        printASCII(f'enemies/{self.ascii}')

    def attack(self):
        result = assetData['weapons'][self.weapon].attack(self.name, "enemy")

        if result:
            playerStats["health"] -= result
            print(f"!! You now have {playerStats['health']} HP")

        if playerStats["health"] <= 0:
            print("!! You died!")
            global runtime
            runtime['gameOver'] = True
            time.sleep(1)

class room():
    def __init__(self, name):
        self.name = name
        self.floorItems = {}
        self.commands = {}
        self.shopItems = {}
        self.lookAroundEvent = []
        self.investigateables = {}
        self.characters = []

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

#endregion gameEngine classes

#Main loop
def main():
    print("!! Text adventure Engine !!")
    time.sleep(1)
    
    clearRuntime()

    newLoad, index = menuSelect('Please select an option to continue:', ['new', 'load'])

    if newLoad == "new":
        adventures = os.listdir(f"{runtime['dirPath']}adventures")
        

        option, index = menuSelect('Select an adventure:', adventures)
        adventure = loadAdventure(option)
        i = loadStory(adventure)
        i = runStory(adventure, i + 1)
        print("!! The story has come to an end")
        time.sleep(1)

    elif newLoad == "load":
        saves = os.listdir(f"{runtime['dirPath']}saves")
        options = []
        for x in saves:
            if x.endswith('.json'):
                options.append(x.replace('.json', ''))
        option, index = menuSelect('What save do you wish to load?', options)
        adventure = loadSave(option)
        runStory(adventure, runtime['adventureProgress'])

#region internal functions

#Remove file extension
def removeFileExtention(file, extention):
    return file.replace(extention, "")

#Display available adventures to the player
def printAdventures():
    print("Loading adventures...")
    time.sleep(0.5)
    adventures = os.listdir(f"{runtime['dirPath']}adventures")

    for i in adventures:
        print(f"|| {i}")
        time.sleep(0.1)

#Load adventure from assets folder
def loadAdventure(adventure):
    global runtime
    runtime['selectedAdventure'] = adventure
    try:
        with open(f"{runtime['dirPath']}adventures/{adventure}/main.ta") as f:
            data = f.read().splitlines()
            # print('Code before minifying:\n')
            # for x in data:
            #     print(x)
            # print()

    except:
        return False
    

    i = 0
    while i < len(data): # Minify code
        if data[i] == '':
            print('Empty line found')
            del data[i]
            continue
        data[i] = data[i].lstrip()

        comments = re.findall('//.*', data[i])
        for x in comments:
            data[i] = data[i].replace(x, '')
        i += 1

    # print('Code after minifying:\n')
    # for x in data:
    #     print(x)
    # print()

    return data

# Split up a command into command type, and variables. Is called by runCommand when needed.
def getCommand(commandString):
    commandString = commandString[1:]
    commandString = commandString.split(" //")[0]
    return commandString.split(" : ")

def getString(text):
    foundText = re.findall('".*"', text)
    if not foundText:
        foundText = re.findall("'.*'", text)

    if foundText:
        foundText = foundText[0]
        if foundText.startswith('"'):
            foundText = foundText.replace('"', '')
        else:
            foundText = foundText.replace("'", '')
        return foundText
    else:
        raise noStringError(f'No string given at line {runtime["adventureProgress"]}')

#Handle commands in the script
def runCommand(command, init=False):

    inlineStrings = re.findall('{\w*}', command)
    for x in inlineStrings:
        strippedX = x.replace('{', '')
        strippedX = strippedX.replace('}', '')
        if strippedX in runtime['codeVars'].keys():
            #print(runtime['codeVars'][strippedX])
            command = command.replace(x, str(runtime['codeVars'][strippedX]['val']))

    if command.startswith("!") and " : " not in command: # Seperate handler for commands without variables
        command = command.replace("!", "")
        command = commands.get(command)
        if command:
            command()
        elif init:
            command = initCommands.get(commandList[0])
            if command:
                command()

    elif command.startswith("!"): # Seperate handler for commands with variables
        commandList = getCommand(command)
        command = commands.get(commandList[0])
        if command:
            command(commandList[1])
        elif init:
            command = initCommands.get(commandList[0])
            if command:
                command(commandList[1])

    elif command.startswith("-"): # Seperate handler for supressed commands (Command will not print anything in the terminal)
        commandList = getCommand(command)
        command = commands.get(commandList[0])
        if command:
            command(commandList[1], True)
        elif init:
            command = initCommands.get(commandList[0])
            if command:
                command(commandList[1], True)

#Load save into memory and runtime.
def loadSave(saveName):
    global runtime
    global activeRoom
    global inventory
    save = False
    with open(f"{runtime['dirPath']}saves/{saveName}.json") as f:
        save = json.load(f)
    adventure = loadAdventure(save["selectedAdventure"])
    runtime = save['runtimeRam']
    inventory = save["inventory"]
    activeRoom = room(save["room"]["name"])
    if "floorItems" in save["room"]:
        activeRoom.floorItems = save["room"]["floorItems"]
    if "roomCommands" in save["room"]:
        activeRoom.commands = save["room"]["roomCommands"]
    if 'shopItems' in save['room']:
        activeRoom.shopItems = save['room']['shopItems']
    if 'lookAroundEvent' in save['room']:
        activeRoom.lookAroundEvent = save['room']['lookAroundEvent']
    if 'investigateables' in save['room']:
        activeRoom.investigateables = save['room']['investigateables']
    if 'characters' in save['room']:
        activeRoom.characters = save['room']['characters']

    if 'runtime' in save:
        for k, v in save['runtime'].items():
            with open(f"{runtime['dirPath']}runtime/{k}.json", "w") as outFile:
                json.dump(v, outFile, indent=4)

    i = 0
    while True:
        if adventure[i] == "init:":
            print("Initializing...")
            runInit(adventure, i + 1)
            break
        i += 1

    return adventure

#Run commands from the story scope.
def loadStory(story, i=0):
    while i < len(story):
        if story[i] == "init:":
            print("Initializing...")
            i = runInit(story, i + 1)
            scroll()

        elif story[i] == "story:":
            return i

        i += 1

#Run commands from the init scope.
def runInit(story, i):
    while True:
        if story[i].startswith("!") or story[i].startswith("-"):
            runCommand(story[i], init=True)
            # commandList = getCommand(story[i])
            # command = initCommands.get(commandList[0]) or commands.get(commandList[0])
            # if command:
            #     command(commandList[1])
            #     time.sleep(0.3)

        elif story[i] == ":init":
            print("Initialization complete...")
            selectRace()
            chooseCosmetics()
            return i

        i += 1

#Let the player pick a race to play as
def selectRace():
    global runtime
    if runtime['playerRace']:
        return

    scroll()
    global assetData
    if assetData["races"]:
        #hvorfor eksisterer Cemil? Ingen vet. (The fuck?)
        print(assetData['races'].keys())
        runtime['playerRace'], index = menuSelect('Please select a race:', list(assetData['races'].keys()))

    else:
        print("There are no races to use")

def chooseCosmetics():
    global runtime
    if runtime['cosmeticChoice']:
        return
    
    scroll()
    global assetData
    if assetData["cosmetics"]:
        print("!! How do your eyes look: ")
        counter = 0 
        for x in assetData["cosmetics"]["eyes"].keys(): 
            print(f"{counter} {x}")
            time.sleep(0.5)
            counter += 1

        IN = ""
        while not IN.isnumeric() or runtime['cosmeticChoice'] == False:
            IN = input(">> ")

            keysList = []
            for x in assetData["cosmetics"].keys():
                keysList.append(x)
            if int(IN) < len(keysList):
                runtime['cosmeticChoice'] = assetData["cosmetics"][keysList[int(IN)]].name
            print(runtime['cosmeticChoice'])
    
    else:
        print("There are no cosmetic choices")

#Load assets from assets
def loadAssetData(data):
    if "weapons" in data:
        print("Loading weapons...")
        for k, v in data["weapons"].items():
            assetData['weapons'][k] = weapon(k, v["desc"], v["damageDice"], v["hitDice"], v["weight"])
    
    if "consumables" in data:
        print("Loading consumables...")
        for k, v in data["consumables"].items():
            assetData["consumables"][k] = consumable(k, v["desc"], v["effect"])

    if "equipment" in data:
        print("Loading equipment...")
        for k, v in data["equipment"].items():
            assetData["equipment"][k] = equipmentClass(k, v["desc"], v["effect"])

    if "commands" in data:
        print("Loading commands...")
        for k, v in data["commands"].items():
            assetData["adventureCommands"][k] = v
            print(k)

    if "enemies" in data:
        print("Loading enemies...")
        for k, v in data["enemies"].items():
            assetData["enemies"][k] = enemy(k, v["desc"], v["ascii"], v["health"], v["AC"], v["weapon"])
    
    if "races" in data:
        print("Loading races...")
        for k, v in data["races"].items():
            assetData["races"][k] = race(k, v["health"], v["AC"], v["intelligence"], v["dexterity"], v["strength"])

    if "cosmeticTraits" in data: #cemil er en bitch. Ingen liker han. Bøg er det han er.
        print("Loading cosmetics...")

    if "armor" in data:
        print("Loading armor...")
        for k, v in data["armor"].items():
            assetData["armors"][k] = armor(k, v["desc"], v["ACmod"], v["weight"])

    if "shopCommands" in data:
        print("Loading shop commands")
        for k, v in data["shopCommands"].items():
            assetData["shopCommands"][k] = v
            print(k)

    if 'characters' in data:
        print('Loading characters')
        for k, v in data['characters'].items():
            assetData['characters'][k] = v
            print(k)

#Run the player through the story
def runStory(story, i):
    global runtime 
    global runtime
    while True:
        

        if runtime['gameOver']:
            return i
        elif story[i] == ":story":
            return i

        runCommand(story[i])


        if runtime['cursorMoved']:
            i = runtime['adventureProgress']
            runtime['cursorMoved'] = False
        else:
            i += 1
            runtime['adventureProgress'] = i

def menuSelect(title, options):
    option, index = pick(options, title, indicator='=>', default_index=0)

    return option, index

#endregion internal functions

#region gameEngine functions

#Importing mods as JSON and return it as a dictionary.
def loadMod(modName):
    print("Importing mods...")
    with open(f"{runtime['dirPath']}mods/{modName}.json") as JSON:
        data = json.load(JSON)

    loadAssetData(data)

#Importing assets as JSON and return it as a dictionary.
def loadAsset(assetName):
    print("Importing asset...")
    with open(f"{runtime['dirPath']}adventures/{runtime['selectedAdventure']}/assets/{assetName}.json") as JSON:
        data = json.load(JSON)

    loadAssetData(data)

#Handle saving of non-runtime things
def saveGame(saveName, supressPrints=False):

    runtimeFiles = os.listdir(f"{runtime['dirPath']}runtime")
    runtimeFiles = filter(lambda x: x.endswith('.json'), runtimeFiles)

    runtimeData = {}
    for file in runtimeFiles:
        with open(f"{runtime['dirPath']}runtime/{file}") as JSON:
            runtimeData[file] = json.load(JSON)
    saveData = {
        "selectedAdventure": runtime['selectedAdventure'],
        "storyPos": runtime['adventureProgress'],
        "inventory": inventory,
        "room": {
            "name": activeRoom.name,
            "floorItems": activeRoom.floorItems,
            "roomCommands": activeRoom.commands,
            'shopItems': activeRoom.shopItems,
            'lookAroundEvent': activeRoom.lookAroundEvent,
            'investigateables': activeRoom.investigateables,
            'characters': activeRoom.characters,
            'connectedRooms': activeRoom.connectedRooms
        },
        "runtime": runtimeData,
        'runtimeRam': runtime
    }

    with open(f"{runtime['dirPath']}saves/{saveName}.json", "w") as outFile:
        json.dump(saveData, outFile, indent=4)

    if not supressPrints:
        print(f"Saved current progress as {saveName}")

#Game over
def endGame():
    global runtime
    runtime['gameOver'] = True

#Move the line you're running from to another line
def setCursor(cursorPos):
    global runtime
    runtime['cursorMoved'] = True

    if cursorPos.isnumeric():
        runtime['adventureProgress'] = int(cursorPos)
    else:
        adventureFile = loadAdventure(runtime['selectedAdventure'])
        i = 0
        for line in adventureFile:
            if line.startswith("#") and cursorPos == line.replace("#", ""):
                runtime['adventureProgress'] = i
            i += 1

#Print text
def displayText(text):
    if runtime['textScroll']['active']:
        chars = list(getString(text))
        outString = ' '
        for char in chars:
            outString = outString + char
            print(outString, end='\r')
            time.sleep(runtime['textScroll']['delay'])
        print('')
    else:
        print(getString(text))

#Print Ascii art
def printASCII(filePath):
    with open(f"{runtime['dirPath']}adventures/{runtime['selectedAdventure']}/ascii/{filePath}.txt") as TXT:
        print(TXT.read())

# Stop playerAction from asking for more input once
def setbreakPlayerAction():
    global runtime
    runtime['breakPlayerAction'] = True

#Get user input
def playerAction(text):
    global runtime

    if runtime['breakPlayerAction']:
        runtime['breakPlayerAction'] = False
        return

    def runPlayerAction(k, v):
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
    
    IN = input(getString(text))

    if not IN:
        return

    INsplit = IN.split(" ")

    if IN == "help":
        print("!! Available commands:\n")

        for command in assetData["adventureCommands"].keys():
            time.sleep(0.5)
            print(f">> {command}")
        for command in activeRoom.commands.keys():
            time.sleep(0.5)
            print(f">> {command}")
    else:
        for k, v in assetData["adventureCommands"].items():
            runPlayerAction(k, v)

        for k, v in activeRoom.commands.items():
            runPlayerAction(k, v)

    playerAction(text)

# Get a response from the player in the form of a string
def userInput(data):
    data = data.split('|')
    data[0] = data[0].lstrip()
    data[1] = data[1].lstrip()
    userRes = input(data[0])
    print(f'Saved variable {data[1]} as {userRes}')
    var(f'string {data[1]} \'{userRes}\'')

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

#Load a room from runtime, or from assets if it's not available.
def loadRoom(selectedRoom):
    global activeRoom
    #unless the player isnt in a room, save the previous room to the runtime
    if activeRoom.name != "No room": 
        roomData = {
            "floorItems": activeRoom.floorItems,
            "roomCommands": activeRoom.commands,
            "shopItems": activeRoom.shopItems,
            "investigateables": activeRoom.investigateables,
            "characters": activeRoom.characters,
            "connectedRooms": activeRoom.connectedRooms
        }

        with open(f"{runtime['dirPath']}runtime/{activeRoom.name}.json", "w") as outFile:
            json.dump(roomData, outFile, indent=4)

    #If the room exists in the runtime, load that, else load from assets.
    
    if os.path.exists(f"{runtime['dirPath']}runtime/{selectedRoom}.json"):
        with open(f"{runtime['dirPath']}runtime/{selectedRoom}.json", "r") as JSON:
            data = json.load(JSON)

    else:
        with open(f"{runtime['dirPath']}adventures/{runtime['selectedAdventure']}/rooms/{selectedRoom}.json") as JSON:
            data = json.load(JSON)

    
    activeRoom = room(selectedRoom)

    if "floorItems" in data:
        activeRoom.floorItems = data["floorItems"]
    if "roomCommands" in data:
        activeRoom.commands = data["roomCommands"]
    if "shopItems" in data:
        activeRoom.shopItems = data["shopItems"]
    if 'investigateables' in data:
        activeRoom.investigateables = data['investigateables']
    if 'lookAroundEvent' in data:
        activeRoom.lookAroundEvent = data['lookAroundEvent']
    if 'characters' in data:
        activeRoom.characters = data['characters']
    if 'connectedRooms' in data:
        activeRoom.connectedRooms = data['connectedRooms']

def moveTo(direction, supressPrints=False):
    if direction in activeRoom.connectedRooms:
        for x in activeRoom.connectedRooms[direction]['execute']:
            runCommand(x)
        loadRoom(activeRoom.connectedRooms[direction]['room'])

def setActiveRoomShop():
    for k, v in assetData["shopCommands"].items():
        activeRoom.commands[k] = v

#Display items that are on the floor.
def displayFloorItems(type):
    activeRoom.displayFloorItems(type=type)

#Handle the playing picking up items
def pickup(item, supressPrints=False):
    #If its a weapon that exists, add it to the player's weapon list.
    if item in assetData['weapons'].keys() and item in activeRoom.floorItems.keys():
        if item in inventory["weapons"]:
            print(f"!! You already have that, you don't need another one.")
        else:
            if not supressPrints:
                print(f"!! Picked up {assetData['weapons'][item].desc}")
            inventory["weapons"].append(item)
            activeRoom.floorItems[item]["amount"] -= 1

    #If its a consumable that exists, add it to the player's consumable list.
    elif item in assetData["consumables"].keys() and item in activeRoom.floorItems.keys():
        if not supressPrints:
            print(f'!! Picked up {assetData["consumables"][item].desc}')

        if item in inventory["consumables"].keys():
            inventory["consumables"][item]["amount"] += 1
        else:
            inventory["consumables"][item] = {
                "amount": 1
            }
        time.sleep(0.5)
        if not supressPrints:
            print(f"!! You now have {inventory['consumables'][item]['amount']} {item}s")
        activeRoom.floorItems[item]["amount"] -= 1

    #If its an equipment that exists, add it to the player's equipment list.
    elif item in assetData["equipment"].keys() and item not in inventory["equipment"] and item in activeRoom.floorItems.keys():

        if item in inventory['equipment']:
            print(f'!! You already have {assetData["equipment"][item].desc}')
        else:
            if not supressPrints:
                print(f'!! Picked up {assetData["equipment"][item].desc}')
            inventory["equipment"].append(item)
            activeRoom.floorItems[item]["amount"] -= 1

    #If its an armor that exists, add it to the player's armor list.
    elif item in assetData["armors"].keys() and item in activeRoom.floorItems.keys():
        if item in inventory['armor']:
            if not supressPrints:
                print(f'!! Picked up {assetData["armors"][item].desc}')
            inventory["armor"].append(item)
            activeRoom.floorItems[item]["amount"] -= 1

    #If nothing seems to work, tell the player he/she can't
    else:
        if not supressPrints:
            print(f"!! Cannot pick up {item}")

    #Delete the item key from floorItems if amount is 0
    if item in activeRoom.floorItems.keys() and activeRoom.floorItems[item]["amount"] <= 0:
        del activeRoom.floorItems[item]

#Handle the player equipping items
def equipWeapon(weapon, supressPrints=False):
    if weapon in inventory["weapons"]:
        global runtime
        runtime['equippedWeapon'] = weapon
        if not supressPrints:
            print(f"!! {weapon} equipped")

    else:
        print("!! You do not have a weapon with that name")

#Display the player's inventory
def displayInventory(type):
    print("!! Opening inventory...")
    scroll()
    print("!! Gold: ", inventory["gold"])
    print("!! Weapons:")
    time.sleep(0.5)
    for weapon in inventory["weapons"]:
        if weapon == runtime['equippedWeapon']:
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
    assetData["enemies"][enemy].displayAscii()

#Spawn an enemy as part of the next combat sequence.
def spawnEnemy(enemy, supressPrints=False):
    if enemy in assetData["enemies"].keys():
        global runtime
        runtime['activeEnemies'][enemy] = {
            "health": assetData["enemies"][enemy].health
        }
        
        if not supressPrints:
            print(f"!! {enemy} is attacking you")
        time.sleep(1)

#Add an item to the player's inventory.
def giveItem(item, supressPrints=False):
    global inventory

    if item in assetData['weapons'].keys():
        if item in inventory['weapons']:
            
            if not supressPrints:
                print(f'!! You were given {assetData["weapons"][item].desc} But you already had one')
        else:
            inventory["weapons"].append(item)
            if not supressPrints:
                print(f'!! You were given {assetData["weapons"][item].desc}')
    elif item in assetData["consumables"].keys():
        if item in inventory["consumables"].keys():
            if not supressPrints:
                print(f'!! You were given {assetData["consumables"][item].desc}')
            inventory["consumables"][item]["amount"] += 1
        else:
            inventory["consumables"][item] = {
                "amount": 1
            }
            if not supressPrints:
                print(f'!! You were given {assetData["consumables"][item].desc}\nYou now have {inventory["consumables"][item]["amount"]}')
    elif item in assetData["equipment"].keys():
        if item in inventory['equipment']:
            if not supressPrints:
                print(f'!! You were given {assetData["equipment"][item].desc} But you already have one')
        else:
            inventory["equipment"].append(item)
            if not supressPrints:
                print(f'You were given {assetData["equipment"][item].desc}')
    elif item in assetData["armors"].keys():
        if item in inventory['armor']:
            if not supressPrints:
                print(f'!! You were given {assetData["armors"][item].desc} But you already have one')
        else:
            inventory["armor"].append(item)
            if not supressPrints:
                print(f'You were given {assetData["armors"][item].desc}')

def newrunCombat():

    def attack(combatString, combatArea, legend):

        #region Generate enemy list
        enemyList = list(runtime['activeEnemies'].keys())
        #endregion Generate enemy list

        option, index = menuSelect(combatString, enemyList)
        combatString = combatString.split('\n')
        combatString[-1] = f'You attacked {option}'
        combatString = '\n'.join(combatString)
        return combatString

    def use(combatString, combatArea, legend):
        print('Use mode activated')
        time.sleep(3)
        return combatString

    def flee(combatString, combatArea, legend):
        print('flee mode activated')
        time.sleep(3)
        return combatString

    combatActions = {
        'Attack': attack,
        'Use': use,
        'Flee': flee
    }

    global runtime

    #region generate map
    combatArea = []
    combatString = ''

    # Generating map:
    for a in range(20):
        combatArea.append([' ' for b in range(20)])
    legend = []

    # Placing player on map:
    while True:
        playerPosX = random.randint(0, 19)
        playerPosY = random.randint(0, 19)

        if combatArea[playerPosX][playerPosY] == ' ':
            legend.append('P = Player')
            combatArea[playerPosX][playerPosY] = 'P'
            break

    # Placing enemies on map:
    i = 1
    for x in runtime['activeEnemies'].keys():

        while True:
            enemyPosX = random.randint(0, 19)
            enemyPosY = random.randint(0, 19)

            if combatArea[enemyPosX][enemyPosY] == ' ':
                legend.append(f'{x} = {i}')
                combatArea[enemyPosX][enemyPosY] = str(i)
                break

        i += 1

    # Adding legend to combat string:
    i = 0
    for x in legend:
        combatString = f'{combatString}{x} | '
        i += 1
        if i == 10:
            combatString = f'{combatString}\n'
            i = 0
    combatString = f'{combatString}\n\n'
    
    # Adding map to combat string:
    for x in combatArea:
        combatString = f'{combatString}{"".join(["-" for i in range(77)])}\n{" | ".join(x)}\n'
    #endregion generate map
    combatString = f'{combatString}\n' # Add empty line to fill space that text feedback will use later

    while True:
        option, index = menuSelect(combatString, list(combatActions.keys()))

        action = combatActions.get(option, None)
        combatString = action(combatString, combatArea, legend)

#Start a combat sequence.
def runCombat():
    global runtime

    if len(runtime['activeEnemies']) < 1:
        return

    while not runtime['gameOver']:

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
            result = assetData['weapons'][runtime['equippedWeapon']].attack(enemyName)

            if result:
                runtime['activeEnemies'][enemyName]['health'] -= result
                print(f"!! {enemyName}'s health is now {runtime['activeEnemies'][enemyName]['health']}")
                time.sleep(1)

                if runtime['activeEnemies'][enemyName]['health'] <= 0:
                    del runtime['activeEnemies'][enemyName]

        elif fnmatch.fnmatch(IN, "use *"):
            useCommand = IN.split(" ")

            del useCommand[0]
            consumableName = " ".join(useCommand)

            if consumableName in inventory["consumables"].keys():
                if inventory["consumables"][consumableName]["amount"] > 0:
                    if assetData["consumables"][consumableName].use():
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
        
        if len(runtime['activeEnemies']) < 1:
            time.sleep(0.5)
            scroll()
            time.sleep(0.1)
            print(f"!! You have defeated all the enemies")
            time.sleep(0.5)
            return

        for k, v in runtime['activeEnemies'].items():
            assetData["enemies"][k].attack()

#Display a shop's items and prices.
def checkShopItems(type):
        if type == "all":
            for key, value in activeRoom.shopItems.items():
                print(f"|| {key} : {value['price']} gold")

def buyItem(item):
    if item in activeRoom.shopItems.items and inventory["gold"] >= activeRoom.shopItems[item]["cost"]:
        giveItem(activeRoom.shopItems[item]["type"], item)
        inventory["gold"] -= activeRoom.shopItems[item]["cost"]

def addGold(gold):
    gold = int(gold)
    if not "gold" in inventory:
        inventory["gold"] = gold
    else:
        inventory["gold"] += gold

def investigate(obj):
    if activeRoom.investigateables:
        if obj in activeRoom.investigateables.keys():
            for command in activeRoom.investigateables[obj]:
                runCommand(command)
    else:
        print('There is nothing to investigate')

def lookAround():
    for x in activeRoom.lookAroundEvent:
        runCommand(x)

def talkTo(character):
    if character in activeRoom.characters:
        dialog = assetData['characters'][character]['dialog']

        dialogIndex = 'initial'
        while True:
            options = []
            if 'responses' in dialog[dialogIndex]:
                for k, v in dialog[dialogIndex]['responses'].items():
                    options.append(v['resp'])
                options.append('Leave conversation')
                option, index = menuSelect(dialog[dialogIndex]['prompt'], options)
                if option == 'Leave conversation':
                    break
                dialogIndex = dialog[dialogIndex]['responses'][str(index)]['next']
            else:
                options.append('Leave conversation')
                option, index = menuSelect(dialog[dialogIndex]['prompt'], options)
                break

# Handler for creating or overwriting .ta variables
def var(data):
    global runtime
    def string(name, data):
        stringVal = re.search('\'(.*?)\'', data).group(1)

        #print(f'Variable \'{name}\' has value \'{stringVal}\'')
        runtime['codeVars'][name] = {
            'type': 'string',
            'val': stringVal
        }
        #print(runtime['codeVars'][name])

    varTypes = {
        'string': string
    }

    varData = data.split(' ')
    varType = varTypes.get(varData[0], None)
    if varType:
        varType(varData[1], data)

def textScrollToggle():
    runtime['textScroll']['active'] = not runtime['textScroll']['active']
def setTextScrollDelay(delay):
    runtime['textScroll']['delay'] = float(delay)

#endregion gameEngine functions

#region defining gameEngine commands

#Defining script commands for the init scope.
initCommands = benedict({
    'import': {
        'mod': loadMod,
        'asset': loadAsset
        }
    },keypath_separator='.')

#Defining script commands for the story scope.
commands = benedict({
    "displayText": displayText,
    "sleep": sleep,
    "scroll": scroll,
    "playerAction": playerAction,
    'userInput': userInput,
    "loadRoom": loadRoom,
    "moveTo": moveTo,
    "displayFloorItems": displayFloorItems,
    "pickup": pickup,
    "equipWeapon": equipWeapon,
    "displayInventory": displayInventory,
    "spawnEnemy": spawnEnemy,
    "runCombat": runCombat,
    "displayEnemy": displayEnemy,
    "giveItem": giveItem,
    "printASCII": printASCII,
    "saveGame": saveGame,
    "endGame": endGame,
    "setCursor": setCursor,
    "breakPlayerAction": setbreakPlayerAction,
    "checkShopItems": checkShopItems,
    "addGold": addGold,
    "openShop": setActiveRoomShop,
    'lookAround': lookAround,
    'investigate': investigate,
    'talkTo': talkTo,
    'var': var,
    'textScroll': {
        'toggle': textScrollToggle,
        'delay': setTextScrollDelay
        }
    },keypath_separator='.')

#endregion defining gameEngine commands

#Testing whether the file is run or imported
if __name__ == "__main__":
    main()