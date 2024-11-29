import random
import sys
import concurrent.futures

class Door:
    def __init__(self, id):
        self.id = id
        self.prize = False
        self.chosen = False
        self.revealed = False

    def __repr__(self):
        return(f"Door(id={self.id}, prize={self.prize}, chosen={self.chosen}, revealed={self.revealed})")


class Game:
    def __init__(self, number_of_doors:int, initial_pick:int, switch:bool, debug=False):
        if debug:
            print(f"number_of_doors:{number_of_doors}, initial_pick:{initial_pick}, switch:{switch}")

        # the number of doors must be positive
        assert number_of_doors > 0

        # the initial pick must be within the range of available dors
        assert initial_pick in range(0,number_of_doors)

        # initialize a list of Door() instances based on number_of_doors requested
        doors = [Door(id=i) for i in range(0,number_of_doors)]

        if debug:
            print("Post initialization of door list:")
            for door in doors:
                print(door)
            print()

        # we need one of them to have a prize.   pick a number between 0 and number_of_doors and put the prize in the associated door.
        doors[random.randrange(0, number_of_doors)].prize = True

        if debug:
            print("Post prize assignment:")
            for door in doors:
                print(door)
            print()

        # pick a door using the initial_pick variable
        chosen_door = doors[initial_pick]
        chosen_door.chosen = True

        if debug:
            print("Post initial pick:")
            for door in doors:
                print(door)
            print()

        # we need to reveal one of the non-picked doors that has no prize, randomly
        # put the non-chosen doors into their own list
        other_doors = []
        # iterate over all the doors and put the non-chosen doors into the aforementioned list
        for door in doors:
            if not door.chosen:
                other_doors.append(door)

        if debug:
            print("Post other door separation:")
            print("All doors:")
            for door in doors:
                print(door)
            print()
            print("Non-chosen doors:")
            for door in other_doors:
                print(door)
            print()


        # randomly pick one of the non-chosen doors, and if it has no prize, reveal it
        while True:
            door = other_doors[random.randrange(0, len(other_doors))]
            if not door.prize:
                door.revealed = True
                break

        if debug:
            print("Post reveal")
            for door in doors:
                print(door)
            print()

        # decide to keep initial choice or switch
        if switch:
            chosen_door.chosen = False
            for door in other_doors:
                if not door.revealed:
                    chosen_door = door
                    chosen_door.chosen = True
                    break

        if debug:
            print("Post switch choice")
            for door in doors:
                print(door)
            print()

        if chosen_door.prize:
            self.winner = True
        else:
            self.winner = False

def rungame(number_of_doors, switch, debug):
        initial_pick = random.randrange(0, number_of_doors)
        game = Game(number_of_doors, initial_pick, switch, debug)
        if game.winner:
            return 1
        else:
            return 0

if __name__ == "__main__":
    try:
        games_to_run = int(sys.argv[1])
        number_of_doors = int(sys.argv[2])
        switch = bool(int(sys.argv[3]))
        debug = bool(int(sys.argv[4]))
    except IndexError:
        sys.exit(1)
    if debug:
        print(sys.argv)
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(rungame, number_of_doors, switch, debug) for i in range(0, games_to_run)]
    for future in futures:
        results.append(future.result())
    print(sum(results)/games_to_run)

