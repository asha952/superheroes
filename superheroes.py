from random import randint, choice

class Ability:
    def __init__(self, name, attack_strength):
        self.name = name
        self.max_damage = attack_strength

    def attack(self):
        return randint(0, self.max_damage)

class Armor:
    def __init__(self, name, max_block):
        self.name = name
        self.max_block = max_block

    def block(self):
        return randint(0, self.max_block)

class Hero:
    def __init__(self, name, starting_health=100):
        self.abilities = []
        self.armors = []
        self.name = name
        self.starting_health = starting_health
        self.current_health = starting_health
        self.kills = 0
        self.deaths = 0

    def add_ability(self, ability):
        self.abilities.append(ability)

    def attack(self):
        total_damage = 0
        for ability in self.abilities:
            total_damage += ability.attack()
        return total_damage

    def add_armor(self, armor):
        self.armors.append(armor)

    def defend(self, damage_amt=0):
        blocked = 0
        for armor in self.armors:
            block = armor.block()
            blocked += block
        return blocked

    def take_damage(self, damage):
        current_heath = self.current_health
        damage_defense = self.defend(damage)

        self.current_health = current_heath - damage_defense

    def is_alive(self):
        return self.current_health > 0

    def fight(self, opponent):
        while self.is_alive() and opponent.is_alive():

            self.take_damage(opponent.attack())
            opponent.take_damage(self.attack())

            if opponent.current_health <= 0:
                print('=' * 24)
                print('BATTLE:\n')
                print(f'\n{self.name} beat {opponent.name} and won!')
                self.add_kill(1)
                opponent.add_deaths(1)
                break

            elif self.current_health <= 0:
                print('=' * 24)
                print('BATTLE:\n')
                print(f'\n{opponent.name} beat {self.name} and won!')
                opponent.add_kill(1)
                self.add_deaths(1)
                break
            else:
                # Indicates a tie, no print message necessary to avoid spam until one wins
                pass

    def add_kill(self, num_kills):
        self.kills += num_kills

    def add_deaths(self, num_deaths):
        self.deaths += num_deaths

    def add_weapon(self, weapon):
        self.abilities.append(weapon)


class Weapon(Ability):
    def attack(self):
        return randint(self.max_damage // 2, self.max_damage)


class Team():
    def __init__(self, name):
        self.name = name
        self.hero_list = []

    def remove_hero(self, name):
        for hero in self.hero_list:
            if hero.name == name:
                self.hero_list.remove(hero)
                break
        return 0

    def view_all_heroes(self):
        for hero in self.hero_list:
            print(hero.name)

    def add_hero(self, hero):
        self.hero_list.append(hero)

    def team_alive(self):
        heroes = []
        for hero in self.hero_list:
            if hero.is_alive():
                heroes.append(hero)
        return heroes

    def attack(self, other_team):
        while len(self.team_alive()) > 0 and len(other_team.team_alive()) > 0:
            heroes = choice(self.team_alive())
            enemy_list = choice(other_team.team_alive())

            heroes.fight(enemy_list)

    def revive_heroes(self, health=100):
        for heroes in self.hero_list:
            heroes.current_health = heroes.starting_health  

    def stats(self):
        team_kills = 0
        team_deaths = 0
        for hero in self.hero_list:
            team_kills += hero.kills
            team_deaths += hero.deaths

            kd = round(hero.kills / hero.deaths,
                       2) if hero.deaths > 0 else hero.kills
            print(f'{hero.name} has {hero.kills} kills and {hero.deaths} deaths')
            print(f'{hero.name} has a KD of: {kd}')

        return round(team_kills / team_deaths, 2) if team_deaths > 0 else team_kills


class Arena:
    def __init__(self):
        self.team_one = Team('Team 1 Heroes')
        self.team_two = Team('Team 2 Heroes')

    def create_ability(self):
        ability_name = input('Create an ability name: ')
        while True:
            damage_input = input(
                'Enter the max amount of damage for your ability: ')
            if damage_input.isnumeric():
                break
            elif damage_input.isalnum():
                print('Please enter an input with numbers only')
        return Ability(ability_name, int(damage_input))

    def create_weapon(self):
        weapon_name = input('Create a weapon name: ')

        while True:
            weapon_damage = input('Enter how much damage your item will do: ')
            if weapon_damage.isnumeric():
                break
            elif weapon_damage.isalnum():
                print('Please enter an input with numbers only')

        return Weapon(weapon_name, int(weapon_damage))

    def create_armor(self):
        armor_name = input('Create an armor name: ')

        while True:
            block_input = input('Enter how much your armor will block: ')
            if block_input.isnumeric():
                break
            elif block_input.isalnum():
                print('Please enter an input with numbers only')

        return Armor(armor_name, int(block_input))

    """
    Allows the user to create heroes with ability, weapon, and armor customization
    Returns: The user's custom heroes
    """

    def create_hero(self):
        hero_name = input('Enter the name of your hero: ')

        while True:
            health_input = input('Enter how much health your hero will have: ')
            if health_input.isnumeric():
                break
            elif health_input.isalnum():
                print('Please enter an input with numbers only')

        user_hero = Hero(hero_name, int(health_input))

        while True:
            ask_ability = input('Would you like abilities? (Y/N): ').lower()
            if ask_ability == 'y':
                user_ability = self.create_ability()
                user_hero.add_ability(user_ability)
                break
            elif ask_ability == 'n':
                break
            else:
                print('\nYou must answer Y or N')

        while True:
            ask_weapon = input('Would you like weapons? (Y/N): ').lower()
            if ask_weapon == 'y':
                user_weapon = self.create_weapon()
                user_hero.add_weapon(user_weapon)
                break
            elif ask_weapon == 'n':
                break
            else:
                print('\nYou must answer Y or N')

        while True:
            ask_armor = input('Would you like armor? (Y/N): ').lower()
            if ask_armor == 'y':
                user_armor = self.create_armor()
                user_hero.add_armor(user_armor)
                break
            elif ask_armor == 'n':
                break
            else:
                print('\nYou must answer Y or N')

        return user_hero

    """
    Allows the user to create teams and decide how many heroes will be on each team and calls the
    create_hero method
    """

    def build_team_one(self):
        add_hero_team = int(
            input('How many heroes would you like on team one? '))

        for amount in range(add_hero_team):
            self.team_one.add_hero(self.create_hero())

        hero_list = [hero.name for hero in self.team_one.hero_list]
        print(f'Heroes on Team 1: {", ".join(hero_list)}')

    def build_team_two(self):
        add_hero_team = int(
            input('How many heroes would you like on team two? '))

        for amount in range(add_hero_team):
            self.team_two.add_hero(self.create_hero())

        hero_list = [hero.name for hero in self.team_two.hero_list]
        print(f'Heroes on Team 2: {", ".join(hero_list)}')

    def team_battle(self):
        self.team_one.attack(self.team_two)

    """
    Prints out the battle statistics including the team's average KD ratio and declares winner
    """

    def show_stats(self):
        print('=' * 24)
        print('TEAM ONE STATISTICS: \n')
        print(f'\nTeam one\'s stats: {self.team_one.stats()}\n')

        print('=' * 24)

        print('TEAM TWO STATISTICS: \n')
        print(f'\nTeam two\'s stats: {self.team_two.stats()}\n')
        print('=' * 24)

        print('FIGHT OUTCOME: \n')
        if self.team_one.team_alive():
            hero_list = [hero.name for hero in self.team_one.hero_list]
            print(
                f'Team 1 is victorious!\nChampions: {", ".join(hero_list)}')
        else:
            hero_list = [hero.name for hero in self.team_two.hero_list]
            print(
                f'Team 2 is victorious!\nChampions: {", ".join(hero_list)}')
        print('=' * 24)


if __name__ == "__main__":
    game_is_running = True

    # Instantiate Game Arena
    arena = Arena()

    # Build Teams
    arena.build_team_one()
    arena.build_team_two()

    while game_is_running:

        arena.team_battle()
        arena.show_stats()
        play_again = input("Play Again? Y or N: ")

        # Check for Player Input
        if play_again.lower() == "n":
            game_is_running = False

        else:
            # Revive heroes to play again
            arena.team_one.revive_heroes()
            arena.team_two.revive_heroes()
