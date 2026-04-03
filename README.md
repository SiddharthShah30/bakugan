# Bakugan: Battle Dimension

A Python Bakugan battle game with a full menu, character passives, team drafting, gate cards, energy-based abilities, items, and turn-based battle strategy.

## Features
- Main menu with Start, How to Play, Credits, and Exit
- 8 anime-inspired character choices with unique passives
- 16 Bakugan in the roster with attributes, stats, and signature abilities
- Team drafting system for both players
- Gate Card system that changes battle conditions each round
- Energy system for basic attacks and special abilities
- Items including Potion, Shield, Energy Drink, and Revive
- Automatic switching when a Bakugan is knocked out
- Win by knocking out all opposing Bakugan or by remaining team power in a tie

## How to Run
1. Make sure you have Python 3.7 or newer installed.
2. Open a terminal in this folder.
3. Run the game:
   ```bash
   python main.py
   ```

## How to Play
1. Start a new battle from the main menu.
2. Enter both player names.
3. Choose a character for each player.
4. Draft 3 Bakugan for each team from the shared roster.
5. On your turn, choose one of these actions:
   - Basic Attack
   - Use Ability
   - Use Item
   - Switch Bakugan
   - View Team
6. Gate Cards apply round-by-round bonuses and affect strategy.
7. Continue until one team has no Bakugan left.

## Bakugan and Attributes
The roster includes Pyrus, Aquos, Subterra, Ventus, Darkus, and Haos Bakugan.

Type advantage follows a simple battle chain:
- Pyrus beats Aquos
- Aquos beats Subterra
- Subterra beats Ventus
- Ventus beats Darkus
- Darkus beats Haos
- Haos beats Pyrus

## Requirements
- Python 3.7+
- No third-party packages required

## Project Files
- [main.py](main.py) - The game itself
- [README.md](README.md) - Project overview and instructions

## Credits
- Fan project inspired by the Bakugan anime series
- Built for local two-player battles in Python

## License
This project is for educational and fan use only.
