'''
We will have two classes to import

Obviously, there is the Pokemon class...

But we also need a Candy class for the candy amounts
Since each pokemon uses its lowest evolution for the candy

Therefore, multiple pokemon of different higher evolutions will all use the same candy
'''


class Candy:
    # Initialize the family, and then the count to 0
    def __init__(self, family, count=0):
        self.family = family
        self.count = count

    # Add candy method
    def add(self, amount):
        self.count += amount

    # We will use a classmethod that acts on the whole class instead of only the 'self' object, since multiple objects will be under this one class
    @classmethod
    # And so to create the candy for the family
    # Class method used to intialize candy object for certain family
    def create_for_family(cls, family):
        # We will return the class with family and count
        return cls(family, count=0)


class Pokemon:

    # Before the __init__ we need to find other information about a given pokemon
    def find_in_names(self, pokemon_names):
        x = 0
        for i in pokemon_names:
            y = 0
            for j in i:
                if self.get_name() == j:
                    break
                y += 1
            if self.get_name() == j:
                break
            x += 1
        return [x, y]

    # Initialize all our variables
    def __init__(self, name, typ, cp, family, randomstats, isShiny, pokemon_names):
        self.name = name
        self.type = typ
        self.cp = cp
        self.stats = randomstats
        # Calculate IV given random initial stats
        self.iv = round((sum(randomstats)/45)*100, 1)
        self.shiny = isShiny
        self.family = family
        self.candy = Candy(family)
        self.candy_powerup = 2
        self.stardust_powerup = 1900
        # Unpack family and evolution from the method above
        x, y = self.find_in_names(pokemon_names)
        self.candy_evolve = 25 * (y+1)
        self.power_up_level = 0
        self.number_of_battles_won = 0

    # Accessor methods

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_cp(self):
        return self.cp

    def get_stats(self):
        return self.stats

    def get_iv(self):
        return self.iv

    def get_shiny(self):
        return self.shiny

    def get_candy_powerup(self):
        return self.candy_powerup

    def get_stardust_powerup(self):
        return self.stardust_powerup

    def get_candy_evolve(self):
        return self.candy_evolve

    def get_number_of_battles_won(self):
        return self.number_of_battles_won

    def get_shiny_text(self):
        x = self.get_shiny()
        if x == True:
            return "\033[1;33mYES!\033[0m"
        else:
            return "No"

    # Method to check if there does exist a higher evolution of the pokemon
    def canEvolve(self, pokemon_names):
        x, y = self.find_in_names(pokemon_names)
        if y+1 < len(pokemon_names[x]):
            return True
        else:
            return False

    # Stat and cost display method
    def display_attributes(self, inventory, pokemon_names, fight=False):
        print(f"\nName: {self.get_name()}")
        print(f"Type: {self.get_type()}")
        print(f"Combat Power: {self.get_cp()}")
        x = self.get_stats()
        print(f"Stats: {x[0]} Attack, {x[1]} Defense, {x[2]} Stamina")
        print(f"IV: {self.get_iv()}%")
        print(f"Number of battles won: {self.get_number_of_battles_won()}")
        # Print shiny state with ANSI colouring
        x = self.get_shiny()
        if x == True:
            print(f"Shiny?: \033[1;33mYES!\033[0m")
        else:
            print("Shiny?: No")

        # Then print costs if this method is not called for a hostile pokemon
        if fight == False:
            print(f"\nCosts:")

            # With green and red to check if the player can do it
            green = '\033[32m'
            red = '\033[31m'

            def powerup_msg(colour):
                print(f"{colour}You need {self.get_candy_powerup()} {self.family} candies and {
                      self.get_stardust_powerup()} stardust to power up this pokemon.\033[0m")

            def evolve_msg(colour):
                print(f"{colour}You need {self.get_candy_evolve()} {
                      self.family} candies to evolve this pokemon.\033[0m")

            if inventory[2] >= self.get_stardust_powerup() and inventory[1][self.family].count >= self.get_candy_powerup():
                powerup_msg(green)
            else:
                powerup_msg(red)

            if self.canEvolve(pokemon_names):
                if inventory[1][self.family].count >= self.get_candy_evolve():
                    evolve_msg(green)
                else:
                    evolve_msg(red)

    # Power up method

    # Essentially checks if player has enough, and powers pokemon up, removing the costs from the inventory

    def power_up(self, inventory, cp_increase, stats_chance, possible_increment):
        if inventory[2] >= self.get_stardust_powerup() and inventory[1][self.family].count >= self.get_candy_powerup():
            # Note: only powers up 10 times
            if self.power_up_level < 10:
                self.power_up_level += 1
                inventory[2] -= self.stardust_powerup
                old = self.cp
                self.cp += int(round(cp_increase*(1-(self.power_up_level/10))))
                print(f"\n{self.get_name()}'s CP increased by {
                      self.cp - old}!")
                # Costs increase
                # Stardust increases 300 each time
                self.stardust_powerup += 300
                # And candy increasing 1 every 3 powerups
                if self.power_up_level % 3 == 0:
                    self.candy_powerup += 1
                # Also a 50% chance to increase stats on a power up
                if stats_chance < 50:
                    self.stats = possible_increment
                    print(f"{self.get_name()}'s stats have also evolved!")
                    self.iv = round((sum(self.get_stats())/45)*100, 1)
            else:
                print("\nThis pokemon has been powered up a maximum of 10 times.")
        else:
            print(f"\nYou either do not have enough stardust or {
                  self.family} candies to power up this pokemon!")

    # Evolve method
    # Essentially checks if it can evolve, and subtracts costs
    # Where it then takes increments and adds it to stats
    # Then prints out results
    def evolve(self, inventory, pokemon_names, pokemon_types, cp_increase, stats_increment):
        if self.canEvolve(pokemon_names):
            if inventory[1][self.family].count >= self.get_candy_evolve():
                inventory[1][self.family].count -= self.get_candy_evolve()
                self.candy_evolve = self.candy_evolve * 2
                x, y = self.find_in_names(pokemon_names)
                old_name = self.name
                old_type = self.type
                self.name = pokemon_names[x][y+1]
                self.type = pokemon_types[x][y+1]
                self.power_up_level = 0
                old_cp = self.cp
                self.cp += cp_increase
                self.stats = stats_increment
                self.iv = round((sum(self.get_stats())/45)*100, 1)
                print(f"Your {old_name} ({old_type}) evolved into a {
                      self.name} ({self.type})! ")
                print(f"\n{self.get_name()}'s CP increased by {
                      self.cp-old_cp}!")
                x = self.get_stats()
                print(f"It's new stats are: {x[0]} Attack, {
                      x[1]} Defense, {x[2]} Stamina")
            else:
                print(f"\nYou do not have enough {self.family} candies!")
        else:
            print("\nThis pokemon cannot evolve any further.")

    # Catch method
    def catch(self, inventory, random):
        # Adds object to first list in inventory
        inventory[0].append(self)
        # And adds candy to candydict
        family = self.family
        # If this is the first time this family is being caught
        if family not in inventory[1]:
            inventory[1][family] = Candy.create_for_family(family)
        # And adds a random amount of candy
        inventory[1][family].add(random)
