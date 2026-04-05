# Homework 3 - Board Game System
# Name:Liam Gillispie
# Date:4/5/2026
# Assignment: Homework 3
# Purpose: Create and impliment a simple board game system.

def loadGameData(filename):
    """Reads game data from a file and returns it as a list."""
    data = []
    with open(filename, "r") as file:
        for line in file:
            data.append(line.strip())
    return data


def displayGame(data):
    """Displays the current game state."""
    print("\nCurrent Game State:")
    for item in data:
        print(item)


def movePlayer(data):
    """Example function to simulate moving a player."""
    print("\nMove player function not fully implemented.")
    # Students will modify this


def main():
    filename = "events.txt"   # Students can rename if needed

    gameData = loadGameData(filename)
    displayGame(gameData)

    # Example interaction
    choice = input("\nMove player? (y/n): ")
    if choice.lower() == "y":
        movePlayer(gameData)


if __name__ == "__main__":
    main()
