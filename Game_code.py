import random  # Import the random module for random chance events

# Character class with attributes
class Character:
    def __init__(self, name, char_class):
        # Initialize character's name, class, health, inventory, and dark soul count
        self.name = name
        self.char_class = char_class
        self.health = 100
        self.inventory = []
        self.dark_souls = 0  # Track collected Dark Souls
        self.set_attributes()  # Set class-specific attributes

    def set_attributes(self):
        # Define attributes based on the character's chosen class
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
        # Display character stats
        print(f"\n{self.name} the {self.char_class}")
        print(f"Health: {self.health}")
        print(f"Strength: {self.strength}, Agility: {self.agility}, Magic: {self.magic}")
        print(f"Dark Souls Collected: {self.dark_souls}")

# Basic enemy class
class Enemy:
    def __init__(self, name, health, strength, agility, magic=0, poison_chance=0):
        # Initialize enemy attributes
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.magic = magic
        self.poison_chance = poison_chance

# Combat system
def combat(player, enemy):
    print(f"\nA wild {enemy.name} appears!")  # Notify player of an encounter
    poison_active = False  # Track if poison effect is active
    poison_damage = 0  # Track poison damage amount

    while player.health > 0 and enemy.health > 0:  # Combat loop while both are alive
        action = input("Choose an action (attack, defend, run): ").lower()  # Player's action choice

        if action == "attack":  # If player chooses to attack
            if random.randint(1, 10) <= player.strength:  # Determine hit based on strength
                damage = random.randint(5, 15)  # Random damage value
                enemy.health -= damage  # Reduce enemy health
                print(f"You hit the {enemy.name} for {damage} damage!")
            else:
                print("You missed!")  # Missed attack message
        elif action == "defend":  # If player chooses to defend
            print("You brace yourself for an attack.")
        elif action == "run":  # If player chooses to run
            if random.randint(1, 10) <= player.agility:  # Determine escape success based on agility
                print("You successfully escaped!")
                return  # Exit combat if escape succeeds
            else:
                print("You failed to escape!")  # Failed escape message
        
        # Enemy's turn to attack
        if enemy.health > 0:
            if enemy.magic > 0 and random.randint(1, 10) <= enemy.magic:  # Enemy magic attack
                enemy_damage = random.randint(8, 15)  # Magic damage
                print(f"The {enemy.name} casts a spell, hitting you for {enemy_damage} magic damage!")
            elif enemy.poison_chance > 0 and random.randint(1, 10) <= enemy.poison_chance:  # Poison attack
                poison_active = True  # Activate poison effect
                poison_damage = random.randint(3, 6)  # Poison damage amount
                print(f"The {enemy.name} ensnares you with poison! You'll take {poison_damage} poison damage each turn.")
            else:  # Regular physical attack
                enemy_damage = random.randint(1, enemy.strength)  # Physical damage based on strength
                print(f"The {enemy.name} hits you for {enemy_damage} physical damage!")
            player.health -= enemy_damage  # Reduce player health by enemy's attack damage

        # Apply poison damage if poison is active
        if poison_active:
            player.health -= poison_damage  # Reduce health by poison damage
            print(f"The poison hurts you for {poison_damage} damage!")

        # Display current health of player and enemy
        print(f"Your Health: {player.health}, {enemy.name} Health: {enemy.health}")

    # Outcome of combat
    if player.health <= 0:
        print("You have been defeated!")  # Player defeat message
    elif enemy.health <= 0:
        print(f"You defeated the {enemy.name}!")  # Enemy defeat message
        player.dark_souls += 1  # Gain a Dark Soul
        print("You collected a Dark Soul!")

        # Display remaining Dark Souls needed
        souls_needed = 5 - player.dark_souls
        if souls_needed > 0:
            print(f"You need {souls_needed} more Dark Souls to reach the Wretched Wasteland.")
        check_dark_souls(player)  # Check if enough Dark Souls collected

        loot = get_loot()  # Obtain loot item
        player.inventory.append(loot)  # Add loot to inventory
        print(f"You found {loot}!")

# Check if player has enough Dark Souls to transition
def check_dark_souls(player):
    if player.dark_souls >= 5:  # If player has 5 or more Dark Souls
        print("\nYou've collected 5 Dark Souls! You feel a dark energy pulling you...")
        print("You are transported to a new environment: The Wretched Wasteland.")
        player.dark_souls = 0  # Reset Dark Soul count

# Loot system: random weapons or armor
def get_loot():
    # Define possible loot items
    loot_items = [
        {"name": "Iron Sword", "type": "weapon", "strength_boost": 3},
        {"name": "Steel Shield", "type": "armor", "health_boost": 10},
        {"name": "Magic Amulet", "type": "weapon", "strength_boost": 2, "health_boost": 5},
        {"name": "Leather Armor", "type": "armor", "health_boost": 8}
    ]
    return random.choice(loot_items)  # Return a random loot item

# World progression
def explore_area(player):
    print("\nYou venture into the Forgotten Forest.")  # Exploration message
    encounter = random.choice(["goblin", "dark_wolf", "shadow_mage", "vine_beast", "item", "nothing"])  # Random encounter

    # Different encounters with different enemies
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
        item = random.choice(["Potion", "Magic Scroll", "Dagger"])  # Random item found
        player.inventory.append(item)  # Add item to inventory
        print(f"You found a {item}!")
    else:
        print("The forest is eerily quiet...")  # No encounter

# Inventory management
def manage_inventory(player):
    print("\nInventory:")  # Display inventory contents
    for i, item in enumerate(player.inventory):  # List items
        if isinstance(item, dict):  # If item is a dictionary (e.g., loot)
            item_description = f"{item['name']} (Boost: "
            if 'strength_boost' in item:
                item_description += f"Strength +{item['strength_boost']} "
            if 'health_boost' in item:
                item_description += f"Health +{item['health_boost']}"
            item_description += ")"
        else:
            item_description = item
        print(f"{i + 1}. {item_description}")

    # Action for using or discarding an item
    action = input("Would you like to (use, discard) an item or (exit)? ").lower()
    if action in ["use", "discard"]:
        try:
            item_choice = int(input("Choose item number: ")) - 1
            if 0 <= item_choice < len(player.inventory):  # Check if choice is valid
                item = player.inventory.pop(item_choice)  # Remove item from inventory
                if action == "use":
                    # Apply item effect if item is a dictionary
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
    # Determine outcome based on player's final health
    if player.health > 70:
        print("You emerge from the adventure victorious and healthy!")
    elif 30 <= player.health <= 70:
        print("You survived, but with heavy injuries.")
    else:
        print("You barely made it out alive. This journey has taken a toll on you.")

# Main game loop
def main():
    print("Welcome to the Text-Based RPG!")  # Introduction message

    # Character creation
    name = input("Enter your character's name: ")
    char_class = input("Choose a class (Warrior, Mage, Rogue): ").capitalize()  # Player chooses class
    if char_class not in ["Warrior", "Mage", "Rogue"]:
        print("Invalid class choice. Defaulting to Warrior.")  # Default class if invalid input
        char_class = "Warrior"

    player = Character(name, char_class)  # Create character object
    player.display_stats()  # Display character's initial stats

    # Main gameplay loop
    while player.health > 0:
        print("\nWhat would you like to do?")
        choice = input("Options: explore, inventory, stats, quit: ").lower()  # Player's choice of action

        # Respond to player's choice
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
        game_ending(player)  # Display end message based on health

if __name__ == "__main__":
    main()  # Run the game
