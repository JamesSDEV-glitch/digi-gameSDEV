import random
import json
import time
# Globals
global playerSTARTHP, quests, activeQuest, statusVisited, currentItem, currentLocation, playerDict, rickFound, timeScale
playerSTARTHP = 50
quests = []
npcQuests = []
activeQuest = None
statusVisited = 0
currentItem = None
currentLocation = None
rickFound = False
timeScale = 20
# PLAYER
class Player:
    def __init__(self, name, hp, strength, intel, luck, skill, startHP, level, xp, armorClass, age, trait, gender, money, inventory):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.intel = intel
        self.luck = luck
        self.skill = skill
        self.startHP = startHP
        self.level = level
        self.xp = xp
        self.armorClass = armorClass
        self.age = age
        self.trait = trait
        self.gender = gender
        self.money = money
        self.inventory = inventory if inventory else []
    def rollAttack(self, enemy):
        global currentItem

        if currentItem is None:
            damageRoll = random.randint(1, 10)
        else:
            damageRoll = random.randint(currentItem.dL, currentItem.dH)
        damageHit = damageRoll + self.strength
        chanceHit = random.randint(1, 10) + self.skill

        print(f"DAMAGE ROLLED: {damageRoll}")

        if damageRoll >= 10:
            damageHit += 10
        else:
            damageHit -= 3

        print(f"DAMAGE: {damageHit}")

        if chanceHit == 10:
            print(f"PERFECT HIT! CHANCE ROLLED: {chanceHit}")
            damageHit += 30
            enemy.hp -= damageHit
        elif chanceHit <= 5:
            print(f"FAILED HIT, NO DAMAGE INFLICTED. CHANCE ROLLED: {chanceHit}")
        else:
            print(f"GOOD HIT. CHANCE ROLLED: {chanceHit}")
            enemy.hp -= damageHit

        print(f"ENEMY HEALTH: {enemy.hp}")

    def inventoryHandler(self, item):
        player.inventory.append(item)
        triggerEvent("find_item", item.name)

    def printInventory(self, item):
        print()
        print(f"NAME: {item.name}")
        print(f"----- HEALTH BOOST: {item.healthBoost}")
        print(f"----- DAMAGE: {item.dL}-{item.dH}")
        print(f"----- ARMOUR CLASS: {item.armorPoints}")
        print(f"----- DESC: {item.desc}")
        print(f"----- TAG: {item.tag}")
        print()

    def useItem(self):
        global currentItem
        if not player.inventory:
            print("EMPTY")
            return

        print("Which item do you want to use?")
        for index, i in enumerate(player.inventory):
            print(f"{index+1}. {i.name}")

        try:
            choice = int(input("> ")) - 1
            item = player.iinventory[choice]  # don't pop, keep in inventory

            if item.tag == "special":
                print(item.addInfo)
            else:
                if item.tag == "health":
                    self.startHP += item.healthBoost
                    print(f"You used {item.name}! HP is now {self.startHP}")
                elif item.tag == "weapon":
                    currentItem = item
                    print(f"Equipped {currentItem.name}. Damage is now {currentItem.dL}-{currentItem.dH}.")
                elif item.tag == "armour":
                    pickedArmour = item
                    print(f"Equipped {pickedArmour.name}. Armour Class is now {pickedArmour.armorPoints}.")
                    player.armorClass = pickedArmour.armorPoints
        except:
            print("Invalid choice.")
            return

    def checkLevelUp(self):
        if self.xp >= 3000:
            self.level += 1
            self.intel += 1
            self.strength += 1
            self.startHP += 20
            self.luck += 1
            self.skill += 1
            self.xp = 0
            print(f"YOU LEVELED UP! CURRENT LEVEL: {self.level}")

    def status(self):
        global statusVisited
        if statusVisited == 0:
            print("HERE, IN YOUR TRUSTY JANAS. ALMANAC, YOU CAN VIEW YOUR STATS!")
            print("Here is a rundown:")
            print("Strength can add boosts for damage when you hit.")
            print("INT: WIP")
            print("LUCK: WIP")
            print("Skill: Makes it easier to land hits on enemies.")
            print("LEVELLING UP:")
            print("When you level up, your stats increase by 1.")
            print("Your max HP also increases by 20.")
            print("Well, I'll let you get on.")
            print("KEEP CONSULTING YOUR TRUSTY JANAS. ALMANAC FOR ALL YOUR NEEDS!")
            statusVisited += 1
        else:
            print("STATUS: ")
            print(f"NAME: {self.name}")
            print(f"AGE: {self.age}")
            print(f"GENDER: {self.gender}")
            print(f"HP: {self.startHP}")
            print(f"ARMOR CLASS: {self.armorClass}")
            print(f"STRENGTH: {self.strength}")
            print(f"INT: {self.intel}")
            print(f"SKILL: {self.skill}")
            print(f"LUCK: {self.luck}")
            print(f"LEVEL: {self.level}")
            print(f"XP: {self.xp}")
            print(f"TRAIT: {self.trait}")
            print(f"MONEY: {self.money}")
            
# ENEMY
class Enemy:
    def __init__(self, name, hp, dL, dH, startHP):
        self.name = name
        self.hp = hp
        self.dL = dL
        self.dH = dH
        self.startHP = startHP

    def enemyAttack(self, player):
        if player.armorClass > 0:
            damageBase = random.randint(self.dL, self.dH)
            damage = damageBase / player.armorClass
            chance = random.randint(1, 10)
        elif player.armorClass == 0:
            damageBase = random.randint(self.dL, self.dH)
            chance = random.randint(1, 10)
        print(f"{self.name} rolled {chance} chance.")
        if chance == 10:
            damage += 10
            player.hp -= damageBase
            print(f"{self.name} HIT YOU FOR {damageBase} DAMAGE! Your health: {player.hp}")
        elif chance >= 5:
            player.hp -= damageBase
            print(f"{self.name} HIT YOU FOR {damageBase} DAMAGE! Your health: {player.hp}")
        elif chance < 5:
            print(f"{self.name} missed!")

# ITEMS
class items:
    def __init__(self, name, healthBoost, dH, tag, desc, addInfo, dL, armorPoints, cost):
        self.name = name
        self.healthBoost = healthBoost
        self.dH = dH
        self.tag = tag
        self.desc = desc
        self.addInfo = addInfo
        self.dL = dL
        self.armorPoints = armorPoints
        self.cost = cost
# LOCATIONS
class Location:
    def __init__(self, name, description, connections=None, encounters=None):
        self.name = name
        self.description = description
        self.connections = connections if connections else {}
        self.encounters = encounters if encounters else []
# QUESTS
class quest:
    def __init__(self, name, requirement, desc, qtype, xpGain):
        self.name = name
        self.requirement = requirement
        self.desc = desc
        self.type = qtype
        self.completed = False
        self.xpGain = xpGain
# NPCs AND DIALOGUE
class NPC:
    def __init__(self, name, desc, dialogue, questDialogue, responseY, responseN):
        self.name = name
        self.desc = desc
        self.dialogue = dialogue
class DialogueNode:
    def __init__(self, id, text, choices=None, onEnter=None):
        self.id = id
        self.text = text
        self.choices = choices if choices else []
        self.onEnter = onEnter  # function to run when entering node

class DialogueChoice:
    def __init__(self, text, nextNode=None, action=None):
        self.text = text
        self.nextNode = nextNode
        self.action = action
def runDialogue(nodes, startNode):
    current = nodes[startNode]
    while True:
        # If node has an onEnter script, run it
        if current.onEnter:
            current.onEnter()
        print("\n" + current.text + "\n")
        # END NODE
        if len(current.choices) == 0:
            print("Dialogue ended.\n")
            return
        # Show player choices
        for i, ch in enumerate(current.choices):
            print(f"{i+1}. {ch.text}")
        # Input handling
        try:
            choiceIndex = int(input("> ")) - 1
            choice = current.choices[choiceIndex]
        except:
            print("Invalid option.")
            continue
        # run action script if exists
        if choice.action:
            choice.action()
        # go to next node
        if choice.nextNode in nodes:
            current = nodes[choice.nextNode]
        else:
            print("Dialogue ended.\n")
            return
def makeRandomNpc():
    namesFirst = ["Joe", "Rita", "John", "Rick", "Randy", "Georgia", "Larry"]
    namesSecond = ["Smith", "Mitchell", "Jackson", "Thomas", "Jones", "RiZario"]
    descs = ["Tall, built like a brick, stinks.", "Long, crooked nose stands out, glasses carefully balanced on top."]
    greetingDialogues = ["Hey, hello! How are you?", "I don't like you. Get this over with.", "Do you know about the rangers?"]
    qDialogues = ["Hey, I need some help with something.", "You know what, I got a lil' something yer can help with, 'ey?"]
    responsesN = ["Oh... well, okay then.", "Guess I'll have to ask somebody else.", "Get outta my sight."]
    responsesY = ["Thank you so much!", "Thanks, I guess.", "Get to it then!"]
    randFirstName = random.choice(namesFirst)
    randSecondName = random.choice(namesSecond)
    randName = randFirstName + " " + randSecondName
    randDesc = random.choice(descs)
    randDialogue = random.choice(greetingDialogues)
    randQuest = random.choice(npcQuests)
    randQuestDialogue = random.choice(qDialogues)
    randResponseN = random.choice(responsesN)
    randResponseY = random.choice(responsesY)
    return randName, randDesc, randDialogue, randQuest, randQuestDialogue, randResponseN, randResponseY
def NPCRanddialogue():
    global quests
    randName, randDesc, randDialogue, randQuest, randQuestDialogue, randResponseN, randResponseY = makeRandomNpc()
    nodes = {
        "start": DialogueNode(
            id="start",
            text=f"{randName}: {randDialogue}",
            choices=[
                DialogueChoice("What do you want?", nextNode="ask_help"),
                DialogueChoice("Leave.", nextNode="end")
            ]
        ),
        "ask_help": DialogueNode(
            id="ask_help",
            text=f"{randName}: {randQuestDialogue}",
            choices=[
                DialogueChoice("I'll do it.", nextNode="accept", action=lambda: quests.append(randQuest)),
                DialogueChoice("Not my problem.", nextNode="reject")
            ]
        ),
        "accept": DialogueNode(
            id="accept",
            text=f"{randName}: {randResponseY}\n QUEST ADDED: {randQuest.name}",
            choices=[]
        ),
        "reject": DialogueNode(
            id="reject",
            text=f"{randName}: {randResponseN}",
            choices=[]
        ),
        "end": DialogueNode(
            id="end",
            text="You walk away.",
            choices=[]
        ),
    }
    runDialogue(nodes, "start")
# ENTITIES
ranger = Enemy("Ranger", 200, 10, 15, 200)
megaZombie = Enemy("Mega Zombie", 300, 20, 40, 300)
mutatedZombie = Enemy("Mutated Zombie", 50, 3, 5, 50)
floaters = Enemy("Floaters", 30, 10, 15, 30)
mutScorpion = Enemy("Mutated Scorpion", 150, 50, 70, 150)
usSoldier = Enemy("U.S. Soldier", 100, 30, 40, 100)
rebel = Enemy("Rowdy Rebel", 115, 20, 30, 115)
krakerJackGanger = Enemy("KrakerJack Gangster", 110, 10, 15, 110)
ntmGanger = Enemy("North Territory Montana Ganger", 110, 10, 15, 110)
player = Player("Player", 50, 4, 4, 4, 4, playerSTARTHP, 1, 0, 0, None, None, None, 0, [])
def makePlayerDict():
    return {
        "name": player.name,
        "hp": player.hp,
        "strength": player.strength,
        "intel": player.intel,
        "luck": player.luck,
        "skill": player.skill,
        "startHP": player.startHP,
        "level": player.level,
        "xp": player.xp,
        "armor-class": player.armorClass,
        "age": player.age,
        "gender": player.gender,
        "trait": player.trait,
        "money": player.money
    }
enemies = [ranger, megaZombie, mutatedZombie, floaters, mutScorpion, usSoldier, rebel, krakerJackGanger, ntmGanger]

# CREATE ITEMS
def createItems():
    global milk, beef, coke, fortyfiveRevolver, shotgunCombat, notes1, nukeLauncher, assaultRifle, combatKnife, gatlingLaser, rickEntrySlip, xTExoArmour, xSExoArmour, redTownMap, leatherArmour, combatArmour
    global itemList, lowLuckItems, medLuckItems, highLuckItems
    milk = items("Milk Carton", 15, 0, "health", "A milk carton, dated 2064.", None, 0, 0, 5)
    beef = items("Beef", 20, 0, "health", "Beef of a barsrot.", None, 0, 0, 10)
    cokeTract = items("Tract Coke", 10, 0, "health", "A popular pre-apocalyptic soda.", None, 0, 0, 5)
    fortyfiveRevolver = items(".45 Revolver", 0, 16, "weapon", "A revolver that uses .45 bullets.", None, 10, 0, 35)
    shotgunCombat = items("M-52 Combat Shotgun", 0, 49, "weapon", "An automatic burst M-52 shotgun, made by Janas Weapons for the US army.", None, 34, 0, 250)
    notes1 = items("Mysterious Note 1", 0, 0, "special", "A note.", "These people. They're driving me insane...", 0, 0, 0)
    nukeLauncher = items("Nuke Launcher", 30, 480, "weapon", "A nuke launcher. Does large amounts of damage.", None, 300, 0, 999)
    assaultRifle = items("M-65 Assault Rifle", 0, 50, "weapon", "A M-65 pre-war assault rifle, issued to troops fighting in the 2065 war.", None, 20, 0, 350)
    combatKnife = items("Combat Knife", 0, 10, "weapon", "A serrated-blade with a compass built into the hilt.", None, 7, 0, 25)
    gatlingLaser = items("Gatling Laser", 0, 150, "weapon", "A gatling laser. The last weapon produced for the US army. This one is modified, having a faster spin-up.", None, 70, 0, 1024)
    leatherArmour = items("Leather Armour", 0, 0, "armour", "A patched-up leather jacket and pants. Has mediocre damage resistance.", None, 0, 15, 45)
    combatArmour = items("M-75 Combat Armour", 0, 0, "armour", "M-75 Combat Armour. Certain factions still use this armour, due to its reliability.", None, 0, 25, 85)
    xTExoArmour  = items("X-T65 Exo-Armour", 0, 0, "armour", "X-T65 Exo-Armour. The most basic X-issue Exo-Armours. Issued to paratroopers for the 2065 war.", None, 0, 60, 450)
    xSExoArmour = items("X-S91 Exo-Armour", 0, 0, "armour", "X-S91 Exo-Armour. Currently used by the remaining US army.", None, 0, 150, 2025)
    redTownMap = items("Redtown map", 0, 0, "special", "A dusty old map.", "This map details the forgotten location of Redtown.", 0, 0, 0)
    rickEntrySlip = items("Rick Crass entry slip", 0, 0, "special", "An entry slip, signed by someone called Rick Crass.", f"NAME: RICK CRASS\n AGE: 32\n STATE OF ORIGIN: NEVADE\n", 0, 0, 0)
    itemList = [milk, beef, cokeTract, fortyfiveRevolver, shotgunCombat, notes1, nukeLauncher, assaultRifle, gatlingLaser, combatKnife, leatherArmour, combatArmour, xTExoArmour, xSExoArmour, rickEntrySlip, redTownMap]
    lowLuckItems = [milk, cokeTract, beef, fortyfiveRevolver, combatKnife, leatherArmour]
    medLuckItems = [milk, cokeTract, beef, fortyfiveRevolver, shotgunCombat, notes1, assaultRifle, combatKnife, leatherArmour, combatArmour, xTExoArmour, rickEntrySlip]
    highLuckItems = [milk, cokeTract, beef, fortyfiveRevolver, shotgunCombat, notes1, nukeLauncher, assaultRifle, gatlingLaser, combatKnife, leatherArmour, combatArmour, xSExoArmour, rickEntrySlip]
def checkRickItem(itemFound):
    global rickFound
    if itemFound.name == rickEntrySlip.name:
        print("Someone new has arrived...")
        rickFound = True
    else:
        return
# CREATE QUESTS
def createQuests():
    global quests, npcQuests, usArmyQONE, usArmyQTWO, redRebelQONE, redRebelQTWO, redTownMapQ
    killMUZombsQuest = quest("Kill Mutated Zombies", {"target": "Mutated Zombie", "count": 3}, "Kill 3 Mutated Zombies.", "kill", 600)
    findFFQuest = quest("Find a Revolver", ".45 Revolver", "Find a .45 revolver.", "find", 600)
    findCShotgunQuest = quest("Find a Shotgun", "M-52 Combat Shotgun", "Find a Combat Shotgun.", "find", 600)
    killRangersQuest = quest("Kill Rangers", {"target": "Ranger", "count": 5}, "Kill 5 Rangers.", "kill", 1000)
    findNukeLauncherQuest = quest("Find a nuke launcher", "Nuke Launcher", "Required luck: 8+", "find", 3000)
    killMegaZombieQuest = quest("Kill Mega Zombies", {"target": "Mega Zombie", "count": 10}, "Kill 10 Mega Zombies", "kill", 3000)
    findCokeQuest = quest("Find A Drink", "Tract Coke", "Find a can of Tract Coke.", "find", 600)
    killFloatersQuest = quest("Kill Floaters", {"traget": "Floaters", "count": 5}, "Kill 5 Floaters.", "kill", 1500)
    killMutScorpionQuest = quest("Kill Mutated Scorpions.", {"target": "Mutated Scorpion", "count": 10}, "Kill a Mutated Scorpion nest.", "kill", 3000)
    gettingStartedQuest = quest("Getting started.", None, "Talk to some people.", None, None)
    usArmyQONE = quest("US Army 1. Kill Rebels", {"target": "Rowdy Rebel", "count": 15}, "Kill rebels to aid the army.", "kill", 1500)
    usArmyQTWO = quest("US Army 2. Find some Exo-Armor.", "X-T65 Exo-Armour", "Find a set of X-T65 Exo-Armour.", "find", 1700)
    redRebelQONE = quest("Redtown Rebels 1. Kill U.S. Soldiers.", {"target": "U.S. Soldier", "count": 7}, "Kill U.S. Soldiers to aid the Redtown Rebels.", "kill", 1500)
    redRebelQTWO = quest("Redtown Rebels 2. Find some combat armor.", "M-75 Combat Armour", "Find a set of M-75 Combat Armour.", "find", 1500)
    redTownMapQ = quest("Redtown location", "Redtown map", "Find the map of Redtown", "find", 700)
    quests = [gettingStartedQuest]
    npcQuests.extend([killMegaZombieQuest, findCokeQuest, killMutScorpionQuest, killFloatersQuest, killMUZombsQuest, findFFQuest, findCShotgunQuest, killRangersQuest, findNukeLauncherQuest])
    
# CREATE LOCATIONS
def createLocations():
    global shiftyShinsLocation, jerbankLocation, eastMontanaArmyBaseLocation
    shiftyShinsLocation = Location("Shifty Shins", "A small town with an old shop, a clinic, and a few dusty houses.", encounters=[])
    jerbankLocation = Location("Jerbank", "Numerous battered, steel hosues litter the land in front of you.", encounters=[mutatedZombie, megaZombie])
    shiftyShinsStore = Location("The New Montana store", "A few drowsy looking people hang around", encounters=[])
    eastMontanaArmyBaseLocation = Location("East Montana Army Base", "This place, it feels wrong. You can hear muffled talking from within.", encounters=[ranger])
    shiftyShinsLocation.connections = {"north": jerbankLocation, "east": eastMontanaArmyBaseLocation, "shop": shiftyShinsStore}
    jerbankLocation.connections = {"south": shiftyShinsLocation}
    eastMontanaArmyBaseLocation.connections = {"west": shiftyShinsLocation}
    shiftyShinsStore.connections = {"exit": shiftyShinsLocation}
# QUEST EVENT HANDLER
def triggerEvent(event_type, data=None):
    for q in quests:
        if q.completed:
            continue
        if event_type == "kill" and q.type == "kill":
            if data == q.requirement["target"]:
                q.requirement["count"] -= 1
                print(f"Quest progress: {q.name} ({q.requirement['count']} left)")
                if q.requirement["count"] <= 0:
                    q.completed = True
                    print(f"--- QUEST COMPLETE: {q.name} ---")
                    player.xp += q.xpGain
                    print(f"GAINED {q.xpGain} XP, CURRENT XP: {player.xp} ")
                    player.checkLevelUp()
        if event_type == "find_item" and q.type == "find":
            if data == q.requirement:
                q.completed = True
                print(f"--- QUEST COMPLETE: {q.name} ---")
                player.xp += q.xpGain
                print(f"GAINED {q.xpGain} XP, CURRENT XP: {player.xp} ")
                player.checkLevelUp()
# FACTIONS
class faction:
    def __init__(self, name, desc, questline=None):
        self.name = name
        self.desc = desc
        self.questline = questline if questline else []
def createFactions():
    global USArmyFaction, rebelFaction, factionList, krakerJakGang, ntmGang
    ntmGang = faction("North Territory Montana Gang", "A gang of teens without a place in this turned upside-down world. Their main enemy are the KrakerJaks.", [])
    krakerJakGang = faction("KrakerJaks", "A gang of kids, naming themselves after a baseball player.", [])
    USArmyFaction = faction("U.S. Army", "The largest, most dangerous militia in the world.", [usArmyQONE, usArmyQTWO])
    rebelRedFaction = faction("The Redtown Rebels", "The most well-known rebel group. Named after a pre-war baseball team, the Redtown Rickets.", [redRebelQONE, redRebelQTWO])
    factionList = [USArmyFaction, rebelRedFaction, ntmGang, krakerJakGang]
def chooseFaction():
    print("FACTION SELECTION")
    for index, fact in enumerate(factionList):
        fIndex = index + 1
        print(f"{fIndex}. {fact.name}")
        print(f"---- {fact.desc}\n")
    choice = int(input("FACTION NUM: ")) - 1
    chosenFaction = factionList[choice]
    quests.extend(chosenFaction.questline)
    print(f"Joined {chosenFaction.name}. New quests added.")
    return
# CHOOSE QUEST
def chooseQuest():
    global activeQuest
    print("\nQUESTS:\n")
    for index, q in enumerate(quests):
        print(f"{index+1}. {q.name} - {q.desc}")
        print("STATUS: " + ("COMPLETED" if q.completed else "IN PROGRESS"))
        print()
    try:
        choice = int(input("QUEST NUM: ")) - 1
        activeQuest = quests[choice]
        print(f"ACTIVE QUEST: {activeQuest.name}")
    except:
        print("Invalid quest.")

# COMBAT
def combat(enemy=None):
    if enemy is None:
        chosenEnemy = random.choice(enemies)
    else:
        chosenEnemy = enemy

    chosenEnemy.hp = chosenEnemy.startHP
    player.hp = player.startHP

    print(f"{chosenEnemy.name} FOUND! IT HAS {chosenEnemy.hp} HP.")

    while chosenEnemy.hp > 0 and player.hp > 0:
        player.rollAttack(chosenEnemy)

        if chosenEnemy.hp <= 0:
            print(f"You defeated {chosenEnemy.name}!")
            triggerEvent("kill", chosenEnemy.name)
            player.xp += 500
            player.checkLevelUp()
            player.money += random.randint(50, 1000)
            return
        chosenEnemy.enemyAttack(player)
        
        if player.hp <= 0:
            print("YOU DIED!")
            return

# LOCATION EVENTS
def triggerLocationEvents():
    if currentLocation.encounters:
        if random.randint(1, 3) == 1:
            enemy = random.choice(currentLocation.encounters)
            print(f"\nA {enemy.name} appears!")
            combat(enemy)

# MOVE
def move():
    global currentLocation
    print(f"\nYou are at: {currentLocation.name}")
    print(currentLocation.description)
    print("\nYou can go:")
    for direction, loc in currentLocation.connections.items():
        print(f"{direction} → {loc.name}")

    choice = input("\nWhere do you go? ").lower().strip()
    if choice in currentLocation.connections:
        currentLocation = currentLocation.connections[choice]
        print(f"\nYou travel {choice} to {currentLocation.name}.")
        triggerLocationEvents()
    else:
        print("You can't go that way.")

# SHOW INVENTORY
def mainMenuInventoryShow():
    print("\nINVENTORY:\n")
    if currentItem:
        print(f"CURRENT ITEM: {currentItem.name}")
    else:
        print("NO ITEM EQUIPPED.")
    if not player.inventory:
        print("EMPTY")
        return
    for i in player.inventory:
        player.printInventory(i)
        print("-----------------")

# SCAVENGE
def scavenge():
    if player.luck == 4 and player.luck < 6:
        itemFound = random.choice(lowLuckItems)
    elif player.luck >= 6 and player.luck < 8:
        itemFound = random.choice(medLuckItems)
    elif player.luck >= 8:
        itemFound = random.choice(highLuckItems)
    if itemFound.tag == "special":
        print(f"YOU FOUND A {itemFound.name}")
        player.inventoryHandler(itemFound)
        medLuckItems.remove(itemFound)
        highLuckItems.remove(itemFound)
    else:
        print(f"YOU FOUND A {itemFound.name}")
        player.inventoryHandler(itemFound)
    checkRickItem(itemFound)
class perkTraitDesc:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
def createTraitsPerks():
    global bruiserTrait, buissnessTrait, nerdTrait, skinnyTrait, traits
    bruiserTrait = perkTraitDesc("Bruiser", "Increases starting strength stat by 2, decreases starting intel stat by 2.")
    buissnessTrait = perkTraitDesc("Buisness Person", "Increases starting intel and skill stats by 1, decreases starting luck by 2.")
    nerdTrait = perkTraitDesc("Stereotypical Nerd", "Increases starting intel by 2, decreases strength by 2.")
    skinnyTrait = perkTraitDesc("Skinny", "Increases starting skill by 2, decreases strength by 2.")
    traits = [bruiserTrait, buissnessTrait, nerdTrait, skinnyTrait]
def createCharacter():
    nameInput = input("NAME: ")
    ageInput = int(input("AGE: "))
    genderInput = input("GENDER MALE = M, FEMALE = F, NON-BINARY = NB: ")
    player.name = nameInput
    player.age = ageInput
    player.gender = genderInput
    print("TRAITS")
    for index, trait in enumerate(traits):
        traitIndex = index + 1
        print(f"{traitIndex}. {trait.name}")
        print(f"-----{trait.desc}")
        print()
    pickTrait = int(input("TRAIT NUM: "))
    if pickTrait == 1:
        player.strength += 2
        player.intel -= 2
        print("Bruiser trait picked")
        player.trait = bruiserTrait.name
        return
    elif pickTrait == 2:
        player.intel += 1
        player.skill -= 1
        player.luck -= 2
        print("Buisness Person trait picked")
        player.trait = buissnessTrait.name
        return
    elif pickTrait == 3:
        player.strength -= 2
        player.intel += 2
        print("Nerd trait picked")
        player.trait = nerdTrait.name
        return
    elif pickTrait == 4:
        player.strength -= 2
        player.skill += 2
        print("Skinny trait picked")
        player.trait = skinnyTrait.name
        return
def saveGame():
    saveData = {
        "player": makePlayerDict(),
        "inventory": [item.name for item in player.inventory],
        "quests": [{"name": q.name, "completed": q.completed} for q in quests],
        "location": currentLocation.name,
        "rick_active": rickFound
    }

    with open("save.json", "w") as f:
        json.dump(saveData, f, indent=4)

    print("Game saved.")


def loadGame():
    global inventory, currentLocation, quests, rickFound
    try:
        with open("save.json", "r") as f:
            data = json.load(f)
    except:
        print("No save file found.")
        createCharacter()
        return

    # LOAD PLAYER
    p = data["player"]
    player.name = p["name"]
    player.hp = p["hp"]
    player.strength = p["strength"]
    player.intel = p["intel"]
    player.luck = p["luck"]
    player.skill = p["skill"]
    player.startHP = p["startHP"]
    player.level = p["level"]
    player.xp = p["xp"]
    player.armorClass = p["armor-class"]
    player.age = p["age"]
    player.gender = p["gender"]
    player.trait = p["trait"]
    player.money = p["money"]
    # LOAD INVENTORY
    inventory.clear()
    for name in data["inventory"]:
        for item in itemList:
            if item.name == name:
                player.inventory.append(item)

    # LOAD QUESTS COMPLETION
    for savedQ in data["quests"]:
        for q in quests:
            if q.name == savedQ["name"]:
                q.completed = savedQ["completed"]

    # LOAD LOCATION
    locName = data["location"]
    for loc in [shiftyShinsLocation, jerbankLocation, eastMontanaArmyBaseLocation]:
        if loc.name == locName:
            currentLocation = loc
            break
    rickFound = data["rick_active"]
    print("Game loaded.")
#RICK COMPANION
rickCompanion = Player("Rick Crass", 150, 7, 6, 8, 8, 150, 3, 0, 0, 32, None, "M", 0, [])
def rickDialogue():
    nodes = {
        "start": DialogueNode(
            id="start",
            text=f"Rick Crass: Hey, {player.name}.",
            choices=[
                DialogueChoice("Tell me about Redtown Rebels.", nextNode="red_town_info"),
                DialogueChoice("Tell me about South Territory Montana.", nextNode="south_territory_montana_info"),
                DialogueChoice("Tell me about the US army.", nextNode="us_army_info"),
                DialogueChoice("See you later.", nextNode="end")
            ]
        ),
        "red_town_info": DialogueNode(
            id="red_town_info",
            text=f"Rick Crass: The Redtown Rebels are a rebel group, based in South Territory Montana.\nThey're named after a pre-war baseball team, the Redtown Rickets.\nNot sure where Redtown is now, I think it was flattened.\n",
            choices=[
                DialogueChoice("Do you think we can find it?", nextNode="redtown_map_q"),
            ]
        ),
        "redtown_map_q": DialogueNode(
            id="redtown_map_q",
            text=f"Rick Crass: You think so? There might be a map lying around somewhere.",
            choices=[
                DialogueChoice("Alright, I'll find it.", nextNode="accept_redtown_find_q", action=lambda: quests.append(redTownMapQ)),
                DialogueChoice("Sorry, I can't do it.", nextNode="reject_redtown_find_q"),
            ]
        ),
        "accept_redtown_find_q": DialogueNode(
            id="accept_redtown_find_q",
            text=f"Rick Crass: Alright.\n QUEST ADDED: {redTownMapQ.name}",
            choices=[
                DialogueChoice("I'll get on it.", nextNode="start", action=lambda: medLuckItems.append(redTownMap) and highLuckItems.append(redTownMap)),
            ]
        ),
        "reject_redtown_find_q": DialogueNode(
            id="reject_redtown_find_q",
            text=f"Rick Crass: Oh, ok.",
            choices=[
                DialogueChoice("Ok.", nextNode="start"),
            ]
        ),
        "south_territory_montana_info": DialogueNode(
            id="south_territory_montana_info",
            text=f"Rick Crass: Down south of Montana used to be connected to the north. Then came along President Dunlop and messed it all up.",
            choices=[
                DialogueChoice("Tell me about President Dunlop.", nextNode="pres_dunlop_info"),
                DialogueChoice("Tell me more about South Territory Montana.", nextNode="more_stm_info"),
                DialogueChoice("Let's talk about something else.", nextNode="start")
            ]
        ),
        "more_stm_info": DialogueNode(
            id="more_stm_info",
            text=f"Rick Crass: STM is plagued  with violence.\nMainly between the Redtown Rebels and The U.S. Army.\nI don't think anything will get better down here.",
            choices=[
                DialogueChoice("Tell me about the Redtown Rebels.", nextNode="red_town_info"),
                DialogueChoice("Tell me about the U.S. Army.", nextNode="us_army_info"),
                DialogueChoice("Let's talk about something else.", nextNode="start")
            ]
        ),
        "pres_dunlop_info": DialogueNode(
            id="pres_dunlop_info",
            text=f"Rick Crass: President Dunlop is a crazy tyrant.\nHe has an insane fixation on controlling everything and anything that breathes or walks.\nOf course, to nurture the failing american dream,\nwhich everyone now-adays is looking for.",
            choices=[
                DialogueChoice("Let's talk about something else.", nextNode="start")
            ]
        ),
        "us_army_info": DialogueNode(
            id="us_army_info",
            text=f"Rick Crass: The U.S. Army is hellbent on controlling everything that it percieves to be dangerous.\nJust like any rebel groups that just want to stop the tyranny.",
            choices=[
                DialogueChoice("Tell me about President Dunlop.", nextNode="pres_dunlop_info"),
                DialogueChoice("Let's talk about something else.", nextNode="start")
            ]
        ),
        "end": DialogueNode(
            id="end",
            text="Rick Crass: Bye.\nYou part ways.",
            choices=[]
        ),
    }
    runDialogue(nodes, "start")

# SETUP
createItems()
createQuests()
createLocations()
createTraitsPerks()
createFactions()
class shop:
    def __init__(self, items):
        self.items = items if items else []
mainShop = shop([fortyfiveRevolver, shotgunCombat, nukeLauncher, assaultRifle, gatlingLaser, combatKnife, leatherArmour, combatArmour, xTExoArmour, xSExoArmour])
def shopMenu():
    print(f"SHOP\n")
    for index, item in enumerate(mainShop.items):
        print(f"\n{index+1}. NAME: {item.name}\nHP BOOST: {item.healthBoost}\nDL: {item.dL}, DH: {item.dH}\nARMOR CLASS: {item.armorPoints}\nDESC: {item.desc}\nCOST: ${item.cost}\n")
    print(f"PLAYER MONEY: ${player.money}")
    choice = int(input("ITEM NUM: ")) - 1
    chosenItem = mainShop.items[choice]
    if player.money >= chosenItem.cost:
        print(f"{chosenItem.name} BOUGHT FOR ${chosenItem.cost}.\nPLAYER MONEY: ${player.money-chosenItem.cost}.")
        player.money -= chosenItem.cost
        player.inventoryHandler(chosenItem)
        return
    if chosenItem.cost > player.money:
        print(f"PLAYER NEEDS MORE MONEY. CURRENT MONEY: ${player.money}")
        return
currentLocation = shiftyShinsLocation
print(f"Welcome to DIGI: A Dystopian Post-Nuclear Role-playing Game.\n(n)ew game, (l)oad game\n")
choice = input("> ")
match choice:
    case "n":
        createCharacter()
    case "l":
        loadGame()
# MAIN LOOP
run = True
while run:
    print("\n--- CRPG ---")
    print(f" 1. Move\n 2. Show Inventory\n 3. Use an Item\n 4. Quests\n 5. Janas. Almanac\n 6. Scavenge\n 7. Standalone Combat\n 8. Meet Someone \n 9. Factions\n 10. Save Game\n 11. Rick Crass\n 12. Shop")
    choice = input("> ")
    if choice == "1":
        move()
    elif choice == "2":
        mainMenuInventoryShow()
    elif choice == "3":
        player.useItem()
    elif choice == "4":
        chooseQuest()
    elif choice == "5":
        player.status()
    elif choice == "6":
        scavenge()
    elif choice == "7":
        combat()
    elif choice == "8":
        NPCRanddialogue()
    elif choice == "9":
        chooseFaction()
    elif choice == "10":
        saveGame()
    elif choice == "11":
        if rickFound == True:
            rickDialogue()
        else:
            print("Unavailable option.")
    elif choice == "12":
        shopMenu()
    elif choice == "four leaf clover":
        player.luck += 500
        print("You feel lucky...")
    elif choice == "wanna play?":
        inventory.append(nukeLauncher)
    elif choice == "ls items":
        for item in itemList:
            print(f"NAME: {item.name}")
            print(f"DH: {item.dH} DL: {item.dL}")
            print(f"HP BOOST: {item.healthBoost}")
            print(f"ARMOR POINTS: {item.armorPoints}")
            print()
    elif choice == "max verstapen":
        for l in range(99):
            player.xp = 3500
            player.checkLevelUp()
    elif choice == "rickCrassACTIVE":
        itemFound = rickEntrySlip
        checkRickItem(itemFound)
    elif choice == "medItems":
        for item in medLuckItems:
            print(f"NAME: {item.name}")
            print(f"DH: {item.dH} DL: {item.dL}")
            print(f"HP BOOST: {item.healthBoost}")
            print(f"ARMOR POINTS: {item.armorPoints}")
            print()
    elif choice == "highItems":
        for item in highLuckItems:
            print(f"NAME: {item.name}")
            print(f"DH: {item.dH} DL: {item.dL}")
            print(f"HP BOOST: {item.healthBoost}")
            print(f"ARMOR POINTS: {item.armorPoints}")
            print()
    elif choice == "rickCheck":
        print(rickFound)
    elif choice == "playerADDMONEY":
        player.money += 500000000000000000000000000
