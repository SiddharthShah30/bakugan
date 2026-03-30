import random

def show_main_menu():
    print("""
============================
   BAKUGAN BRAWLERS GAME
============================
1. Start Game
2. Instructions
3. Credits
4. Exit
============================
    """)
    while True:
        choice = input("Select an option (1-4): ")
        if choice == '1':
            return 'start'
        elif choice == '2':
            show_instructions()
        elif choice == '3':
            show_credits()
        elif choice == '4':
            print("Goodbye, Brawler!")
            exit()
        else:
            print("Invalid option. Please choose 1-4.")

def show_instructions():
    print("""
--- INSTRUCTIONS ---
Welcome to Bakugan Brawlers!
1. Each player selects a team of Bakugan.
2. Take turns attacking, using items, or switching Bakugan.
3. The player with the last Bakugan standing wins!
4. Use strategy: each Bakugan has strengths and weaknesses.
5. More features and Bakugan coming soon!
Press Enter to return to the main menu.
    """)
    input()

def show_credits():
    print("""
--- CREDITS ---
Bakugan Brawlers Game
Created by: Your Name
Inspired by Bakugan franchise
2026
Press Enter to return to the main menu.
    """)
    input()

def main():
    while True:
        action = show_main_menu()
        if action == 'start':
            game_loop()

def game_loop():
    # ...existing code...

    # (Everything from the old game setup and play_game logic goes here)

    # --- REPLAY LOGIC ---
    while True:
        play_game()
        replay = input("\nDo you want to play another match? (yes/no): ").lower()
        if replay != "yes":
            print("BRAWL TERMINATED. Goodbye!")
            break

# --- OLD CODE BELOW (to be moved into game_loop) ---


# --- GAME CLASSES AND LOGIC ---

class Bakugan:
    def __init__(self, name, attribute, level=5, special_attack=None, special_desc="", special_power=0):
        self.name = name
        self.level = level
        self.attribute = attribute
        self.health = level * 6
        self.max_health = level * 6
        self.is_knocked_out = False
        self.special_attack = special_attack
        self.special_desc = special_desc
        self.special_power = special_power

    def __repr__(self):
        return f"{self.name} (Lv{self.level}, {self.attribute}) | HP: {self.health}/{self.max_health} | Special: {self.special_attack or 'None'}"

    def revive(self):
        self.is_knocked_out = False
        if self.health == 0:
            self.health = 1
        print(f"{self.name} has been revived with {self.health} health.")

    def knock_out(self):
        self.is_knocked_out = True
        if self.health != 0:
            self.health = 0
        print(f"{self.name} has been knocked out.")

    def lose_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.knock_out()
        else:
            print(f"{self.name} now has {self.health} health.")

    def gain_health(self, amount):
        if self.health == 0:
            self.revive()
        self.health += amount
        if self.health >= self.max_health:
            self.health = self.max_health
        print(f"{self.name} now has {self.health} health.")

    def attack(self, other_bakugan):
        if self.is_knocked_out:
            print(f"{self.name} can't attack because it is knocked out.")
            return
        # Type effectiveness
        if (self.attribute == "Pyrus" and other_bakugan.attribute == "Aquos") or (self.attribute == "Aquos" and other_bakugan.attribute == "Subterra") or (self.attribute == "Subterra" and other_bakugan.attribute == "Pyrus"):
            print(f"{self.name} attacks {other_bakugan.name} for damage {round(self.level * 0.5)} (not effective!)")
            other_bakugan.lose_health(round(self.level * 0.5))
        elif (self.attribute == other_bakugan.attribute):
            print(f"{self.name} attacks {other_bakugan.name} for damage {self.level} (effective!)")
            other_bakugan.lose_health(self.level)
        elif (self.attribute == "Pyrus" and other_bakugan.attribute == "Subterra") or (self.attribute == "Aquos" and other_bakugan.attribute == "Pyrus") or (self.attribute == "Subterra" and other_bakugan.attribute == "Aquos"):
            print(f"{self.name} attacks {other_bakugan.name} for damage {self.level * 2} (super effective!)")
            other_bakugan.lose_health(self.level * 2)
        else:
            print(f"{self.name} attacks {other_bakugan.name} for damage {self.level}")
            other_bakugan.lose_health(self.level)

    def use_special(self, other_bakugan):
        if self.is_knocked_out:
            print(f"{self.name} can't use special because it is knocked out.")
            return
        if not self.special_attack:
            print(f"{self.name} has no special attack!")
            return
        print(f"{self.name} uses SPECIAL ATTACK: {self.special_attack}! {self.special_desc}")
        other_bakugan.lose_health(self.special_power)

class Trainer:
    def __init__(self, bakugan_list, num_potions, name, character=None):
        self.bakugans = bakugan_list
        self.potions = num_potions
        self.current_bakugan = 0
        self.name = name
        self.character = character
        self.items = {"Potion": num_potions, "Shield": 1}

    def __repr__(self):
        print(f"{self.name} ({self.character or 'No Character'}) has {len(self.bakugans)} bakugans, {self.potions} potions and the current bakugan is {self.bakugans[self.current_bakugan].name}.")
        for bakugan in self.bakugans:
            print(bakugan)
        return f"The current active Bakugan is {self.bakugans[self.current_bakugan].name}"

    def switch_active_bakugan(self, new_active):
        if new_active < len(self.bakugans) and new_active >= 0:
            if self.bakugans[new_active].is_knocked_out:
                print(f"{self.bakugans[new_active].name} is knocked out. You can't make it your active bakugan")
            elif new_active == self.current_bakugan:
                print(f"{self.bakugans[self.current_bakugan].name} is already your active bakugan")
            else:
                self.current_bakugan = new_active
                print(f"Go {self.bakugans[self.current_bakugan].name}, it's your turn!")

    def use_item(self, item):
        if item == "Potion" and self.items.get("Potion", 0) > 0:
            print(f"You used a potion on {self.bakugans[self.current_bakugan].name}.")
            self.bakugans[self.current_bakugan].gain_health(10)
            self.items["Potion"] -= 1
        elif item == "Shield" and self.items.get("Shield", 0) > 0:
            print(f"You used a shield! {self.bakugans[self.current_bakugan].name} will take half damage next attack.")
            self.items["Shield"] -= 1
            self.bakugans[self.current_bakugan].shielded = True
        else:
            print(f"You don't have any more {item}s")

    def attack_other_trainer(self, other_trainer, use_special=False):
        my_bakugan = self.bakugans[self.current_bakugan]
        their_bakugan = other_trainer.bakugans[other_trainer.current_bakugan]
        if use_special:
            my_bakugan.use_special(their_bakugan)
        else:
            my_bakugan.attack(their_bakugan)

def game_loop():
    # Expanded Bakugan Roster
    bakugan_roster = [
        Bakugan("Dragonoid", "Pyrus", 7, "Dragon Fire", "A fiery blast that scorches the foe!", 15),
        Bakugan("Atmos", "Pyrus", 9, "Meteor Strike", "Summons a meteor for massive damage!", 18),
        Bakugan("Tigrerra", "Aquos", 6, "Aqua Shield", "Reduces next damage taken by half.", 0),
        Bakugan("Balista", "Aquos", 8, "Tidal Wave", "A huge wave crashes into the enemy!", 14),
        Bakugan("Centipoid", "Subterra", 5, "Earthquake", "Shakes the ground, damaging all!", 12),
        Bakugan("Clawsaurus", "Subterra", 10, "Stone Crush", "Crushes the foe with boulders!", 20),
        Bakugan("Skyress", "Ventus", 8, "Wind Cutter", "Sharp wind blades slice the enemy!", 13),
        Bakugan("Hydranoid", "Darkus", 9, "Shadow Burst", "A burst of dark energy!", 17),
        Bakugan("Preyas", "Aquos", 7, "Bubble Trap", "Traps foe in a bubble, reducing their next attack.", 0),
        Bakugan("Gorem", "Subterra", 8, "Rock Slam", "Slams the ground with rocks!", 16),
        Bakugan("El Condor", "Ventus", 6, "Gale Force", "A powerful gust knocks back the foe!", 11),
        Bakugan("Fear Ripper", "Darkus", 7, "Night Slash", "A quick, shadowy slash!", 14),
    ]

    # Expanded Character Roster
    character_roster = [
        "Dan Kuso", "Shun Kazami", "Marucho Marukura", "Runo Misaki", "Julie Makimoto", "Masquerade"
    ]

    print("Welcome to Bakugan! Choose your characters.")
    for i, char in enumerate(character_roster):
        print(f"{i+1}: {char}")
    trainer_one_char = character_roster[int(input("Player One, pick your character (number): "))-1]
    trainer_two_char = character_roster[int(input("Player Two, pick your character (number): "))-1]

    trainer_one_name = input("Enter a name for Player One: ")
    trainer_two_name = input("Enter a name for Player Two: ")

    # Bakugan Selection (each player picks 3)
    print("\nBakugan Roster:")
    for i, b in enumerate(bakugan_roster):
        print(f"{i+1}: {b}")
    trainer_one_bakugan = []
    trainer_two_bakugan = []
    print("\nPlayer One, pick 3 Bakugan by number (separated by spaces):")
    picks = input().split()
    for p in picks[:3]:
        trainer_one_bakugan.append(bakugan_roster[int(p)-1])
    print("\nPlayer Two, pick 3 Bakugan by number (separated by spaces):")
    picks = input().split()
    for p in picks[:3]:
        trainer_two_bakugan.append(bakugan_roster[int(p)-1])

    trainer_one = Trainer(trainer_one_bakugan, 3, trainer_one_name, trainer_one_char)
    trainer_two = Trainer(trainer_two_bakugan, 3, trainer_two_name, trainer_two_char)

    print("\nLet's get ready to fight! Here are our two trainers:")
    print(trainer_one)
    print()
    print(trainer_two)

    def play_game():
        # --- RESET TEAMS ---
        for b in trainer_one_bakugan + trainer_two_bakugan:
            b.health = b.max_health
            b.is_knocked_out = False
            b.shielded = False
        trainer_one = Trainer(trainer_one_bakugan, 3, trainer_one_name, trainer_one_char)
        trainer_two = Trainer(trainer_two_bakugan, 3, trainer_two_name, trainer_two_char)
        for round_num in range(1, 4):
            print(f"\n{'='*30}")
            print(f"       ROUND {round_num} / 3")
            print(f"{'='*30}")
            for t, opp in [(trainer_one, trainer_two), (trainer_two, trainer_one)]:
                active = t.bakugans[t.current_bakugan]
                print(f"\n>> {t.name}'s turn!")
                print(f"Active Bakugan: {active}")
                print("Options: 1) Attack  2) Special  3) Use Item  4) Switch Bakugan")
                move = input("Choose your action (1-4): ")
                if move == '1':
                    t.attack_other_trainer(opp)
                elif move == '2':
                    t.attack_other_trainer(opp, use_special=True)
                elif move == '3':
                    print(f"Items: {t.items}")
                    item = input("Which item? (Potion/Shield): ")
                    t.use_item(item)
                elif move == '4':
                    print("Select a Bakugan:")
                    for i, b in enumerate(t.bakugans):
                        print(f"{i}: {b.name} ({b.health} HP)")
                    try:
                        choice = int(input("Enter number: "))
                        t.switch_active_bakugan(choice)
                    except:
                        print("Invalid choice, staying with current Bakugan.")
                else:
                    print("Invalid move. Skipping turn.")
            # Status
            print("\n" + "-"*15 + " CURRENT STATUS " + "-"*15)
            for t in [trainer_one, trainer_two]:
                ko_names = [b.name for b in t.bakugans if b.is_knocked_out]
                print(f"{t.name}: Active HP: {t.bakugans[t.current_bakugan].health} | KOs: {len(ko_names)} ({', '.join(ko_names) if ko_names else 'None'})")
        # --- WINNER DETERMINATION ---
        print("\n" + "#"*40)
        print("           FINAL JUDGMENT")
        print("#"*40)
        t1_kos = sum(1 for b in trainer_one.bakugans if b.is_knocked_out)
        t2_kos = sum(1 for b in trainer_two.bakugans if b.is_knocked_out)
        t1_hp = sum(b.health for b in trainer_one.bakugans)
        t2_hp = sum(b.health for b in trainer_two.bakugans)
        if t1_kos < t2_kos:
            print(f"VICTORY FOR {trainer_one.name.upper()}! (Fewer KOs)")
        elif t2_kos < t1_kos:
            print(f"VICTORY FOR {trainer_two.name.upper()}! (Fewer KOs)")
        else:
            if t1_hp > t2_hp:
                print(f"VICTORY FOR {trainer_one.name.upper()}! (Higher Total HP)")
            elif t2_hp > t1_hp:
                print(f"VICTORY FOR {trainer_two.name.upper()}! (Higher Total HP)")
            else:
                print("IT'S A COMPLETE TIE!")
    while True:
        play_game()
        replay = input("\nDo you want to play another match? (yes/no): ").lower()
        if replay != "yes":
            print("BRAWL TERMINATED. Goodbye!")
            break

# --- RUN MAIN MENU ---
if __name__ == "__main__":
    main()