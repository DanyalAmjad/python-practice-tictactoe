# Tic Tac Toe
# GAME MODES (1player, 2player, 1 vs AI,  AI vs AI)
# The board will refresh after each move.
# At the end of the game there will be an option to check

import random as r


class Game:
    def __init__(self, game='TicTacToe', new_game=True):
        self.game = game
        self.new_game = new_game
        self.game_data = None
        self.moves_made = None
        self.players = None
        self.symbol_taken = None
        self.counter = None
        Game.clear_board(self)

    def clear_board(self, rematch=False):
        # initialize the board for a new game
        if self.new_game or rematch:
            self.game_data = {i: [i] for i in range(1, 10)}
            print(f"The board is cleared. Ready for a new game of {self.game}!")
            self.moves_made = []
            self.players = []
            self.symbol_taken = []
            self.counter = 1
            self.new_game = False

    def __repr__(self):
        layout = ''
        for index in range(1, len(self.game_data) + 1):
            converted_value = str(self.game_data[index][0])
            if index % 3 == 0:
                layout += ' [' + converted_value + '] '
                layout += '\n'
                if index != 9:
                    layout += '=====|=====|=====' + '\n'
            else:
                layout += ' [' + converted_value + '] '
                layout += '|'
        return layout

    @staticmethod
    def title():
        print("=======================================================")
        print("XXXXX X  XXXX  =====   ^      =====  00OOO OOO  OOOOO  ")
        print("  X   X X        |    / \    ||        O  O   O O      ")
        print("  X   X X        |   /   \   ||        O  O   O OOOO   ")
        print("  X   X X        |  / === \  ||        O  O   O O      ")
        print("  X   X  XXXX    | /       \  =====    O   OOO  OOOOO  ")
        print("=======================================================")

    def create_players(self):
        # ask player count to decide human vs AI players. If 0, results in 2 AI players
        num_players = int(input(
            f"""Welcome to TicTacToe!\nHow many players are playing {self.game}?\nChoose: '1' for 1-player, '2' for 2-players, '0' to kick back and watch two intelligent AI battle it out: """))
        if 1 <= num_players < 3:
            while len(self.players) < num_players:
                player = len(self.players) + 1
                player_name = (input(f"Player {player}, type your gamer name: ")).title()
                if len(self.players) != 0:
                    player_symbol = 'X' if 'X' not in self.symbol_taken else 'O'
                    print(f"{player_name} was automatically assigned the remaining symbol '{player_symbol}'.")
                else:
                    player_symbol = (input(f"{player_name}, choose 'X' or 'O' for your symbol: ")).upper()

                Player(player_name, self, player_symbol, is_ai=False)

        # create AI against human
        if num_players == 1:
            player_symbol = 'X' if 'X' not in self.symbol_taken else 'O'
            Player('Megatron', self, player_symbol, is_ai=True)
            print("Megatron will be your AI opponent. Good Luck!")

        # create 2 AI against each other
        if num_players == 0:
            Player('Megatron', self, 'X', is_ai=True)
            Player('Optimus Prime', self, 'O', is_ai=True)
            print("You will witness a battle for supremacy between Optimus Prime and Megatron!")

        elif 0 > num_players > 2:
            print('the number is out of range. im too lazy to fix this issue.')

    def coin_flip(self):
        player_choice = 0
        while player_choice > 3 or player_choice < 1:
            player_choice = int(input("Type '1' for player-1 go first, '2' for player-2 to go first, or '3' for a coin flip: "))
            if player_choice == 3:
                player_choice = r.randint(1, 2)
                print(f"The coin toss concluded that {self.players[player_choice - 1].name} will go first.")
            elif int(player_choice) == 1 or int(player_choice) == 2:
                print(f"{self.players[player_choice - 1].name} will go first.")
                player_choice = int(player_choice)
            else:
                print("You have not made a valid choice.")
        return player_choice

    def game_play(self, rematch=False):
        Game.title()
        Game.clear_board(self, rematch)
        Game.create_players(self)
        current_player = Game.coin_flip(self)

        # from turn 1 until all 9 squares are marked
        winning_conditions = False
        while self.counter <= 9:
            print(self)
            self.players[current_player - 1].make_move()

            # check if winning conditions are met after the player makes a move
            if ((self.game_data[1] == self.game_data[2] == self.game_data[3]) or
                    (self.game_data[4] == self.game_data[5] == self.game_data[6]) or
                    (self.game_data[7] == self.game_data[8] == self.game_data[9]) or
                    (self.game_data[1] == self.game_data[4] == self.game_data[7]) or
                    (self.game_data[2] == self.game_data[5] == self.game_data[8]) or
                    (self.game_data[3] == self.game_data[6] == self.game_data[9]) or
                    (self.game_data[1] == self.game_data[5] == self.game_data[9]) or
                    (self.game_data[3] == self.game_data[5] == self.game_data[7])):
                print(self)
                winning_conditions = True
                break
            current_player = 1 if current_player == 2 else 2
            self.counter += 1

        # if someone wins
        if winning_conditions:
            print(f"CONGRATS {self.players[current_player - 1].name.upper()} WON IN {self.counter} TURNS!!!")

        # if no one wins
        else:
            print(self)
            print("It's a Tie game")

        print("===============Game Over===============")

        # Ask for Moves Data and Rematch, only if there is a non AI player
        if (self.players[1].ai == False) or (self.players[0].ai == False):

            # Asking if player requires game details
            game_details = input(
                "Would you like to see a play by play of the moves made? Type yes or no: ").lower()
            if game_details == 'yes':
                for x in range(len(self.moves_made)):
                    i = self.moves_made[x]
                    print(f"{i[0]}. {i[1]} put an {i[3]} on box number {i[2]}.")
            print("----------------End of Data--------------------")

            # Asking if player wants a rematch
            rematch_input = input("Would players like a re-match? Type yes or no: ").lower()
            if rematch_input == 'yes':
                Game.game_play(self, rematch=True)


class Player:
    def __init__(self, name, game, symbol, is_ai=False):
        self.name = name
        self.game = game
        self.symbol = symbol
        self.ai = is_ai
        self.game.symbol_taken.append(self.symbol)
        self.game.players.append(self)

    def make_move(self):
        player_move = None
        while player_move == None or self.game.game_data[player_move] != [player_move]:
            if self.ai == True:
                player_move = r.randint(1, 9)
            else:
                player_move = int(input(f"{self.name}, pick an empty cell with a number to place your symbol: "))

        if self.ai == True:
            print(f"{self.name} put an '{self.symbol}' on cell {player_move}.")
        self.game.game_data[player_move] = [self.symbol]
        self.game.moves_made.append([self.game.counter, self.name, player_move, self.symbol])


game1 = Game()
game1.game_play()
