import time, os, json

dirPath = os.path.realpath(__file__).split("\\")
dirPath.pop()
temp = ""
for i in dirPath:
    temp += (f"{i}/")
dirPath = temp

class weapon():
    def __init__(self, name, damageDice, hitDice, weight):
        self.name = name
        self.damageDice = damageDice
        self.hitDice = hitDice
        self.weight = weight
        print(f"{self.name} loaded")

class consumable():
    def __init__(self, name, desc, effect):
        self.name = name
        self.desc = desc
        self.effect = effect
        print(f"{self.name} loaded")

class equipmentClass():
    def __init__(self, name, desc, effect):
        self.name = name
        self.desc = desc
        self.effect = effect
        print(f"{self.name} loaded")

class room():
    def __init__(self, name):
        self.name = name
        self.floorItems = False

    def setFloorItems(self, floorItems):
        self.floorItems = floorItems

    def displayFloorItems(self, type):
        floorItems = self.floorItems

        if type == "all":
            for k, v in floorItems.items():
                print(f"ii {k}")
                time.sleep(1)

selectedAdventure = ""
weapons = {}
consumables = {}
equipment = {}
activeRoom = room("No room") # Initialize the active room with an empty room with no features

def main():
    print("!! Text adventure Engine !!")
    time.sleep(0.5)
    print(getAdventures())
    
    adventure = False
    while not adventure:
        adventure = loadAdventure(input("Select one of the above adventures >> "))
    scroll()
    i = loadStory(adventure)
    print(weapons, "\n", consumables, "\n", equipment)
    scroll()
    i = runStory(adventure, i + 1)
    
def removeFileExtention(file):
    return file.replace(".txt", "")

def displayText(text):
    print(text)

def prompt(text):
    IN = input(text)
    print(IN)

def sleep(secs):
    time.sleep(float(secs))

def scroll(lines=5, delay=0.1):
    i = 0
    while i < int(lines):
        print("\n")
        i += 1
        time.sleep(delay)

def getCommand(commandString):
    commandString = commandString[1:]
    return commandString.split(" : ")

def getAdventures():
    print("Loading adventures...")
    time.sleep(0.5)
    adventures = os.listdir(f"{dirPath}adventures")

    for i in adventures:
        print(f"|| {removeFileExtention(i)}")
        time.sleep(0.1)

def loadAdventure(adventure):
    global selectedAdventure
    selectedAdventure = adventure
    try:
        with open(f"{dirPath}adventures/{adventure}/main.txt") as f:
            data = f.read().splitlines()
        return data
    except:
        return False

def loadStory(story):
    i = 0
    while i < len(story):
        if story[i] == "init:":
            print("Initializing...")
            i = runInit(story, i + 1)

        elif story[i] == "story:":
            return i

        i += 1

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
            return i

        i += 1

def loadItems(data):
    if data["weapons"]:
        for k, v in data["weapons"].items():
            weapons[k] = weapon(k, v["damageDice"], v["hitDice"], v["weight"])
    
    if data["consumables"]:
        for k, v in data["consumables"].items():
            consumables[k] = consumable(k, v["desc"], v["effect"])

    if data["equipment"]:
        for k, v in data["equipment"].items():
            equipment[k] = equipmentClass(k, v["desc"], v["effect"])

def loadRoom(selectedRoom):
    with open(f"{dirPath}adventures/{selectedAdventure}/rooms/{selectedRoom}.json") as JSON:
        data = json.load(JSON)

    global activeRoom
    activeRoom = room(selectedRoom)

    if data["floorItems"]:
        activeRoom.setFloorItems(data["floorItems"])

def displayFloorItems(type):
    activeRoom.displayFloorItems(type=type)

def loadMod(modName):
    print("Importing mods...")
    with open(f"{dirPath}mods/{modName}.json") as JSON:
        data = json.load(JSON)

    loadItems(data)

def loadAsset(assetName):
    print("Importing mods...")
    with open(f"{dirPath}adventures/{selectedAdventure}/assets/{assetName}.json") as JSON:
        data = json.load(JSON)

    loadItems(data)

def runStory(story, i):
    while True:

        if story[i] == ":story":
            return i

        elif story[i].startswith("!"):
            commandList = getCommand(story[i])
            command = commands.get(commandList[0], None)
            if command:
                command(commandList[1])


        i += 1


initCommands = {
    "importMod": loadMod,
    "importAsset": loadAsset
}

commands = {
    "displayText": displayText,
    "sleep": sleep,
    "scroll": scroll,
    "loadRoom": loadRoom,
    "displayFloorItems": displayFloorItems,
    "prompt": prompt
}

if __name__ == "__main__":
    main()