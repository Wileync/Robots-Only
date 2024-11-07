import random

# Character class with attributes
class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.health = 100
        self.inventory = []
        self.dark_souls = 0  # Track Dark Souls
        self.set_attributes()

    def set_attributes(self):
        if self.char_class == "Warrior":
            self.strength = 10
            self.agility = 5
            self.magic = 2
        elif self.char_class == "Mage":
            self.strength = 2
            self.agility = 5
            self.magic = 10
        elif self.char_class == "Rogue":
            self.strength = 5
            self.agility = 10
            self.magic = 3

    def display_stats(self):
        print(f"\n{self.name} the {self.char_class}")
        print(f"Health: {self.health}")
        print(f"Strength: {self.strength}, Agility: {self.agility}, Magic: {self.magic}")
        print(f"Dark Souls Collected: {self.dark_souls}")

# Basic enemy class
class Enemy:
    def __init__(self, name, health, strength, agility, magic=0, poison_chance=0):
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.magic = magic
        self.poison_chance = poison_chance

# Combat system
def combat(player, enemy):
    print(f"\nA wild {enemy.name} appears!")
    poison_active = False
    poison_damage = 0

    while player.health > 0 and enemy.health > 0:
        action = input("Choose an action (attack, defend, run): ").lower()
        
        if action == "attack":
            if random.randint(1, 10) <= player.strength:
                damage = random.randint(5, 15)
                enemy.health -= damage
                print(f"You hit the {enemy.name} for {damage} damage!")
            else:
                print("You missed!")
        elif action == "defend":
            print("You brace yourself for an attack.")
        elif action == "run":
            if random.randint(1, 10) <= player.agility:
                print("You successfully escaped!")
                return
            else:
                print("You failed to escape!")
        
        # Enemy attacks
        if enemy.health > 0:
            if enemy.magic > 0 and random.randint(1, 10) <= enemy.magic:
                enemy_damage = random.randint(8, 15)
                print(f"The {enemy.name} casts a spell, hitting you for {enemy_damage} magic damage!")
            elif enemy.poison_chance > 0 and random.randint(1, 10) <= enemy.poison_chance:
                poison_active = True
                poison_damage = random.randint(3, 6)
                print(f"The {enemy.name} ensnares you with poison! You'll take {poison_damage} poison damage each turn.")
            else:
                enemy_damage = random.randint(1, enemy.strength)
                print(f"The {enemy.name} hits you for {enemy_damage} physical damage!")
            player.health -= enemy_damage

        # Apply poison damage if active
        if poison_active:
            player.health -= poison_damage
            print(f"The poison hurts you for {poison_damage} damage!")

        print(f"Your Health: {player.health}, {enemy.name} Health: {enemy.health}")

    if player.health <= 0:
        print("You have been defeated!")
    elif enemy.health <= 0:
        print(f"You defeated the {enemy.name}!")
        player.dark_souls += 1  # Gain a Dark Soul upon defeating an enemy
        print("You collected a Dark Soul!")

        # Display how many more Dark Souls are needed
        souls_needed = 5 - player.dark_souls
        if souls_needed > 0:
            print(f"You need {souls_needed} more Dark Souls to reach the Wretched Wasteland.")
        check_dark_souls(player)  # Check if the player has enough Dark Souls to transition environments
        
        loot = get_loot()
        player.inventory.append(loot)
        print(f"You found {loot}!")

# Check if player has enough Dark Souls to transition
def check_dark_souls(player):
    if player.dark_souls >= 5:
        print("\nYou've collected 5 Dark Souls! You feel a dark energy pulling you...")
        print("You are transported to a new environment: The Wretched Wasteland.")
        player.dark_souls = 0  # Reset Dark Souls count

# Loot system: random weapons or armor
def get_loot():
    loot_items = [
        {"name": "Iron Sword", "type": "weapon", "strength_boost": 3},
        {"name": "Steel Shield", "type": "armor", "health_boost": 10},
        {"name": "Magic Amulet", "type": "weapon", "strength_boost": 2, "health_boost": 5},
        {"name": "Leather Armor", "type": "armor", "health_boost": 8}
    ]
    return random.choice(loot_items)

# World progression
def explore_area(player):
    print("\nYou venture into the Forgotten Forest.")
    encounter = random.choice(["goblin", "dark_wolf", "shadow_mage", "vine_beast", "item", "nothing"])
    
    if encounter == "goblin":
        enemy = Enemy("Goblin", 30, 5, 3)
        combat(player, enemy)
    elif encounter == "dark_wolf":
        enemy = Enemy("Dark Wolf", 40, 7, 4)
        combat(player, enemy)
    elif encounter == "shadow_mage":
        enemy = Enemy("Shadow Mage", 35, 3, 5, magic=10)
        combat(player, enemy)
    elif encounter == "vine_beast":
        enemy = Enemy("Vine Beast", 50, 6, 2, poison_chance=3)
        combat(player, enemy)
    elif encounter == "item":
        item = random.choice(["Potion", "Magic Scroll", "Dagger"])
        player.inventory.append(item)
        print(f"You found a {item}!")
    else:
        print("The forest is eerily quiet...")

# Inventory management
def manage_inventory(player):
    print("\nInventory:")
    for i, item in enumerate(player.inventory):
        if isinstance(item, dict):  # Loot items as dictionaries
            item_description = f"{item['name']} (Boost: "
            if 'strength_boost' in item:
                item_description += f"Strength +{item['strength_boost']} "
            if 'health_boost' in item:
                item_description += f"Health +{item['health_boost']}"
            item_description += ")"
        else:
            item_description = item
        print(f"{i + 1}. {item_description}")
    
    action = input("Would you like to (use, discard) an item or (exit)? ").lower()
    if action in ["use", "discard"]:
        try:
            item_choice = int(input("Choose item number: ")) - 1
            if 0 <= item_choice < len(player.inventory):
                item = player.inventory.pop(item_choice)
                if action == "use":
                    if isinstance(item, dict):
                        if "strength_boost" in item:
                            player.strength += item["strength_boost"]
                            print(f"Your strength increased by {item['strength_boost']}!")
                        if "health_boost" in item:
                            player.health += item["health_boost"]
                            print(f"Your health increased by {item['health_boost']}!")
                    else:
                        print(f"You use the {item}.")
                        if item == "Potion":
                            player.health += 20
                            print("Your health is restored by 20 points!")
                else:
                    print(f"You discarded the {item}.")
            else:
                print("Invalid item number.")
        except ValueError:
            print("Please enter a valid number.")

# Game ending based on choices
def game_ending(player):
    if player.health > 70:
        print("You emerge from the adventure victorious and healthy!")
    elif 30 <= player.health <= 70:
        print("You survived, but with heavy injuries.")
    else:
        print("You barely made it out alive. This journey has taken a toll on you.")

# Main game loop
def main():
    print("Welcome to the Text-Based RPG!")
    
    # Character creation
    name = input("Enter your character's name: ")
    char_class = input("Choose a class (Warrior, Mage, Rogue): ").capitalize()
    if char_class not in ["Warrior", "Mage", "Rogue"]:
        print("Invalid class choice. Defaulting to Warrior.")
        char_class = "Warrior"
    
    player = Character(name, char_class)
    player.display_stats()

    # Main gameplay loop
    while player.health > 0:
        print("\nWhat would you like to do?")
        choice = input("Options: explore, inventory, stats, quit: ").lower()
        
        if choice == "explore":
            explore_area(player)
        elif choice == "inventory":
            manage_inventory(player)
        elif choice == "stats":
            player.display_stats()
        elif choice == "quit":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

    # End game after health reaches 0
    if player.health <= 0:
        print("Game over! You have been defeated.")
        game_ending(player)

if __name__ == "__main__":
    main()