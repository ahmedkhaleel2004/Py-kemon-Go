import subprocess

# This game uses the keyboard module, which is prompted to automatically install here

try: 
    import keyboard
except ImportError:
    input("You are missing a required module. Would you like to automatically install it right now?\nY / N:\t")

    # I think this errors on MacOS? If it does, try "sudo pip3 install keyboard"

    subprocess.run(["pip", "install", "keyboard"])
import keyboard
import random
import time
import sys

# Import classes

from Pokemon_class import Pokemon, Candy

# This game uses a text file with all pokemon names and types, which is parsed through and indexed to lists here

file = open('first_gen_pokemon.txt', 'r')

pokemon_names = [] # [[charmander, charmeleon, charizard], [pikachu, raichu]]
pokemon_types = [] # [['fire', 'fire', 'fire/flying'], ['electric', 'electric']]

for line in file:
    names = []
    types = []
    data = line.split()

    # I can probably optimize this much better

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

# This is the inventory access function, containing all the 6 available options to interact with

def inventory_interact():
    print("\nAccessing inventory...")
    while True:

        # First enter a choice

        while True:
            choice = input("\n1:\tDisplay all caught pokemon\n2:\tShow pokemon stats\n3:\tShow available resources\n4:\tPower up a pokemon\n5:\tEvolve a pokemon\n6:\tQuit\n\nWhat would you like to do?:\t")
            if choice not in ['1','2','3','4','5','6']:
                print("\nPlease enter a valid choice.")
            else:
                break

        # Display all pokemon names on a new line
        
        if choice == '1':
            for i in range(len(inventory[0])):
                print(f"\n{i+1}:\t {inventory[0][i].get_name()}")

        # This one lets a user choose a pokemon that they have, and displays all of its stats, plus the costs

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

        # Display the values of candydict, showing base evolutionary family candies for each of their pokemon, plus stardust

        elif choice == '3':
            print("\nAvailable candies:")
            for key in inventory[1]:
                print(f"\t- {key} candy: {inventory[1][key].count}")
            print(f"\nAvailable stardust:\t{inventory[2]}")

        # Given valid choices, run the power up method
        
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

        # Given valid choices, run the evolve method
        
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

        # Exit the inventory
        
        elif choice == '6':
            break
        
        # Prompt user to exit inventory after each option

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

'''

Ok, time to render a map in the command line

'''

# I need a width and a height
width = 30
height = 15

# Where our player will always be in the center
x_x = width // 2
x_y = height // 2

'''
Essentially, the map render function works most efficiently by thinking of it as a grid

Our height is 15, meaning that we can think of it as 15 lists vertically, each with 30 items

Therefore, our top line (not part of the height), will also be 30 items long
'''

border = ['+', '+']
for i in range(width-1):
    border.insert(-1, '-')

# border is now a list with a '+' for each corner and dashes in the middle to show the border

# Time to define a bunch of global variables here before we jump into the nested stuff, these will come in handy later

map_list = []

'''
Note: 

This one is the most important.

map_list is a list of lists, which will always contain the 15 lists mentioned earlier.

We will now initialize them
'''

bottom_gone = []
top_gone = []
right_gone = []
left_gone = []

# For each row (15 from height)
for i in range(height):
    # We will create a row, starting with '|' for the edges
    row_list = ['|']

    # Making sure the player is in the middle
    if i == x_y:
        for i in range(x_x-1):
            row_list.append('/')
        row_list.append('X')
        for i in range(x_x-1):
            row_list.append('/')
        row_list.append('|')
        map_list.append(row_list)
        
    # Now for each of the 14 other lists not containing our player
    else:
        # Given a 10% chance...
        if random.randint(0, 100) < 10:
            # Fill some amount of the row with emptiness (a slash)
            for i in range(width-random.randint(2, 30)):
                row_list.append('/')
            # And then put in a '?' for a pokemon somewhere along there
            row_list.append("\033[1;31m?\033[0m")
            # Note: The '\033' indicates a breakout code for ANSI syntax, this allows the colouring
            # Then fill the rest with emptiness
            for i in range(width-len(row_list)):
                row_list.append('/')
            # Add our edge in
            row_list.append('|')
            # Finally, send it off to map_list
            map_list.append(row_list)
        # Given a less than 3% chance...
        elif random.randint(0, 100) < 3:
            # We will do the same, but this time for a green '!', indicating an enemy pokemon
            for i in range(width-random.randint(2, 30)):
                row_list.append('/')
            row_list.append("\033[1;32m!\033[0m")
            for i in range(width-len(row_list)):
                row_list.append('/')
            row_list.append('|')
            map_list.append(row_list)
        # And if none of those chances hit, the row is simple emptiness
        else:
            for i in range(width-1):
                row_list.append('/')
            row_list.append('|')
            map_list.append(row_list)
        
'''
After we have initialized the map, we will define all our functions

The order is a bit messy since thats how it was done during development

There are many functions, that are sometimes called in other functions, and will all be executed in run()
'''

# Simple print statements in the beginning
def print_instructions():
    print("\nWelcome to Py-kemon Go!")
    print("\nBuilt by Ahmed Khaleel and Ali Hussin")
    print("\nThis game only works when ran in a proper IDE like VSCode. Running this in the terminal or IDLE will cause lots of formatting issues.")
    print("\nControls:\n\t- WASD for moving around the map\n\t- 'F' to attempt a capture once you are next to a '?'\n\t- 'I' to access your inventory\n\t- 'G' to interact with an enemy pokemon '!'\n\t- 'Q' to quit")
    input("\nEnter any key to start.\t")

# This allows for the display of the map, joining all the lists together
def print_map():
    print("\033c")
    # Note: this print statement above is ANSI breakout code to clear the terminal
    print(''.join(border))
    for i in range(len(map_list)):
        print(''.join(map_list[i]))
    print(''.join(border))

# Row generator, essentially copied from above, but without the player
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

# Column generator in case the player wants to move to the left or right
# Only difference here is realistically 'width' being swapped with 'height'
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

# Move the map function, given a direction
def move_map(direction):

    '''
    In terms of directions, up and down are relatively the same, with only differences being the '-' or '+'

    Therefore, I will only include explanation of the 'up' and 'left' directions
    '''    

    # In order to move the map upwards
    if direction == 'up':

        # All the lines need to move down one, the top one is generated, and X (the player) moves up one line

        # Move the player up
        map_list[x_y][x_x] = '/'
        map_list[x_y-1][x_x] = 'X'
        # And here is where those 'gone' lists come in, used to store the information on the map that was previously on display
        bottom_gone.append(map_list.pop(-1))
        # Therefore, if the player had already moved down before this, if they were to move up, we can display the information that used to be there
        if len(top_gone) > 0:
            map_list.insert(0, top_gone.pop(-1))
        # And if it is newly discovered land, generate a row to place there
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

    # Up and down was simple enough, but for left and right, we need to deal with the second or second last item in each list
    if direction == 'left':
        # Move the player
        map_list[x_y][x_x] = '/'
        map_list[x_y][x_x-1] = 'X'
        # This list will be used to store the information that will be taken away
        right_column_downwards = []
        # And so for each row, take the second last item (because of the edges) and store it into its corresponding 'gone' list
        for i in range(height):
            right_column_downwards.append(map_list[i].pop(-2))
        right_gone.append(right_column_downwards)
        # Once again, if the player had already moved right, then we can just display the information that used to be there
        if len(left_gone) > 0:
            for i in range(height):
                map_list[i].insert(1, left_gone[-1][i])
            left_gone.pop(-1)
        # Otherwise, generate it
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

# This function uses random chances to chose a pokemon from the parsed lists, where a higher evolution is more rare
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

# This weird function deletes the input buffer from when a player was moving, so that it doesnt input all the keys pressed when they finally interact
def clear_buffer():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

# After an interaction is done, we need to remove the '?' or '!' that was around the player
def ran_away():
    for i in range(-1, 2):
        map_list[x_y+i][x_x] = '/'
        map_list[x_y][x_x+i] = '/'

# I want this game to be fast paced, and this multiplier quickly increases based on how many pokemon the player has
def current_multiplier():
    if len(inventory[0]) % 2 == 0:
        return len(inventory[0])/2
    else:
        return (len(inventory[0])/2)+0.5

# Creation of a pokemon, using our imported classes
def find_and_create_pokemon(pokemon_name: str):
    # Given a pokemon name, we need to find its type, and the evolutionary family it belongs to
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
    
    # To choose our CP, we will guess between 200 and 400 for a start
    # If the player has not caught any pokemon yet
    if current_multiplier() == 0:
        # Simply multiply the guess by the level of his evolution in the family
        cp = random.randint(200,400)*(y+1)
    # And otherwise, also multiply it by the current multiplier
    else:
        cp = int(random.randint(200,400)*(y+1)*current_multiplier()) # EXTREMELY oversimplified initial CP guess
    # Defining our family, being the first pokemon in that group
    family = pokemon_names[x][0]

    # Generating our stats, where the guess is between 1 and 4 initially
    randomstats = []
    for i in range(3):
        j = random.randint(1,4)
        randomstats.append(j)
    # And adjusted if its a higher evolution
    for i in randomstats:
        i = i*(y+1)
    
    # Implementation of a shiny catch, where it is set to 20% of pokemon (I want this to be fast paced)
    if random.randint(0, 100) < 20:
        isShiny = True
        print("This pokemon is \033[1;33mSHINY!\033[0m")
    else:
        isShiny = False

    # Finally, this function returns the creation of the pokemon, using all our defined variables
    return Pokemon(pokemon_name, typ, cp, family, randomstats, isShiny, pokemon_names)

# Catching a pokemon adds it to your inventory, rewards an adjusted amount of stardust, and ann adjusted amount of family candy for that pokemon
def catch_pokemon(pokemon_name: str):
    pokemon = find_and_create_pokemon(pokemon_name)
    pokemon.catch(inventory, random.randint(3, 20))
    inventory[1][pokemon.family].count = int(inventory[1][pokemon.family].count*current_multiplier())
    inventory[2] += int(random.randint(300, 1000)*current_multiplier())

# Checking for an ANSI escape code around the player (useful later)
def check_around_x(escape_code: str):
    return any(map_list[x_y+i][x_x] == escape_code for i in range(-1,2)) or any(map_list[x_y][x_x+i] == escape_code for i in range(-1,2))

# Attempts capture of a pokemon
def attempt_capture():
    clear_buffer()
    found_pokemon = random_pokemon()

    # If it is there
    if check_around_x('\033[1;31m?\033[0m'):
        print(f"You found a {found_pokemon}!")
        print("\nDo you want to attempt to capture it? It will run away if you don't.")
        # Prompt to catch
        while True:
            choice = input("Y / N:\t")
            if choice.lower() == 'y':
                attempts = 5
                # Where they will have 5 attempts
                while attempts > 1:
                    # And a 20% chance to catch it each attempt
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
                    # And it runs away if you run out of attempts
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

# Function to fight a nearby pokemon
def fight():
    # If it is there
    if check_around_x('\033[1;32m!\033[0m'):
        # We will create that pokemon
        pokemon = find_and_create_pokemon(random_pokemon())
        # And adjust its stats based on the player's progress in the game
        for i in range(3):
            if pokemon.stats[i] < 15:
                pokemon.stats[i] += int(1*current_multiplier())
                if pokemon.stats[i] > 15:
                    pokemon.stats[i] = 15
        # Calculate IV
        pokemon.iv = round((sum(pokemon.get_stats())/45)*100, 1)
        print(f"You found a hostile {pokemon.get_name()}!")
        print("\nIt's stats:")
        # And display its stats, to let the player choose whether or not they want to fight it
        pokemon.display_attributes(inventory, pokemon_names, True)
        
        # But if they don't have any pokemon already, it will run away by default
        if len(inventory[0]) == 0:
            print("\nYou do not have a pokemon available to fight yet.")
            ran_away()
            print(f"\nThe {pokemon.get_name()} ran away.")
            return
        
        # Prompt to fight
        while True:
            choice = input(f"\nDo you want to fight this {pokemon.get_name()}? It will run away if you don't. (Y / N):\t")
            # If yes
            if choice.lower() == 'y':
                # Show their available pokemon (no backing out now)
                print("\nYour available pokemon:")
                for i in range(len(inventory[0])):
                    # And their stats
                    print(f"\n{i+1}: {inventory[0][i].get_name()} CP: {inventory[0][i].get_cp()} IV: {inventory[0][i].get_iv()}% Shiny?: {inventory[0][i].get_shiny_text()}")
                while True:
                    try:
                        # Let them choose which one
                        pokemon_choice = int(input("\nWhich pokemon would you like to use against the enemy?:\t"))
                        # And assign it to 'friendly'
                        friendly = inventory[0][pokemon_choice-1]
                        break
                    except IndexError:
                        print("\nPlease input a valid choice.")
                    except ValueError:
                        print("\nPlease only input integers.")

                # Fighting simulation
                print("\n\033[1;31mFIGHT STARTING\033[0m")
                time.sleep(0.5)
                print(".")
                time.sleep(0.5)
                print("..")
                time.sleep(0.5)
                print("...")
                time.sleep(0.5)

                # Time to calculate power and who wins

                # The calculation will be as follows: power = CP * IV * (1.5 if SHINY)

                # Calculate friendly's power
                if friendly.get_shiny() == True:
                    friendly_power = friendly.get_cp()*friendly.get_iv()*1.5
                else:
                    friendly_power = friendly.get_cp()*friendly.get_iv()

                # Calculate enemy's power
                if pokemon.get_shiny() == True:
                    enemy_power = pokemon.get_cp()*pokemon.get_iv()*1.5
                else:
                    enemy_power = pokemon.get_cp()*pokemon.get_iv()

                # If friendly wins
                if friendly_power > enemy_power:
                    # Add one to his battles won
                    friendly.number_of_battles_won += 1
                    # We will increase CP and add stardust, so lets get the stats before
                    old_cp = friendly.get_cp()
                    old_stardust = inventory[2]
                    # Increase CP by some diminishing amount from 50 to 150
                    friendly.cp += int(random.randint(50, 150)*(1/friendly.number_of_battles_won))
                    # And add some amount of stardust from 800 to 1500
                    inventory[2] += random.randint(800, 1500)
                    # Display results
                    print(f"\nYour {friendly.get_name()} won!")
                    print(f"It gained {friendly.get_cp() - old_cp} CP!")
                    print(f"You gained {inventory[2] - old_stardust} Stardust!")
                    ran_away()
                    return
                else: # If enemy wins
                    # We will decrease friendly cp
                    old_cp = friendly.get_cp()
                    # By some amount 30 to 150
                    friendly.cp -= random.randint(30, 150)
                    # Display results
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

# Finally, we will define the run() function
def run():
    # Consistently check for...
    while True:
        # 'WASD', all the movement keys
        # And so if the player moves
        if keyboard.is_pressed('w'):
            # Sleep for a small time to avoid lag and allow playability
            time.sleep(0.1)
            # Move the map up
            move_map('up')
            # And display it again
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
        # If they want to quit
        if keyboard.is_pressed('q'):
            # Then quit
            clear_buffer()
            quit()
        # If they want to attempt capture
        if keyboard.is_pressed('f'):
            time.sleep(0.1)
            # Run its function
            attempt_capture()
            # And allow movement after
            print("\nYou can move again...")
        # 'I' to access inventory...
        if keyboard.is_pressed('i'):
            time.sleep(0.1)
            clear_buffer()
            inventory_interact()
            print("\nYou can move again...")
        # And 'G' to fight
        if keyboard.is_pressed('g'):
            time.sleep(0.3)
            clear_buffer()
            fight()
            print("\nYou can move again...")

# Lastly, call the functions
print_instructions()
print_map()
run()