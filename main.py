from __future__ import annotations

import copy
import os
import random
import time
from dataclasses import dataclass, field


ATTRIBUTE_ORDER = ["Pyrus", "Aquos", "Subterra", "Ventus", "Darkus", "Haos"]
TYPE_CHART = {
    ("Pyrus", "Aquos"): 1.4,
    ("Aquos", "Subterra"): 1.4,
    ("Subterra", "Ventus"): 1.4,
    ("Ventus", "Darkus"): 1.4,
    ("Darkus", "Haos"): 1.4,
    ("Haos", "Pyrus"): 1.4,
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause(message="Press Enter to continue..."):
    input(f"\n{message}")


def wait(duration=0.12):
    time.sleep(duration)


def line(char="=", width=76):
    return char * width


def header(title):
    print("\n" + line())
    print(title.center(76))
    print(line())


def section(title):
    print("\n" + title)
    print("-" * len(title))


def cinematic_frame(top_text, middle_text="", bottom_text=""):
    clear_screen()
    print(line())
    print(top_text.center(76))
    if middle_text:
        print(middle_text.center(76))
    if bottom_text:
        print(bottom_text.center(76))
    print(line())


def animate_sequence(frames, delay=0.15, final_pause=False):
    for frame in frames:
        clear_screen()
        print(frame)
        wait(delay)
    if final_pause:
        pause()


def render_title_art():
        print(r"""
     ____   ___    _    _   _  _   _   ____   _____   ____   ______   _   _
    | __ ) / _ \  | |  | | | || | | | / ___| | ____| |  _ \ |___  /  | | | |
    |  _ \| | | | | |  | | | || |_| || |  _  |  _|   | |_) |  / /   | |_| |
    | |_) | |_| | | |__| | |__   _  || |_| | | |___  |  _ <  / /_   |  _  |
    |____/ \___/   \____/     |_| |_| \____| |_____| |_| \_\/____|  |_| |_|
        """)
        print("""
                                     B A K U G A N   :   B A T T L E   D I M E N S I O N
                                I N   S H A D O W   A N D   S I L V E R   T O N E S
        """)


def render_battle_banner(trainer_one, trainer_two, battle):
    clear_screen()
    print(line())
    print(f"ROUND {battle.round_number} - {battle.gate_card.name}".center(76))
    print(line())
    print(f"GATE CARD: {battle.gate_card.description}")
    print(line("-"))
    left = f"{trainer_one.name} [{trainer_one.character.name}]"
    right = f"{trainer_two.name} [{trainer_two.character.name}]"
    print(left.ljust(38) + right.rjust(38))
    print(f"{trainer_one.active().name} vs {trainer_two.active().name}".center(76))
    print(line("-"))


def animate_bakugan_entry(bakugan, side="left"):
    slides = [
        f"[{bakugan.name}]",
        f"    [{bakugan.name}]",
        f"        [{bakugan.name}]",
        f"            [{bakugan.name}]",
        f"                [{bakugan.name}]",
    ]
    if side == "right":
        slides = [frame.rjust(76) for frame in slides]
    animate_sequence(slides, delay=0.08)


def animate_attack(attacker_name, defender_name, move_name):
    frames = [
        f"{attacker_name} prepares {move_name}",
        f"{attacker_name} >>>                {defender_name}",
        f"{attacker_name} >>>>>>>>>>>>       {defender_name}",
        f"{attacker_name} >>>>>>>>>>>>>>>>>>> {defender_name}",
        f"{defender_name} reels from the impact!",
    ]
    animate_sequence(frames, delay=0.09)


def animate_status_shift(message):
    frames = [
        message,
        f"{message}.",
        f"{message}..",
        f"{message}...",
    ]
    animate_sequence(frames, delay=0.08)


def play_sound(tag, detail=""):
    suffix = f" - {detail}" if detail else ""
    print(f"[SFX] {tag}{suffix}")


def play_impact_sound(kind="hit"):
    sound_map = {
        "hit": "THUD",
        "crit": "KRAK",
        "heal": "SHIIINE",
        "shield": "WHUM",
        "burn": "FWOOSH",
        "energy": "VMMM",
        "stun": "BZZT",
    }
    play_sound(sound_map.get(kind, "THUD"))


def ask_choice(prompt, options):
    normalized = {str(index + 1): option for index, option in enumerate(options)}
    while True:
        if prompt:
            print(prompt)
        for index, option in enumerate(options, start=1):
            print(f"  {index}. {option}")
        choice = input("Select an option: ").strip()
        if choice in normalized:
            return normalized[choice]
        print("Invalid choice. Try again.")


def ask_int(prompt, minimum, maximum):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            number = int(value)
            if minimum <= number <= maximum:
                return number
        print(f"Enter a number between {minimum} and {maximum}.")


@dataclass(frozen=True)
class Ability:
    name: str
    cost: int
    kind: str
    power: int
    description: str


@dataclass(frozen=True)
class GateCard:
    name: str
    description: str
    attack_bonus: dict[str, float] = field(default_factory=dict)
    defense_bonus: dict[str, float] = field(default_factory=dict)
    energy_bonus: int = 0


@dataclass(frozen=True)
class Character:
    name: str
    title: str
    bonus_text: str
    attack_bonus_attribute: str | None = None
    attack_bonus_multiplier: float = 1.0
    heal_bonus: int = 0
    energy_bonus: int = 0
    speed_bonus: int = 0
    crit_bonus: float = 0.0
    potion_bonus: int = 0
    shield_bonus: int = 0
    discount_attribute: str | None = None


@dataclass
class Bakugan:
    name: str
    attribute: str
    power: int
    stamina: int
    speed: int
    abilities: list[Ability]

    def __post_init__(self):
        self.max_health = 42 + self.power * 4 + self.stamina * 2
        self.health = self.max_health
        self.max_energy = 5 + self.power // 2
        self.energy = 2
        self.shield_turns = 0
        self.stun_turns = 0
        self.burn_turns = 0

    def clone(self):
        return copy.deepcopy(self)

    def is_alive(self):
        return self.health > 0

    def reset(self):
        self.health = self.max_health
        self.energy = 2
        self.shield_turns = 0
        self.stun_turns = 0
        self.burn_turns = 0

    def card(self):
        return f"{self.name} [{self.attribute}] HP {self.health}/{self.max_health} EN {self.energy}/{self.max_energy}"

    def status_line(self):
        statuses = []
        if self.shield_turns:
            statuses.append(f"Shield {self.shield_turns}")
        if self.stun_turns:
            statuses.append(f"Stun {self.stun_turns}")
        if self.burn_turns:
            statuses.append(f"Burn {self.burn_turns}")
        return ", ".join(statuses) if statuses else "None"

    def gain_energy(self, amount):
        self.energy = min(self.max_energy, self.energy + amount)

    def heal(self, amount):
        if self.health <= 0:
            self.health = 1
        self.health = min(self.max_health, self.health + amount)

    def take_damage(self, amount):
        damage = max(1, amount)
        if self.shield_turns > 0:
            damage = max(1, damage // 2)
            self.shield_turns -= 1
            print(f"{self.name}'s shield reduced the damage.")
        reduced = max(0, damage - max(0, self.stamina // 3))
        self.health = max(0, self.health - reduced)
        print(f"{self.name} took {reduced} damage.")
        if self.health == 0:
            print(f"{self.name} has been knocked out!")

    def type_multiplier_against(self, other):
        return TYPE_CHART.get((self.attribute, other.attribute), 1.0)

    def basic_attack_damage(self, other, trainer, battle):
        damage = self.power + 6 + random.randint(0, 4)
        damage = int(damage * self.type_multiplier_against(other))
        damage = int(damage * battle.gate_card.attack_bonus.get(self.attribute, 1.0))
        damage = int(damage * battle.gate_card.defense_bonus.get(other.attribute, 1.0))

        if trainer.character.attack_bonus_attribute == self.attribute:
            damage = int(damage * trainer.character.attack_bonus_multiplier)

        if trainer.character.discount_attribute == self.attribute:
            damage += 1

        if random.random() < (0.08 + trainer.character.crit_bonus):
            damage = int(damage * 1.5)
            print("Critical hit!")

        return max(1, damage)

    def start_turn(self):
        if self.burn_turns > 0:
            self.health = max(0, self.health - 3)
            self.burn_turns -= 1
            print(f"{self.name} suffers burn damage.")

    def use_basic_attack(self, other, trainer, battle):
        if self.energy < 1:
            play_sound("DRIFT", f"{self.name} is out of energy")
            print(f"{self.name} is too low on energy. It regains 1 energy instead.")
            self.gain_energy(1)
            return

        self.energy -= 1
        damage = self.basic_attack_damage(other, trainer, battle)
        play_impact_sound("hit")
        animate_attack(self.name, other.name, "BATTLE CLAW")
        print(f"{self.name} uses a basic attack on {other.name} for {damage} damage.")
        other.take_damage(damage)

    def use_ability(self, index, other, trainer, battle):
        if index < 0 or index >= len(self.abilities):
            print("Invalid ability choice.")
            return

        ability = self.abilities[index]
        cost = max(1, ability.cost - (1 if trainer.character.discount_attribute == self.attribute else 0))
        if self.energy < cost:
            play_sound("DRIFT", f"{self.name} cannot pay the energy cost")
            print(f"Not enough energy for {ability.name}.")
            return

        self.energy -= cost
        play_sound("CALL", ability.name)
        animate_attack(self.name, other.name, ability.name)
        print(f"{self.name} uses {ability.name}: {ability.description}")

        if ability.kind == "damage":
            damage = int((self.power + ability.power + random.randint(1, 5)) * self.type_multiplier_against(other))
            damage = int(damage * battle.gate_card.attack_bonus.get(self.attribute, 1.0))
            if trainer.character.attack_bonus_attribute == self.attribute:
                damage = int(damage * trainer.character.attack_bonus_multiplier)
            play_impact_sound("crit" if damage >= other.health else "hit")
            other.take_damage(damage)
        elif ability.kind == "heal":
            heal_amount = ability.power + trainer.character.heal_bonus
            play_impact_sound("heal")
            animate_status_shift(f"{self.name} channels recovery energy")
            self.heal(heal_amount)
            print(f"{self.name} healed {heal_amount} HP.")
        elif ability.kind == "shield":
            play_impact_sound("shield")
            animate_status_shift(f"{self.name} raises a guard barrier")
            self.shield_turns += 1
            print(f"{self.name} gained a shield.")
        elif ability.kind == "stun":
            play_impact_sound("stun")
            animate_status_shift(f"{other.name} is trapped by the hit")
            other.stun_turns += 1
            print(f"{other.name} is stunned.")
        elif ability.kind == "burn":
            play_impact_sound("burn")
            animate_status_shift(f"{other.name} is engulfed in heat")
            other.burn_turns += 2
            print(f"{other.name} is burning.")
        elif ability.kind == "energy":
            play_impact_sound("energy")
            animate_status_shift(f"{self.name} gathers energy from the gate")
            self.gain_energy(ability.power)
            print(f"{self.name} regained {ability.power} energy.")


@dataclass
class Trainer:
    name: str
    character: Character
    team: list[Bakugan]
    is_ai: bool = False

    def __post_init__(self):
        self.active_index = 0
        self.items = {
            "Potion": 2 + self.character.potion_bonus,
            "Shield": 1 + self.character.shield_bonus,
            "Energy Drink": 1,
            "Revive": 1,
        }

    def active(self):
        return self.team[self.active_index]

    def has_available(self):
        return any(bakugan.is_alive() for bakugan in self.team)

    def available_indices(self):
        return [index for index, bakugan in enumerate(self.team) if bakugan.is_alive()]

    def auto_switch_if_needed(self):
        if self.active().is_alive():
            return
        options = self.available_indices()
        if not options:
            return
        self.active_index = options[0]
        print(f"{self.name} sends out {self.active().name}!")

    def choose_active(self):
        options = self.available_indices()
        if len(options) <= 1:
            print("No other Bakugan are available to switch.")
            return

        section(f"{self.name}'s Team")
        for index in options:
            marker = " (Active)" if index == self.active_index else ""
            print(f"{index + 1}. {self.team[index].card()}{marker}")

        while True:
            choice = ask_int("Choose a Bakugan number: ", 1, len(self.team)) - 1
            if choice in options and choice != self.active_index:
                self.active_index = choice
                print(f"{self.name} switched to {self.active().name}.")
                return
            print("That Bakugan is unavailable or already active.")

    def summary(self):
        print(f"{self.name} - {self.character.name} ({self.character.title})")
        print(f"Items: {self.items}")
        for index, bakugan in enumerate(self.team, start=1):
            marker = " [Active]" if bakugan == self.active() else ""
            print(f"  {index}. {bakugan.card()}{marker} | Status: {bakugan.status_line()}")


@dataclass
class BattleState:
    gate_card: GateCard
    round_number: int = 1


def build_abilities():
    return {
        "Blaze Cannon": Ability("Blaze Cannon", 2, "damage", 12, "A straight Pyrus blast."),
        "Phoenix Burst": Ability("Phoenix Burst", 3, "burn", 10, "A surge of flame that scorches the opponent."),
        "Dragon Guard": Ability("Dragon Guard", 2, "shield", 0, "Wraps the Bakugan in burning armor."),
        "Meteor Strike": Ability("Meteor Strike", 3, "damage", 15, "A powerful meteor crash."),
        "Solar Charge": Ability("Solar Charge", 2, "energy", 2, "Absorbs energy from the arena."),
        "Inferno Spiral": Ability("Inferno Spiral", 4, "damage", 18, "A heavy rotating fire assault."),
        "Aqua Cannon": Ability("Aqua Cannon", 2, "damage", 11, "Pressurized water blast."),
        "Tidal Shield": Ability("Tidal Shield", 2, "shield", 0, "A protective barrier of water."),
        "Bubble Prison": Ability("Bubble Prison", 3, "stun", 0, "Traps the foe in a bubble."),
        "Hydro Flow": Ability("Hydro Flow", 2, "heal", 10, "A restorative wave."),
        "Earthquake": Ability("Earthquake", 3, "damage", 14, "Shakes the battlefield."),
        "Stone Wall": Ability("Stone Wall", 2, "shield", 0, "Raises a rock shield."),
        "Quake Smash": Ability("Quake Smash", 4, "damage", 18, "A heavy earth slam."),
        "Wind Cutter": Ability("Wind Cutter", 2, "damage", 11, "A slicing gust."),
        "Gale Rush": Ability("Gale Rush", 2, "energy", 2, "Uses wind to regain energy."),
        "Cyclone Trap": Ability("Cyclone Trap", 3, "stun", 0, "A spiraling storm trap."),
        "Shadow Burst": Ability("Shadow Burst", 3, "damage", 14, "A blast of dark energy."),
        "Night Veil": Ability("Night Veil", 2, "shield", 0, "Shadows absorb the next attack."),
        "Dark Drain": Ability("Dark Drain", 3, "energy", 2, "Siphons power from the arena."),
        "Light Flash": Ability("Light Flash", 2, "stun", 0, "A bright flash that interrupts the foe."),
        "Heavenly Heal": Ability("Heavenly Heal", 2, "heal", 11, "A light-infused recovery."),
        "Radiant Force": Ability("Radiant Force", 3, "damage", 14, "A focused beam of power."),
    }


def build_roster():
    a = build_abilities()
    return [
        Bakugan("Dragonoid", "Pyrus", 8, 7, 6, [a["Blaze Cannon"], a["Phoenix Burst"], a["Inferno Spiral"]]),
        Bakugan("Delta Dragonoid", "Pyrus", 9, 8, 5, [a["Blaze Cannon"], a["Dragon Guard"], a["Meteor Strike"]]),
        Bakugan("Tigrerra", "Haos", 7, 8, 7, [a["Light Flash"], a["Heavenly Heal"], a["Radiant Force"]]),
        Bakugan("Skyress", "Ventus", 8, 7, 9, [a["Wind Cutter"], a["Gale Rush"], a["Cyclone Trap"]]),
        Bakugan("Preyas", "Aquos", 7, 6, 7, [a["Aqua Cannon"], a["Hydro Flow"], a["Bubble Prison"]]),
        Bakugan("Gorem", "Subterra", 8, 9, 4, [a["Earthquake"], a["Stone Wall"], a["Quake Smash"]]),
        Bakugan("Clawsaurus", "Subterra", 10, 8, 4, [a["Earthquake"], a["Stone Wall"], a["Quake Smash"]]),
        Bakugan("Hydranoid", "Darkus", 9, 7, 8, [a["Shadow Burst"], a["Night Veil"], a["Dark Drain"]]),
        Bakugan("Fear Ripper", "Darkus", 7, 6, 9, [a["Shadow Burst"], a["Night Veil"], a["Dark Drain"]]),
        Bakugan("Alpha Hydranoid", "Darkus", 10, 8, 8, [a["Shadow Burst"], a["Night Veil"], a["Dark Drain"]]),
        Bakugan("Serpenoid", "Aquos", 6, 6, 6, [a["Aqua Cannon"], a["Tidal Shield"], a["Bubble Prison"]]),
        Bakugan("Laserman", "Haos", 8, 7, 8, [a["Light Flash"], a["Heavenly Heal"], a["Radiant Force"]]),
        Bakugan("Mantris", "Ventus", 7, 7, 8, [a["Wind Cutter"], a["Gale Rush"], a["Cyclone Trap"]]),
        Bakugan("Cycloid", "Pyrus", 7, 7, 5, [a["Blaze Cannon"], a["Dragon Guard"], a["Meteor Strike"]]),
        Bakugan("Robanoid", "Haos", 7, 8, 6, [a["Light Flash"], a["Heavenly Heal"], a["Radiant Force"]]),
        Bakugan("Falconeer", "Ventus", 6, 6, 10, [a["Wind Cutter"], a["Gale Rush"], a["Cyclone Trap"]]),
    ]


def build_characters():
    return [
        Character("Dan Kuso", "Pyrus Brawler", "Pyrus Bakugan deal 15% more damage.", attack_bonus_attribute="Pyrus", attack_bonus_multiplier=1.15),
        Character("Shun Kazami", "Speed Tactician", "Ventus Bakugan gain +2 speed and act sooner.", attack_bonus_attribute="Ventus", speed_bonus=2, attack_bonus_multiplier=1.1),
        Character("Marucho Marukura", "Strategist", "Starts with extra energy and a larger item stash.", energy_bonus=1, potion_bonus=1),
        Character("Runo Misaki", "Recovery Specialist", "Healing effects restore more health.", heal_bonus=5, potion_bonus=1),
        Character("Julie Makimoto", "Lucky Challenger", "Crit chance is higher and attacks can spike harder.", crit_bonus=0.12),
        Character("Alice Gehabich", "Calm Defender", "Bakugan are sturdier in battle.", shield_bonus=1),
        Character("Masquerade", "Dark Strategist", "Darkus Bakugan gain a discount on abilities.", attack_bonus_attribute="Darkus", attack_bonus_multiplier=1.1, discount_attribute="Darkus"),
        Character("Spectra Phantom", "Elite Commander", "Aquos and Pyrus hits are more aggressive.", attack_bonus_attribute="Aquos", attack_bonus_multiplier=1.12),
    ]


def build_gate_cards():
    return [
        GateCard("Fusion Gate", "Pyrus and Aquos gain a slight power boost.", attack_bonus={"Pyrus": 1.12, "Aquos": 1.12}, energy_bonus=1),
        GateCard("Stone Circuit", "Subterra Bakugan defend better on this gate.", defense_bonus={"Subterra": 1.15}, energy_bonus=1),
        GateCard("Sky Platform", "Ventus strikes feel faster and cleaner.", attack_bonus={"Ventus": 1.15}),
        GateCard("Night Core", "Darkus Bakugan draw more power from the battlefield.", attack_bonus={"Darkus": 1.15}, energy_bonus=1),
        GateCard("Radiant Sphere", "Haos Bakugan shine brighter and resist pressure.", attack_bonus={"Haos": 1.15}, defense_bonus={"Haos": 1.1}),
        GateCard("Inferno Ring", "Pyrus attacks hit harder, but everyone burns energy faster.", attack_bonus={"Pyrus": 1.18}, energy_bonus=1),
    ]


def show_main_menu():
    clear_screen()
    render_title_art()
    print("""
                     A N I M A T E   B A T T L E   P R O J E C T
    """)
    print(line("-"))
    print("1. Start Battle")
    print("2. Story Mode")
    print("3. Instructions")
    print("4. Credits")
    print("5. Exit")
    print(line("-"))
    return ask_choice("", ["Start Battle", "Story Mode", "Instructions", "Credits", "Exit"])


def show_instructions():
    clear_screen()
    header("INSTRUCTIONS")
    print("This game is a turn-based Bakugan battle simulator inspired by the anime.")
    print()
    print("SETUP")
    print("- Enter player names.")
    print("- Choose one character per player for passive bonuses.")
    print("- Draft 3 Bakugan each from the shared roster.")
    print()
    print("BATTLE FLOW")
    print("- Each round opens on a Gate Card with its own effects.")
    print("- Faster Bakugan usually act first.")
    print("- On your turn you may attack, use an ability, use an item, switch Bakugan, or view your team.")
    print("- Basic attacks cost 1 energy.")
    print("- Abilities cost more energy, but can heal, stun, burn, shield, or deal heavier damage.")
    print()
    print("WINNING")
    print("- Knock out every Bakugan on the opposing team to win.")
    print("- If both sides fall at the same time, total remaining team power breaks the tie.")
    print()
    print("TIPS")
    print("- Use type advantage: Pyrus > Aquos > Subterra > Ventus > Darkus > Haos > Pyrus.")
    print("- Save energy for stronger abilities when the match gets close.")
    print("- Use shields before taking a hard hit.")
    print("- Revive is strongest when you are down to your last few Bakugan.")
    pause()


def battle_intro(trainer_one, trainer_two, battle):
    frames = [
        f"{trainer_one.name} steps into the arena...",
        f"{trainer_two.name} steps into the arena...",
        f"GATE CARD: {battle.gate_card.name}",
        f"{trainer_one.active().name} faces {trainer_two.active().name}",
        "The battle dimension locks in.",
    ]
    animate_sequence(frames, delay=0.45)


def battle_story_intro(player_trainer, enemy_trainer, battle, story_text):
    frames = [
        story_text,
        f"{player_trainer.name} prepares for battle...",
        f"{enemy_trainer.name} steps into the arena...",
        f"GATE CARD: {battle.gate_card.name}",
    ]
    animate_sequence(frames, delay=0.55)


def victory_splash(message):
    frames = [
        message,
        f"{message} ",
        f"{message}  ",
        f"{message}   ",
    ]
    animate_sequence(frames, delay=0.18)


def show_credits():
    clear_screen()
    header("CREDITS")
    print("Bakugan: Battle Dimension fan project")
    print("Built in Python for local two-player battles")
    print("Inspired by the anime Bakugan mechanics")
    pause()


def select_character(characters, prompt):
    clear_screen()
    header(prompt)
    for index, character in enumerate(characters, start=1):
        print(f"{index}. {character.name} - {character.title}")
        print(f"   {character.bonus_text}")
    choice = ask_int("Choose a character number: ", 1, len(characters))
    return characters[choice - 1]


def draft_team(player_name, roster_pool, team_size=3):
    team = []
    available = roster_pool[:]
    for slot in range(team_size):
        clear_screen()
        header(f"{player_name} - Draft Bakugan {slot + 1}/{team_size}")
        for index, bakugan in enumerate(available, start=1):
            print(f"{index}. {bakugan.name} | {bakugan.attribute} | Power {bakugan.power} | Stamina {bakugan.stamina} | Speed {bakugan.speed}")
            print(f"   Abilities: {', '.join(ability.name for ability in bakugan.abilities)}")
        choice = ask_int("Choose a Bakugan number: ", 1, len(available))
        selected = available.pop(choice - 1)
        team.append(selected.clone())
        print(f"{selected.name} added to {player_name}'s team.")
        pause()
    return team


def choose_active_if_needed(trainer):
    if trainer.active().is_alive():
        return
    trainer.auto_switch_if_needed()


def apply_round_start(trainer, battle):
    active = trainer.active()
    active.gain_energy(1 + battle.gate_card.energy_bonus)
    active.start_turn()
    choose_active_if_needed(trainer)


def choose_action(trainer):
    active = trainer.active()
    print(f"\nActive Bakugan: {active.card()}")
    print(f"Statuses: {active.status_line()}")
    print("1. Basic Attack")
    print("2. Use Ability")
    print("3. Use Item")
    print("4. Switch Bakugan")
    print("5. View Team")
    return ask_int("Choose an action: ", 1, 5)


def use_item(trainer):
    available = [name for name, count in trainer.items.items() if count > 0]
    if not available:
        print("No items left.")
        return

    section(f"{trainer.name}'s Items")
    for index, item_name in enumerate(available, start=1):
        print(f"{index}. {item_name} x{trainer.items[item_name]}")
    choice = ask_int("Select an item: ", 1, len(available))
    item = available[choice - 1]
    active = trainer.active()

    if item == "Potion":
        play_sound("CHIME", "Potion")
        amount = 18 + trainer.character.heal_bonus
        active.heal(amount)
        trainer.items[item] -= 1
        print(f"{active.name} recovered {amount} HP.")
    elif item == "Shield":
        play_sound("WHUM", "Shield")
        active.shield_turns += 1
        trainer.items[item] -= 1
        print(f"{active.name} is protected by a shield.")
    elif item == "Energy Drink":
        play_sound("VMMM", "Energy Drink")
        active.gain_energy(3)
        trainer.items[item] -= 1
        print(f"{active.name} gained 3 energy.")
    elif item == "Revive":
        play_sound("SHIIINE", "Revive")
        knocked_out = [index for index, bakugan in enumerate(trainer.team) if not bakugan.is_alive()]
        if not knocked_out:
            print("No knocked out Bakugan to revive.")
            return
        section("Choose a Bakugan to Revive")
        for position, index in enumerate(knocked_out, start=1):
            bakugan = trainer.team[index]
            print(f"{position}. {bakugan.name}")
        revive_choice = ask_int("Choose a Bakugan: ", 1, len(knocked_out))
        target = trainer.team[knocked_out[revive_choice - 1]]
        target.health = max(1, target.max_health // 2)
        target.energy = 2
        target.shield_turns = 0
        target.stun_turns = 0
        target.burn_turns = 0
        trainer.items[item] -= 1
        print(f"{target.name} has returned to the battle at half power.")


def ai_choose_action(attacker, defender):
    active = attacker.active()
    enemy = defender.active()
    if active.health <= active.max_health // 3 and attacker.items.get("Potion", 0) > 0:
        return 3
    if active.energy >= 3 and any(ability.kind in {"damage", "burn", "stun"} for ability in active.abilities):
        return 2
    if active.health <= active.max_health // 4 and len(attacker.available_indices()) > 1:
        return 4
    if attacker.items.get("Shield", 0) > 0 and active.health <= active.max_health // 2:
        return 3
    if active.energy == 0:
        return 1
    if enemy.health <= active.power * 2:
        return 2 if active.energy >= 2 else 1
    return 1


def ai_choose_ability_index(attacker, defender):
    active = attacker.active()
    affordable = []
    for index, ability in enumerate(active.abilities):
        cost = max(1, ability.cost - (1 if attacker.character.discount_attribute == active.attribute else 0))
        if active.energy >= cost:
            score = ability.power
            if ability.kind == "damage":
                score += 8
            elif ability.kind == "burn":
                score += 6
            elif ability.kind == "stun":
                score += 7
            elif ability.kind == "heal" and active.health <= active.max_health // 2:
                score += 5
            elif ability.kind == "shield" and active.health <= active.max_health // 2:
                score += 4
            affordable.append((score, index))
    if not affordable:
        return 0
    affordable.sort(reverse=True)
    return affordable[0][1]


def ai_choose_item(trainer):
    active = trainer.active()
    if trainer.items.get("Potion", 0) > 0 and active.health <= active.max_health // 2:
        return "Potion"
    if trainer.items.get("Shield", 0) > 0 and active.health <= active.max_health // 3:
        return "Shield"
    if trainer.items.get("Energy Drink", 0) > 0 and active.energy <= 1:
        return "Energy Drink"
    if trainer.items.get("Revive", 0) > 0 and any(not bakugan.is_alive() for bakugan in trainer.team):
        return "Revive"
    return "Potion" if trainer.items.get("Potion", 0) > 0 else "Shield"


def ai_choose_switch(trainer):
    options = trainer.available_indices()
    if len(options) <= 1:
        return
    best_index = max(options, key=lambda index: trainer.team[index].health + trainer.team[index].energy * 2)
    trainer.active_index = best_index
    print(f"{trainer.name} switches to {trainer.active().name}.")


def battle_turn(attacker, defender, battle, is_ai=False):
    active = attacker.active()
    if active.stun_turns > 0:
        active.stun_turns -= 1
        print(f"{active.name} is stunned and misses the turn.")
        return

    action = ai_choose_action(attacker, defender) if is_ai else choose_action(attacker)
    if action == 1:
        active.use_basic_attack(defender.active(), attacker, battle)
    elif action == 2:
        if is_ai:
            ability_choice = ai_choose_ability_index(attacker, defender)
        else:
            section(f"{active.name} - Abilities")
            for index, ability in enumerate(active.abilities, start=1):
                print(f"{index}. {ability.name} | Cost {ability.cost} | {ability.description}")
            ability_choice = ask_int("Choose an ability: ", 1, len(active.abilities)) - 1
        active.use_ability(ability_choice, defender.active(), attacker, battle)
    elif action == 3:
        if is_ai:
            selected_item = ai_choose_item(attacker)
            if selected_item == "Revive":
                print(f"{attacker.name} uses Revive.")
            use_item(attacker)
        else:
            use_item(attacker)
    elif action == 4:
        if is_ai:
            ai_choose_switch(attacker)
        else:
            attacker.choose_active()
    elif action == 5:
        if is_ai:
            active.use_basic_attack(defender.active(), attacker, battle)
        else:
            clear_screen()
            header(f"{attacker.name}'s Team Overview")
            attacker.summary()
            pause()

    if defender.active().health <= 0:
        defender.auto_switch_if_needed()


def render_battle_status(trainers, battle):
    clear_screen()
    header(f"ROUND {battle.round_number} - {battle.gate_card.name}")
    print(battle.gate_card.description)
    print(line("-"))
    for trainer in trainers:
        active = trainer.active()
        print(f"{trainer.name} as {trainer.character.name} ({trainer.character.title})")
        print(f"Active: {active.card()}")
        print(f"Status: {active.status_line()}")
        print(f"Items: {trainer.items}")
        print(line("-"))


def determine_turn_order(first, second, battle):
    first_score = first.active().speed + first.character.speed_bonus + random.randint(1, 6)
    second_score = second.active().speed + second.character.speed_bonus + random.randint(1, 6)
    if battle.gate_card.name == "Sky Platform" and first.active().attribute == "Ventus":
        first_score += 2
    if battle.gate_card.name == "Sky Platform" and second.active().attribute == "Ventus":
        second_score += 2
    return (first, second) if first_score >= second_score else (second, first)


def battle_match(trainer_one, trainer_two, opening_text=None):
    gate_deck = build_gate_cards()
    random.shuffle(gate_deck)
    battle = BattleState(gate_card=gate_deck[0])
    trainers = [trainer_one, trainer_two]
    round_index = 0

    if opening_text:
        battle_story_intro(trainer_one, trainer_two, battle, opening_text)
    else:
        battle_intro(trainer_one, trainer_two, battle)

    while trainer_one.has_available() and trainer_two.has_available():
        battle.gate_card = gate_deck[round_index % len(gate_deck)]
        battle.round_number = round_index + 1
        play_sound("ROUND START", f"{battle.gate_card.name}")

        for trainer in trainers:
            trainer.active().gain_energy(battle.gate_card.energy_bonus)

        render_battle_status(trainers, battle)
        print(f"Gate effect: {battle.gate_card.description}")
        animate_bakugan_entry(trainer_one.active(), "left")
        animate_bakugan_entry(trainer_two.active(), "right")
        pause("Press Enter to start the round...")

        first, second = determine_turn_order(trainer_one, trainer_two, battle)
        print(f"{first.name} will act first this round.")
        pause()

        for current, opponent in ((first, second), (second, first)):
            if not current.has_available() or not opponent.has_available():
                break
            choose_active_if_needed(current)
            choose_active_if_needed(opponent)
            if not current.has_available() or not opponent.has_available():
                break
            current.active().start_turn()
            if current.active().health <= 0:
                current.auto_switch_if_needed()
                continue
            battle_turn(current, opponent, battle, is_ai=current.is_ai)
            if not opponent.has_available():
                break

        if not trainer_one.has_available() or not trainer_two.has_available():
            break

        round_index += 1

    clear_screen()
    header("FINAL JUDGMENT")
    if trainer_one.has_available() and not trainer_two.has_available():
        victory_splash(f"Victory goes to {trainer_one.name}!")
    elif trainer_two.has_available() and not trainer_one.has_available():
        victory_splash(f"Victory goes to {trainer_two.name}!")
    else:
        one_hp = sum(bakugan.health for bakugan in trainer_one.team)
        two_hp = sum(bakugan.health for bakugan in trainer_two.team)
        if one_hp > two_hp:
            victory_splash(f"Victory goes to {trainer_one.name} by total remaining power!")
        elif two_hp > one_hp:
            victory_splash(f"Victory goes to {trainer_two.name} by total remaining power!")
        else:
            victory_splash("The battle ends in a draw.")

    print("\nBattle summary:")
    trainer_one.summary()
    print()
    trainer_two.summary()
    pause()


def build_story_opponents():
    roster = build_roster()
    characters = build_characters()
    return [
        {
            "name": "Alpha Team Commander",
            "character": characters[5],
            "team": [roster[5].clone(), roster[10].clone(), roster[14].clone()],
            "text": "A silent challenger emerges from the stone arena.",
        },
        {
            "name": "Shadow Rival",
            "character": characters[6],
            "team": [roster[7].clone(), roster[8].clone(), roster[9].clone()],
            "text": "Darkus power gathers at the edge of the battlefield.",
        },
        {
            "name": "Grand Arena Champion",
            "character": characters[7],
            "team": [roster[1].clone(), roster[3].clone(), roster[11].clone()],
            "text": "The final champion steps forward under the arena lights.",
        },
    ]


def story_mode():
    clear_screen()
    header("STORY MODE")
    print("A campaign path with named rivals, dialogue, and escalating battle difficulty.")
    print("Win every match to claim the arena title.")
    pause()

    player_name = input("Enter your trainer name: ").strip() or "Bakugan Brawler"
    characters = build_characters()
    player_character = select_character(characters, f"{player_name} - Choose Your Character")
    roster = build_roster()
    team = draft_team(player_name, roster, 3)
    player_trainer = Trainer(player_name, player_character, team)

    opponents = build_story_opponents()
    for stage_number, opponent_data in enumerate(opponents, start=1):
        clear_screen()
        header(f"CAMPAIGN STAGE {stage_number}")
        print(opponent_data["text"])
        print(f"Opponent: {opponent_data['name']} ({opponent_data['character'].name})")
        pause()

        enemy_trainer = Trainer(opponent_data["name"], opponent_data["character"], [bakugan.clone() for bakugan in opponent_data["team"]], is_ai=True)
        battle_match(player_trainer, enemy_trainer, opening_text=opponent_data["text"])

        if not player_trainer.has_available():
            clear_screen()
            header("CAMPAIGN FAILED")
            print("Your Bakugan team has fallen. The campaign ends here.")
            pause()
            return

        if stage_number < len(opponents):
            for bakugan in player_trainer.team:
                if bakugan.is_alive():
                    bakugan.heal(12)
                    bakugan.gain_energy(1)
            clear_screen()
            header("STAGE CLEARED")
            print("Your surviving Bakugan recover a little before the next battle.")
            pause()

    clear_screen()
    header("CAMPAIGN CLEARED")
    print("You defeated every rival and claimed the arena.")
    pause()


def setup_match():
    clear_screen()
    header("NEW BATTLE")
    player_one_name = input("Player One name: ").strip() or "Player One"
    player_two_name = input("Player Two name: ").strip() or "Player Two"

    characters = build_characters()
    player_one_character = select_character(characters, f"{player_one_name} - Choose Your Character")
    player_two_character = select_character(characters, f"{player_two_name} - Choose Your Character")

    roster = build_roster()
    team_one = draft_team(player_one_name, roster, 3)
    remaining = [bakugan.clone() for bakugan in roster if bakugan.name not in {selected.name for selected in team_one}]
    team_two = draft_team(player_two_name, remaining, 3)

    trainer_one = Trainer(player_one_name, player_one_character, team_one)
    trainer_two = Trainer(player_two_name, player_two_character, team_two)
    battle_match(trainer_one, trainer_two)


def main():
    while True:
        choice = show_main_menu()
        if choice == "Start Battle":
            setup_match()
        elif choice == "Story Mode":
            story_mode()
        elif choice == "Instructions":
            show_instructions()
        elif choice == "Credits":
            show_credits()
        elif choice == "Exit":
            clear_screen()
            print("Thanks for playing Bakugan: Battle Dimension.")
            break


if __name__ == "__main__":
    main()