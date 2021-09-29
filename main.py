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

selectedAdventure = ""
weapons = {}

def main():
    print("!! Text adventure Engine !!")
    time.sleep(0.5)
    print(getAdventures())
    
    adventure = False
    while not adventure:
        adventure = loadAdventure(input("Select one of the above adventures >> "))
    print(selectedAdventure)
    scroll()
    i = loadStory(adventure)
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

def loadMod(modName):
    print("Importing mods...")
    with open(f"{dirPath}mods/{modName}.json") as JSON:
        data = json.load(JSON)

    print(data)
    if data["weapons"]:
        for k, v in data["weapons"].items():
            weapons[k] = weapon(k, v["damageDice"], v["hitDice"], v["weight"])

def loadAsset(assetName):
    print("Importing mods...")
    with open(f"{dirPath}adventures/{selectedAdventure}/assets/{assetName}.json") as JSON:
        data = json.load(JSON)

    print(data)
    if data["weapons"]:
        for k, v in data["weapons"].items():
            weapons[k] = weapon(k, v["damageDice"], v["hitDice"], v["weight"])

def loadWeapons(data, i):
    print("Loading weapons...")
    currentWeapon = ""
    while True:
        if data[i].startswith("!"):
            currentWeapon = data[i].replace("!", "")
            weaponData = {
                "damageDice": "",
                "hitDice": "",
                "weight": "",
            }

        elif data[i] == f"{currentWeapon}!":
            weapons[currentWeapon] = weapon(currentWeapon, weaponData["damageDice"], weaponData["hitDice"], weaponData["weight"])
            print(weapons[currentWeapon])
        elif data[i] == ":weapons":
            print("All weapons loaded...")
            return i
        else:
            Property = data[i].split(" : ")
            weaponData[Property[0]] = Property[1]

        i += 1

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
    "prompt": prompt
}

if __name__ == "__main__":
    main()