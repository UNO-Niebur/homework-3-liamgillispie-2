# Homework 3 - Board Game System
# Name:Liam Gillispie
# Date:4/5/2026
# Assignment: Homework 3
# Purpose: Create and impliment a simple board game system

import random
DEFAULT_BOARD_SIZE = 200
DICE_MIN = 1
DEFAULT_DICE_MAX = 20
EVENTS_FILE = "events.txt"

def loadEvents(filename):
    events = {}
    try:
        with open(filename, "r") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(":", 2)
                if len(parts) < 2:
                    continue
                # parse position
                try:
                    pos = int(parts[0])
                except ValueError:
                    continue
                if len(parts) == 2:
                    # pos:message
                    events[pos] = ("message", parts[1].strip())
                else:
                    typ = parts[1].strip().lower()
                    val_raw = parts[2].strip()
                    if typ == "message":
                        events[pos] = ("message", val_raw)
                    elif typ == "jump":
                        try:
                            events[pos] = ("jump", int(val_raw))
                        except ValueError:
                            events[pos] = ("message", val_raw)
                    elif typ == "offset":
                        try:
                            events[pos] = ("offset", int(val_raw))
                        except ValueError:
                            events[pos] = ("message", val_raw)
                    else:
                        events[pos] = ("message", val_raw)
    except FileNotFoundError:
        pass
    return events

def movePlayer(player, roll, events, board_size):
    """
    Move player forward by roll, apply events:
      - jump: absolute position (int)
      - offset: relative move (int)
      - message: print message
    Returns (won: bool, event_msg: str or None)
    """
    pos = player["pos"]
    name = player["name"]
    event_msg = None

    final = pos + roll
    if final > board_size:
        final = board_size

    print(f"{name} rolled {roll} and moved to {final}")

    if final in events:
        typ, val = events[final]
        if typ == "jump":
            new_final = max(1, min(board_size, int(val)))
            event_msg = f"jump to {new_final}"
            print(f"Event at {final}: jump -> {new_final}")
            final = new_final
        elif typ == "offset":
            new_final = final + int(val)
            new_final = max(1, min(board_size, new_final))
            event_msg = f"offset {val} -> {new_final}"
            print(f"Event at {final}: offset {val} -> {new_final}")
            final = new_final
        else:  # message
            event_msg = str(val)
            print(f"Event at {final}: message -> {event_msg}")

    player["pos"] = final

    if final == board_size:
        print(f"{name} reached goal ({final}) and wins!")
        return True, event_msg
    return False, event_msg

def main():
    print("-----Journey to Cloudlandia!-----")

    board_size = DEFAULT_BOARD_SIZE
    dice_max = DEFAULT_DICE_MAX

    b_in = input(f"Board size (Default: {board_size}): ").strip()
    if b_in:
        try:
            board_size = int(b_in)
            if board_size < 1:
                board_size = DEFAULT_BOARD_SIZE
        except Exception:
            board_size = DEFAULT_BOARD_SIZE

    d_in = input(f"Die max size (Default/max die size: {dice_max}): ").strip()
    if d_in:
        try:
            dice_max = int(d_in)
            if dice_max < DICE_MIN:
                dice_max = DEFAULT_DICE_MAX
        except Exception:
            dice_max = DEFAULT_DICE_MAX

    names = input("Enter player names separated by commas (default Player1,Player2): ").strip()
    if not names:
        names = "Player1,Player2"
    players = [{"name": n.strip(), "pos": 1} for n in names.split(",") if n.strip()]

    print(f"Players: {', '.join([p['name'] for p in players])}")

    events = loadEvents(EVENTS_FILE)

    print("Welcome to the start of your journey to Cloudlandia!")
    print("This adventure is booby trapped and you can be sprung forward or pulled down.")
    print("Good luck, you'll need it....")

    turn = 0
    while True:
        for player in players:
            input(f"\n{player['name']}'s turn. Press Enter to roll...")
            roll = random.randint(DICE_MIN, dice_max)
            win, _ = movePlayer(player, roll, events, board_size)
            if win:
                print(f"Welcome to Cloudlandia! Winner: {player['name']}")
                return
        turn += 1

if __name__ == "__main__":
    main()
