import time, os, json, random

dirPath = os.path.realpath(__file__).split("\\")
dirPath.pop()
temp = ""
for i in dirPath:
    temp += (f"{i}/")
dirPath = temp

gameOver = False

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

            print("!! Rolling hit dice...")
            time.sleep(0.5)
            hitDice = int(self.hitDice.split("x")[0]) * int(self.hitDice.split("x")[1])
            hitRoll = random.randint(1, hitDice)
            print(f"!! You rolled {hitRoll}")
            time.sleep(0.5)

            if hitRoll > int(enemies[target].AC):
                print("!! That hits!")
                time.sleep(1)
                
                print("!! Rolling damage dice...")
                time.sleep(0.5)
                damageDice = int(self.damageDice.split("x")[0]) * int(self.damageDice.split("x")[1])
                damageRoll = random.randint(1, damageDice)
                print(f"!! You rolled {damageRoll}")
                time.sleep(0.5)
                return damageRoll

            else:
                print("!! You miss!")
                time.sleep(1)
                return False

        elif mode == "enemy":
            
            print(f"!! {activeEnemy} is attacking!")
            time.sleep(1)
            print(f"!! {activeEnemy} is rolling hit dice with {self.name}...")
            time.sleep(1)
            hitDice = int(self.hitDice.split("x")[0]) * int(self.hitDice.split("x")[1])
            hitRoll = random.randint(1, hitDice)
            print(f"!! {activeEnemy} rolled {hitRoll}")
            time.sleep(1)

            if hitRoll > playerStats["AC"]:
                print("!! Ouch, that hits!")
                time.sleep(1)

                print(f"!! {activeEnemy} is rolling damage dice...")
                time.sleep(1)
                damageDice = int(self.damageDice.split("x")[0]) * int(self.damageDice.split("x")[1])
                damageRoll = random.randint(1, damageDice)
                print(f"!! {activeEnemy} rolled {damageRoll}")
                time.sleep(1)
                return damageRoll
            
            else:
                print(f"!! {activeEnemy} missed!")
                time.sleep(1)
                return False

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
        printTXT(self.ascii)

    def attack(self):
        result = weapons[self.weapon].attack("player", "enemy")

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
        self.floorItems = False

    def setFloorItems(self, floorItems):
        self.floorItems = floorItems

    def displayFloorItems(self, type):
        floorItems = self.floorItems

        if type == "all":
            for k, v in floorItems.items():
                print(f"ii {k}")
                time.sleep(0.5)

selectedAdventure = ""

weapons = {}
consumables = {}
equipment = {}
inventory = {
    "weapons": [],
    "consumables": {},
    "equipment": []
}
playerStats = {
    "health": 20,
    "AC": 10
}
equippedWeapon = ""

adventureCommands = {}

activeRoom = room("No room") # Initialize the active room as an empty room with no features

enemies = {}
activeEnemy = ""

def main():
    print("!! Text adventure Engine !!")
    time.sleep(0.5)
    print(getAdventures())
    
    adventure = False
    while not adventure:
        adventure = loadAdventure(input("Select one of the above adventures >> "))
    scroll()
    i = loadStory(adventure)
    scroll()
    i = runStory(adventure, i + 1)
    print("!! The story has come to an end")
    time.sleep(1)
    
def removeFileExtention(file):
    return file.replace(".txt", "")

def displayText(text):
    print(text)

def printTXT(filePath):
    with open(f"{dirPath}adventures/{selectedAdventure}/{filePath}.txt") as TXT:
        print(TXT.read())

def prompt(text):
    IN = input(text)
    INsplit = IN.split(" ")

    if not IN:
        return
    elif IN == "help":
        print("!! Available commands:\n")

        for command in adventureCommands.keys():
            time.sleep(0.5)
            print(f">> {command}")

    try:
    
        for k, v in adventureCommands.items():
            multiWordFill = False
            if "<?" in k:
                splitCommand = k.split(" ")
                
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
                    command = v.replace("<?>", INsplit[variableIndex])
                    if command.startswith("!"):
                        commandList = getCommand(command)
                        runCommand(commandList)

                elif commandFound and multiWordFill:
                    i = variableIndex
                    multiWord = ""
                    while i < len(INsplit):
                        multiWord += INsplit[i] + " "
                        i += 1
                    multiWord = multiWord[:-1]
                        
                    command = v.replace("<?", multiWord)
                    if command.startswith("!"):
                        commandList = getCommand(command)
                        runCommand(commandList)
                    
            else:
                splitCommand = k.split(" ")
                i = 0
                commandFound = True
                for x in splitCommand:
                    if x == INsplit[i]:
                        commandFound = True
                    else:
                        commandFound = False
                        break
                    i += 1
                
                if commandFound:
                    if v.startswith("!"):
                        commandList = getCommand(v)
                        runCommand(commandList)
        
    except IndexError:
        print("!! Oops! Seems you are missing part of the command! Remember, you can write help for a list of all commands")

    prompt(text)

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

def runCommand(commandList):
    command = commands.get(commandList[0], None)
    if command:
        command(commandList[1])
        return True
    else:
        return False

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

    loadAssetData(data)

def loadAsset(assetName):
    print("Importing asset...")
    with open(f"{dirPath}adventures/{selectedAdventure}/assets/{assetName}.json") as JSON:
        data = json.load(JSON)

    loadAssetData(data)

def runStory(story, i):
    while True:

        if gameOver:
            return i
        elif story[i] == ":story":
            return i

        elif story[i].startswith("!"):
            commandList = getCommand(story[i])
            command = commands.get(commandList[0], None)
            if command:
                command(commandList[1])

        i += 1

def pickup(item):

    if item in weapons.keys() and item not in inventory["weapons"] and item in activeRoom.floorItems.keys():
        print(f"!! Picked up {weapons[item].desc}")

        inventory["weapons"].append(item)
        del activeRoom.floorItems[item]

    elif item in consumables.keys() and item in activeRoom.floorItems.keys():
        print(f"!! Picked up {consumables[item].desc}")

        if item in inventory["consumables"].keys():
            inventory["consumables"][item]["amount"] += 1
        else:
            inventory["consumables"][item] = {
                "amount": 1
            }
        time.sleep(0.5)
        print(f"!! You now have {inventory['consumables'][item]['amount']} {item}s")
        del activeRoom.floorItems[item]

    elif item in equipment.keys() and item not in inventory["equipment"] and item in activeRoom.floorItems.keys():
        print(f"!! Picked up {equipment[item].desc}")

        inventory["equipment"].append(item)
        del activeRoom.floorItems[item]

    else:
        print(f"!! Cannot pick up {item}")

def equipWeapon(weapon):
    if weapon in inventory["weapons"]:
        global equippedWeapon
        equippedWeapon = weapon
        print(f"!! {weapon} equipped")

    else:
        print("!! You do not have a weapon with that name")

def displayInventory(type):
    print("!! Opening inventory...")
    scroll()
    print("!! Weapons:")
    time.sleep(0.5)
    for weapon in inventory["weapons"]:
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

def displayEnemy(enemy):
    enemies[enemy].displayAscii()

def spawnEnemy(enemy):
    if enemy in enemies.keys():
        global activeEnemy
        activeEnemy = enemy
        
        print(f"!! {enemy} is attacking you")
        time.sleep(1)
        runCombat()

def runCombat():
    enemyHealth = enemies[activeEnemy].health
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

        if IN == "attack":
            result = weapons[equippedWeapon].attack(activeEnemy)

            if result:
                enemyHealth -= result
                print(f"!! {activeEnemy}'s health is now {enemyHealth}")
                time.sleep(1)

        if enemyHealth <= 0:
            time.sleep(0.5)
            scroll()
            time.sleep(0.1)
            print(f"!! You have defeated the {activeEnemy}")
            time.sleep(0.5)
            break

        enemies[activeEnemy].attack()

initCommands = {
    "importMod": loadMod,
    "importAsset": loadAsset
}

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
}

if __name__ == "__main__":
    main()