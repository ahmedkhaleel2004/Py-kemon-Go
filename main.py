import subprocess
try: 
    import keyboard
except ImportError:
    input("You are missing a required module. Would you like to automatically install it right now?\nY / N:\t")
    subprocess.run(["pip", "install", "keyboard"])
import keyboard
import random
import time
import sys

from classes import Pokemon, Candy

file = open('first_gen_pokemon.txt', 'r')

pokemon_names = [] # [[charmander, charmeleon, charizard], [pikachu, raichu]]
pokemon_types = [] # [['fire', 'fire', 'fire/flying'], ['electric', 'electric']]

for line in file:
    names = []
    types = []
    data = line.split()

    if len(data) == 8:
        for i in range(0,8,2):
            names.append(data[i])
        for i in range(1,8,2):
            types.append(data[i].strip('()'))
        pokemon_names.append(names)
        pokemon_types.append(types)
    elif len(data) == 6:
        for i in range(0,6,2):
            names.append(data[i])
        for i in range(1,6,2):
            types.append(data[i].strip('()'))
        pokemon_names.append(names)
        pokemon_types.append(types)
    elif len(data) == 4:
        for i in range(0,4,2):
            names.append(data[i])
        for i in range(1,4,2):
            types.append(data[i].strip('()'))
        pokemon_names.append(names)
        pokemon_types.append(types)
    elif len(data) == 2:
        for i in range(0,2,2):
            names.append(data[i])
        for i in range(1,2,2):
            types.append(data[i].strip('()'))
        pokemon_names.append(names)
        pokemon_types.append(types)

# inventory = [pokemonlist, candydict, stardust]
inventory = [[], {}, 0]

def inventory_interact():
    print("\nAccessing inventory...")
    while True:
        while True:
            choice = input("\n1:\tDisplay all caught pokemon\n2:\tShow pokemon stats\n3:\tShow available resources\n4:\tPower up a pokemon\n5:\tEvolve a pokemon\n6:\tQuit\n\nWhat would you like to do?:\t")
            if choice not in ['1','2','3','4','5','6']:
                print("\nPlease enter a valid choice.")
            else:
                break

        if choice == '1':
            for i in range(len(inventory[0])):
                print(f"\n{i+1}:\t {inventory[0][i].get_name()}")
        elif choice == '2':
            while True:
                try:
                    if len(inventory[0]) == 0:
                        print("\nYou do not have any pokemon")
                        break
                    else:
                        pokemon_choice = int(input("Which pokemon?:\t"))
                        inventory[0][pokemon_choice-1].display_attributes(inventory, pokemon_names)
                        break
                except IndexError:
                    print("Please input a valid choice (You can use menu option 1. to view pokemon)")
                except ValueError:
                    print("Please only input integers.")
        elif choice == '3':
            print("\nAvailable candies:")
            for key in inventory[1]:
                print(f"\t- {key} candy: {inventory[1][key].count}")
            print(f"\nAvailable stardust:\t{inventory[2]}")
        elif choice == '4':
            while True:
                try:
                    if len(inventory[0]) == 0:
                        print("\nYou do not have any pokemon")
                        break
                    else:
                        pokemon_choice = int(input("Which pokemon?:\t"))
                        possible_increment = inventory[0][pokemon_choice-1].get_stats()
                        for i in range(3):
                            if possible_increment[i] < 15:
                                possible_increment[i] += random.randint(1, 2)
                                if possible_increment[i] > 15:
                                    possible_increment[i] = 15
                        inventory[0][pokemon_choice-1].power_up(inventory, random.randint(50, 150), random.randint(0, 100), possible_increment)
                        break
                except IndexError:
                    print("Please input a valid choice (You can use menu option 1. to view pokemon)")
                except ValueError:
                    print("Please only input integers.")
        elif choice == '5':
            while True:
                try:
                    if len(inventory[0]) == 0:
                        print("\nYou do not have any pokemon")
                        break
                    else:
                        pokemon_choice = int(input("Which pokemon?:\t"))
                        stats_increment = inventory[0][pokemon_choice-1].get_stats()
                        for i in range(3):
                            if stats_increment[i] < 15:
                                stats_increment[i] += random.randint(3, 7)
                                if stats_increment[i] > 15:
                                    stats_increment[i] = 15
                        inventory[0][pokemon_choice-1].evolve(inventory, pokemon_names, pokemon_types, random.randint(200, 600), stats_increment)
                        break
                except IndexError:
                    print("Please input a valid choice (You can use menu option 1. to view pokemon)")
                except ValueError:
                    print("Please only input integers.")
        elif choice == '6':
            break

        while True:
            choice = input("\nExit inventory? (Y / N):\t")
            if choice.lower() == 'y':
                break
            elif choice.lower() == 'n':
                break
            else:
                print("\nPlease enter a valid input.")
        if choice.lower() == 'y':
            break

width = 30
height = 15

x_x = width // 2
x_y = height // 2

border = ['+', '+']
for i in range(width-1):
    border.insert(-1, '-')

map_list = []
bottom_gone = []
top_gone = []
right_gone = []
left_gone = []

for i in range(height):
    row_list = ['|']

    if i == x_y:
        for i in range(x_x-1):
            row_list.append('/')
        row_list.append('X')
        for i in range(x_x-1):
            row_list.append('/')
        row_list.append('|')
        map_list.append(row_list)
    else:
        if random.randint(0, 100) < 10:
            for i in range(width-random.randint(2, 30)):
                row_list.append('/')
            row_list.append("\033[1;31m?\033[0m")
            for i in range(width-len(row_list)):
                row_list.append('/')
            row_list.append('|')
            map_list.append(row_list)
        elif random.randint(0, 100) < 3:
            for i in range(width-random.randint(2, 30)):
                row_list.append('/')
            row_list.append("\033[1;32m!\033[0m")
            for i in range(width-len(row_list)):
                row_list.append('/')
            row_list.append('|')
            map_list.append(row_list)
        else:
            for i in range(width-1):
                row_list.append('/')
            row_list.append('|')
            map_list.append(row_list)
        
def print_instructions():
    print("\nWelcome to Py-kemon Go!")
    print("\nBuilt by Ahmed Khaleel and Ali Hussin")
    print("\nThis game only works when ran in a proper IDE like VSCode. Running this in the terminal or IDLE will cause lots of formatting issues.")
    print("\nControls:\n\t- WASD for moving around the map\n\t- 'F' to attempt a capture once you are next to a '?'\n\t- 'I' to access your inventory\n\t- 'G' to interact with an enemy pokemon '!'\n\t- 'Q' to quit")
    input("\nEnter any key to start.\t")

def print_map():
    print("\033c")
    print(''.join(border))
    for i in range(len(map_list)):
        print(''.join(map_list[i]))
    print(''.join(border))

def generate_row():
    row_list = ['|']
    if random.randint(0, 100) < 10:
        for i in range(width-random.randint(2, 30)):
            row_list.append('/')
        row_list.append("\033[1;31m?\033[0m")
        for i in range(width-len(row_list)):
            row_list.append('/')
        row_list.append('|')
    elif random.randint(0, 100) < 3:
        for i in range(width-random.randint(2, 30)):
            row_list.append('/')
        row_list.append("\033[1;32m!\033[0m")
        for i in range(width-len(row_list)):
            row_list.append('/')
        row_list.append('|')
    else:
        for i in range(width-1):
            row_list.append('/')
        row_list.append('|')
    return row_list

def generate_column():
    column_list = []
    if random.randint(0, 100) < 10:
        for i in range(height-random.randint(0, 15)):
            column_list.append('/')
        column_list.append("\033[1;31m?\033[0m")
        for i in range(height-len(column_list)):
            column_list.append('/')
    elif random.randint(0, 100) < 3:
        for i in range(height-random.randint(0, 15)):
            column_list.append('/')
        column_list.append("\033[1;32m!\033[0m")
        for i in range(height-len(column_list)):
            column_list.append('/')
    else:
        for i in range(height):
            column_list.append('/')
    return column_list

def move_map(direction):
    if direction == 'up':

        # All the lines need to move down one, top one is generated, and X moves up one.

        map_list[x_y][x_x] = '/'
        map_list[x_y-1][x_x] = 'X'

        bottom_gone.append(map_list.pop(-1))

        if len(top_gone) > 0:
            map_list.insert(0, top_gone.pop(-1))
        else:
            map_list.insert(0, generate_row())

    if direction == 'down':
        map_list[x_y][x_x] = '/'
        map_list[x_y+1][x_x] = 'X'

        top_gone.append(map_list.pop(0))

        if len(bottom_gone) > 0:
            map_list.append(bottom_gone.pop(-1))
        else:
            map_list.append(generate_row())

    if direction == 'left':
        map_list[x_y][x_x] = '/'
        map_list[x_y][x_x-1] = 'X'

        right_column_downwards = []

        for i in range(height):
            right_column_downwards.append(map_list[i].pop(-2))
        right_gone.append(right_column_downwards)

        if len(left_gone) > 0:
            for i in range(height):
                map_list[i].insert(1, left_gone[-1][i])
            left_gone.pop(-1)
        else:
            new = generate_column()

            for i in range(height):
                map_list[i].insert(1, new[i])

    if direction == 'right':
        map_list[x_y][x_x] = '/'
        map_list[x_y][x_x+1] = 'X'

        left_column_downwards = []

        for i in range(height):
            left_column_downwards.append(map_list[i].pop(1))
        left_gone.append(left_column_downwards)

        if len(right_gone) > 0:
            for i in range(height):
                map_list[i].insert(-2, right_gone[-1][i])
            right_gone.pop(-1)
        else:
            new = generate_column()

            for i in range(height):
                map_list[i].insert(-2, new[i])

def random_pokemon():
    evolution_chance = random.randint(0, 100)
    chosen_family = pokemon_names[random.randint(0, len(pokemon_names)-1)]
    if evolution_chance < 20 and len(chosen_family) >= 3:
        pick = 2
    elif evolution_chance < 50 and len(chosen_family) >= 2:
        pick = 1
    else:
        pick = 0
    return chosen_family[pick]

def clear_buffer():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def ran_away():
    for i in range(-1, 2):
        map_list[x_y+i][x_x] = '/'
        map_list[x_y][x_x+i] = '/'

def find_and_create_pokemon(pokemon_name: str):
    x = 0
    for i in pokemon_names:
        y = 0
        for j in i:
            if pokemon_name == j:
                break
            y += 1
        if pokemon_name == j:
            break
        x += 1
    typ = pokemon_types[x][y]

    if current_multiplier() == 0:
        cp = random.randint(200,400)*(y+1)
    else:
        cp = int(random.randint(200,400)*(y+1)*current_multiplier()) # EXTREMELY oversimplified initial CP guess

    family = pokemon_names[x][0]

    randomstats = []
    for i in range(3):
        j = random.randint(1,4)
        randomstats.append(j)
    for i in randomstats:
        i = i*(y+1)

    if random.randint(0, 100) < 20:
        isShiny = True
        print("This pokemon is \033[1;33mSHINY!\033[0m")
    else:
        isShiny = False

    return Pokemon(pokemon_name, typ, cp, family, randomstats, isShiny, pokemon_names)

def current_multiplier():
    if len(inventory[0]) % 2 == 0:
        return len(inventory[0])/2
    else:
        return (len(inventory[0])/2)+0.5

def catch_pokemon(pokemon_name: str):
    pokemon = find_and_create_pokemon(pokemon_name)
    pokemon.catch(inventory, random.randint(3, 20))
    inventory[1][pokemon.family].count = int(inventory[1][pokemon.family].count*current_multiplier())
    inventory[2] += int(random.randint(300, 1000)*current_multiplier())

def check_around_x(escape_code: str):
    return any(map_list[x_y+i][x_x] == escape_code for i in range(-1,2)) or any(map_list[x_y][x_x+i] == escape_code for i in range(-1,2))

def attempt_capture():
    clear_buffer()
    found_pokemon = random_pokemon()
    if check_around_x('\033[1;31m?\033[0m'):
        print(f"You found a {found_pokemon}!")
        print("\nDo you want to attempt to capture it? It will run away if you don't.")
        while True:
            choice = input("Y / N:\t")
            if choice.lower() == 'y':
                attempts = 5
                while attempts > 1:
                    if random.randint(0, 100) < 20:
                        print(f"You have caught the {found_pokemon}! It has been added to your collection.")
                        ran_away()
                        catch_pokemon(found_pokemon)
                        break
                    else:
                        attempts -= 1
                        print(f"You were not able to catch it.\nAttempts left: {attempts}")
                        while True:
                            choice = input("Try again? (Y / N):\t")
                            if choice.lower() == 'n':
                                ran_away()
                                print(f"The {found_pokemon} ran away.")
                                break
                            elif choice.lower() == 'y':
                                break
                            else:
                                print("Please enter a valid input.")
                        if choice.lower() == 'n':
                            break
                if attempts == 1:
                    ran_away()
                    print(f"You have ran out of attempts, the {found_pokemon} ran away.")
                break
            elif choice.lower() == 'n':
                ran_away()
                print(f"The {found_pokemon} ran away.")
                break
            else:
                print("Please enter a valid input.")
    else:
        print("You are not next to a pokemon")

def fight():
    if check_around_x('\033[1;32m!\033[0m'):
        pokemon = find_and_create_pokemon(random_pokemon())
        for i in range(3):
            if pokemon.stats[i] < 15:
                pokemon.stats[i] += int(1*current_multiplier())
                if pokemon.stats[i] > 15:
                    pokemon.stats[i] = 15
        pokemon.iv = round((sum(pokemon.get_stats())/45)*100, 1)
        print(f"You found a hostile {pokemon.get_name()}!")
        print("\nIt's stats:")
        pokemon.display_attributes(inventory, pokemon_names, True)
        
        if len(inventory[0]) == 0:
            print("\nYou do not have a pokemon available to fight yet.")
            ran_away()
            print(f"\nThe {pokemon.get_name()} ran away.")
            return

        while True:
            choice = input(f"\nDo you want to fight this {pokemon.get_name()}? It will run away if you don't. (Y / N):\t")
            if choice.lower() == 'y':
                print("\nYour available pokemon:")
                for i in range(len(inventory[0])):
                    print(f"\n{i+1}: {inventory[0][i].get_name()} CP: {inventory[0][i].get_cp()} IV: {inventory[0][i].get_iv()}% Shiny?: {inventory[0][i].get_shiny_text()}")
                while True:
                    try:
                        pokemon_choice = int(input("\nWhich pokemon would you like to use against the enemy?:\t"))
                        friendly = inventory[0][pokemon_choice-1]
                        break
                    except IndexError:
                        print("\nPlease input a valid choice.")
                    except ValueError:
                        print("\nPlease only input integers.")

                print("\n\033[1;31mFIGHT STARTING\033[0m")
                time.sleep(0.5)
                print(".")
                time.sleep(0.5)
                print("..")
                time.sleep(0.5)
                print("...")
                time.sleep(0.5)
                if friendly.get_shiny() == True:
                    friendly_power = friendly.get_cp()*friendly.get_iv()*1.5
                else:
                    friendly_power = friendly.get_cp()*friendly.get_iv()
                if pokemon.get_shiny() == True:
                    enemy_power = pokemon.get_cp()*pokemon.get_iv()*1.5
                else:
                    enemy_power = pokemon.get_cp()*pokemon.get_iv()
                if friendly_power > enemy_power:
                    friendly.number_of_battles_won += 1
                    old_cp = friendly.get_cp()
                    old_stardust = inventory[2]
                    friendly.cp += int(random.randint(50, 150)*(1/friendly.number_of_battles_won))
                    inventory[2] += random.randint(800, 1500)
                    print(f"\nYour {friendly.get_name()} won!")
                    print(f"It gained {friendly.get_cp() - old_cp} CP!")
                    print(f"You gained {inventory[2] - old_stardust} Stardust!")
                    ran_away()
                    return
                else:
                    old_cp = friendly.get_cp()
                    friendly.cp -= random.randint(30, 150)
                    print(f"\nYour {friendly.get_name()} lost the battle!")
                    print(f"It was damaged and lost {old_cp - friendly.get_cp()} CP!")
                    ran_away()
                    return

            elif choice.lower() == 'n':
                ran_away()
                print(f"\nThe {pokemon.get_name()} ran away.")
                return
            else:
                print("\nPlease enter a valid input.")
    else:
        print("You are not next to a hostile pokemon.")

def run():
    while True:
        if keyboard.is_pressed('w'):
            time.sleep(0.1)
            move_map('up')
            print_map()
        if keyboard.is_pressed('s'):
            time.sleep(0.1)
            move_map('down')
            print_map()
        if keyboard.is_pressed('a'):
            time.sleep(0.1)
            move_map('left')
            print_map()
        if keyboard.is_pressed('d'):
            time.sleep(0.1)
            move_map('right')
            print_map()
        if keyboard.is_pressed('q'):
            clear_buffer()
            quit()
        if keyboard.is_pressed('f'):
            time.sleep(0.1)
            attempt_capture()
            print("\nYou can move again...")
        if keyboard.is_pressed('i'):
            time.sleep(0.1)
            clear_buffer()
            inventory_interact()
            print("\nYou can move again...")
        if keyboard.is_pressed('g'):
            time.sleep(0.3)
            clear_buffer()
            fight()
            print("\nYou can move again...")

print_instructions()
print_map()
run()