"""
Project: Game Connect-4 in Terminal
File: connect_four.py
Author: Ivaylo Stoyanov - Devihem

Description: This is a basic project that recreates the game Connect 4. It is played in the terminal.
The script give the user options to choose a gameplay mode: default mode with two players and a standard board,
or a custom mode with two to six players and a custom board. In the custom mode, the user can choose the number of rows,
columns, and players. Each player can also choose a name and select a color.

Players take turns placing their tokens on the board by selecting a column.
If a player has four or more tokens in a row, column, or diagonal connected together the player wins.
If no player wins and the board is full, the game is considered a draw.
"""

import re
import random
import copy


# First user input possible for selecting game mode. The function return 'P' or 'Any input'
def choosing_game_play_mode():
    user_choice = input('\n┌─-----------------Choose-a-gameplay-mode----------------─┐'
                        '\n│ Versus AI     - One Player, Standard Board, AI          │'
                        '\n│ Normal        - Two Players, Standard Board             │'
                        '\n│ Party         - Two - Six Players, Custom Board         │'
                        '\n└─-------------------------------------------------------─┘\n'
                        '\n Type "AI" to play against Bot, type "N" for normal match or'
                        ' "P" for Party match and Press ENTER to continue :'
                        '\n => :  ')
    return user_choice


# Receiving user input for the game mode. Return how many rows, columns and players will teh game have.
def game_mod(user_mode_input: str):
    #  default values (Grid 6 x 7 ,  2 Players)
    custom_rows, custom_cols, custom_players = 6, 7, 2

    # if the selected mode is Party the user choose one by one the parameters.
    if user_mode_input.upper() == 'P':

        # Rows input with try/except. If input is incorrect the error is raised and the input is repeated.
        while True:
            try:
                custom_rows = int(input('\nHow many ROWS [ 1 - 99 ] ?'
                                        '\nRecommended ROWS [ 4 to 10 ] => : '))
                if 0 < custom_rows < 100:
                    break
                else:
                    raise ValueError

            except ValueError:
                print('\nIncorrect input !\nExpected input - integer number in the given range [ 1 - 99 ]')
                continue

        # Columns input with try/except. If input is incorrect the error is raised and the input is repeated.
        while True:
            try:
                custom_cols = int(input('\nHow many COLUMNS [ 1 - 99 ] ?'
                                        '\nRecommended COLUMNS [ 4 to 16 ] => : '))
                if 0 < custom_cols < 100:
                    break
                else:
                    raise ValueError

            except ValueError:
                print('\nIncorrect input !\nExpected input - integer number in the given range [ 1 - 99 ]')
                continue

        # Player count input with try/except. If input is incorrect the error is raised and the input is repeated.
        while True:
            try:
                custom_players = int(input('\nHow many PLAYERS [ 1 - 6 ] ?'
                                           '\nRecommended PLAYERS [ 2 to 4 ] => : '))
                if 0 < custom_players < 7:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('\nIncorrect input !\nExpected input - integer number in the given range [ 1 - 6 ]')
                continue

        # Return custom parameters
        return custom_rows, custom_cols, custom_players

    else:
        # Return default parameters
        return custom_rows, custom_cols, custom_players


# If game mode is Party function return players name and color selected by users , otherwise return default values
def players_name_and_color(new_players_count: int, user_mode_input: str):
    players_dictionary = {}

    # All colors available
    colors_list = ['\033[1;31m██\033[0m', '\033[1;32m██\033[0m', '\033[1;33m██\033[0m',
                   '\033[1;34m██\033[0m', '\033[1;35m██\033[0m', '\033[1;37m██\033[0m']

    # If Custom mode is selected
    if user_mode_input.upper() == 'P':

        # While loop until the selected players count is the same as the dictionary keys ( Players )
        while len(players_dictionary.keys()) < new_players_count:
            new_player_name = input('\nWelcome, enter your name, between [4-20] characters from [ a-z, A-Z, 0-9 , _ ]'
                                    '\nEnter Your name => : ')

            # Username validation in 4 steps - Valid format 4-20 - characters [a-z, A-Z, 0-9, _] and to be unique:
            # Check_1 - if name is empty
            if not new_player_name:
                print('\nPlayer name cannot be empty !')
                continue

            # Check_2 - if name is not within correct length
            if len(new_player_name) < 4 or len(new_player_name) > 20:
                print('\nPlayer name length not in range [ 4 - 20 ] !')
                continue

            # Check_3 - if name contain not allowed characters, (Regex check for all symbols except [^_a-zA-Z0-9] )
            if re.findall(r'\W+', new_player_name):
                print('\nPlayer name contains not allowed characters')
                continue

            # Check_4 if name already exist return user to the player name-input, until correct name is written.
            if new_player_name in players_dictionary.keys():
                # For better visualisation print the error and the usernames that already exist
                print(f'\nThis Player name already exist !'
                      f'\nPlayers names that already used: {", ".join(players_dictionary.keys())}')
                continue

            # Player choose his color , with int index , repeat until correct index is typed
            while True:

                # Print Colors and their Index underneath
                print('\n', *colors_list)
                print(''.join((f'  {color_index}' for color_index in range(1, len(colors_list) + 1))))

                # Color index input - try/except. If input is incorrect the error is raised and the input is repeated.
                try:
                    player_color = int(input('Please select your color !\nColor number => : '))
                    if 0 < player_color <= len(colors_list):

                        players_dictionary[new_player_name] = colors_list.pop(player_color - 1)
                        print(f'\n{players_dictionary[new_player_name][0:7]} {new_player_name}\033[0m '
                              f'You are set and ready !')
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print(f'Incorrect input ! '
                          f'Expected input - integer number in the given range [ 1 - {len(colors_list)} ]')
                    continue

    elif user_mode_input.upper() == 'N':
        # Return Default Player 1  and Player 2 information for quick games.
        players_dictionary['Player_1'] = colors_list.pop(0)  # Red Current Index
        players_dictionary['Player_2'] = colors_list.pop(2)  # BLue Current Index

    elif user_mode_input.upper() == 'AI':
        # Return Default Player 1  and Player 2 - AI information for quick games.
        players_dictionary['Player_1'] = colors_list.pop(0)  # Red Current Index
        players_dictionary['Player_2_AI'] = colors_list.pop(2)  # BLue Current Index

    # When all the data is fill out correctly return dictionary in format (Player-name : [Color_code + symbol])
    return players_dictionary


# Receiving matrix row and col and Creating empty board/matrix , also create columns indexes list and return them.
def board_creating(matrix_rows: int, matrix_cols: int):
    board_matrix = [['  ' for _ in range(matrix_cols)] for _ in range(matrix_rows)]
    columns_index_print = [' ' + str(x) if x < 10 else str(x) for x in range(1, number_of_cols + 1)]
    return board_matrix, columns_index_print


# Making check  for possible places to put the token. Returning free columns and flag.
def check_free_columns(matrix_board: list, matrix_cols: int):
    free_cols = [(index_col + 1) for index_col in range(matrix_cols) if matrix_board[0][index_col] == '  ']
    return free_cols


# Take the user input and check it if is valid, return correct index for token place
def player_token_placement(p_symbol: str, p_name: str, free_columns_index: list, matrix):
    #  Repeating the player input if it's incorrect or the index is wrong
    if p_name == "Player_2_AI":
        return monte_carlo_ai_placement(matrix)

    while True:

        try:
            column_index_place = int(input(f'\nWhere you want to place your token'
                                           f' {p_symbol[0:9]} {p_name}\033[0m ?\n => :  ')) - 1

            # If index is incorrect raise error
            if column_index_place + 1 not in free_columns_index:
                raise ValueError

            # stop the loop and return correct index for placing the player symbol
            return column_index_place

        # if error occurred print error message and show the free columns for placement
        except ValueError:
            print(f'\nIncorrect input !'
                  f'\nExpected input - Integer number. One, from the free columns indexes {free_columns_index}')


#  Placing the token, checking from the lowest to the upper floor/level  for empty cell / box
def place_token(board_matrix: list, matrix_rows: int, col_to_place: int, p_symbol: str):
    # Starting form the bottom of the board/matrix
    for current_row in range(matrix_rows - 1, -1, -1):

        # There is no else case, there is at least one free space guaranteed from check_free_columns().
        if board_matrix[current_row][col_to_place] == '  ':
            board_matrix[current_row][col_to_place] = p_symbol

            # Creating variable for where was placed the last token.
            last_row_col_placement = (current_row, col_to_place)

            # Return updated matrix/board and the coordinates of the last token placed
            return board_matrix, last_row_col_placement


# Function to check if there is a winner after every placement on board
def winner_check(matrix_board: list, p_symbol: str, last_r_c_token_placed: tuple, matrix_rows: int, matrix_cols: int):
    row, col = last_r_c_token_placed

    # Win pattern, going in both direction in the matrix with positive or negative step( -1 , +1 ).
    directions = (
        # (R, C) # First direction | Second direction
        (1, 0),  # Bottom - Top
        (0, 1),  # Right - Left
        (1, 1),  # Prime Diagonal
        (1, -1)  # Secondary Diagonal
    )

    # Checking every possible direction for least 4 connected/same blocks
    for dir_r, dir_c in directions:

        # The last token itself is already 1 of 4 blocks , counter = 1
        counter = 1

        # Using positive or negative step to check in both direction of a row , column or diagonal
        for direction_step_pos_or_neg in [1, -1]:

            # Checking maximum tree blocks in direction is the limit for longest chain , or maximum 7 blocks connected.
            for dir_step in range(1, 4):

                #  Token index  row/col  + ( direction pattern * dir_step (1,2,3) * step (+1 , -1 )
                new_r = row + dir_r * dir_step * direction_step_pos_or_neg
                new_c = col + dir_c * dir_step * direction_step_pos_or_neg

                # check if the new created indexes are in range of the matrix/board
                if 0 <= new_r < matrix_rows and 0 <= new_c < matrix_cols:

                    # if there is the same symbol there as the current player  counter add 1
                    if matrix_board[new_r][new_c] == p_symbol:
                        counter += 1
                    # else stop checking in this direction
                    else:
                        break

        # if counter is at least 4 = four or more connected same elements , return True ( current player is Winner )
        if counter >= 4:
            return True
    # return False there is still no winner
    return False


# Taking input from user and return boolean statement for new_game_flag
def another_game():
    # The loop is repeated until correct input yes or no.
    while True:
        do_you_want_new_game = input('\n\nDo you want to play again [YES/NO] ? \n => : ')
        if do_you_want_new_game.upper() == 'YES':
            return True
        elif do_you_want_new_game.upper() == 'NO':
            return False
        else:
            print(f'\nIncorrect input !')


# Print - WELCOME
def starting_print():
    print(' _______                                         _     _ '
          '\n(_______)                               _       | |   (_)'
          '\n _       ___  ____  ____  _____  ____ _| |_     | |_____ '
          '\n| |     / _ \\|  _ \\|  _ \\| ___ |/ ___|_   _)    |_____  |'
          '\n| |____| |_| | | | | | | | ____( (___  | |_           | |'
          '\n \\______)___/|_| |_|_| |_|_____)\\____)  \\__)          |_|'
          '\n')


# Print - GAME BOARD
def board_print(matrix_board: list, columns_print: list, matrix_cols: int):
    # Spacing from other prints
    print('\n\n\n\n\n\n\n')

    # Top frame
    print('┌─' + '───┬─' * (matrix_cols - 1) + '───┐')

    # Columns with numbers
    print('│', ' │ '.join(columns_print), '│')

    # Every mid row and matrix row.
    [print('├─' + '───┼─' * (matrix_cols - 1) + '───┤\n' + '│ ' + ' │ '.join(x), end=' │\n') for x in matrix_board]

    # Bottom frame
    print('└─' + '───┴─' * (matrix_cols - 1) + '───┘\n')


def winner_print(p_symbol: str, p_name: str):
    print(
        f'\n┌─---------CONGRATULATION-----------┐'
        f'\n            {p_symbol[0:9]} {p_name}\033[0m                    '
        f'\n└─-------------YOU-WIN--------------┘'
    )


def draw_print():
    print(
        f'\n┌─-----------GOOD-GAME-----------┐'
        f'\n           THIS ROUND IS                    '
        f'\n└─-------------DRAW--------------┘'
    )


#######################################################################################################################
#######################################################################################################################
def monte_carlo_ai_placement(matrix):
    ai_placement = 0
    ai_color = '\033[1;33m██\033[0m'

    best_position = 0
    while True:
        mc_matrix = copy.deepcopy(matrix)

        free_cols = check_free_columns(mc_matrix, len(mc_matrix[0]))
        print(free_cols)
        break

    print(*matrix, sep='\n')
    [print(''.join(x)) for x in matrix]

    return ai_placement


#######################################################################################################################
#######################################################################################################################
#  Welcome, Print with script name.
starting_print()

# User choose - Gameplay mode , Custom or Default
# gameplay_mode = choosing_game_play_mode()
gameplay_mode = "AI"

# Common variables for creating the game board and saving players' info.
number_of_rows, number_of_cols, players = game_mod(gameplay_mode)

# All players are added in dictionary with their personal name and color
players_dict = players_name_and_color(players, gameplay_mode)

# Board creating
board, columns_print_for_representation = board_creating(number_of_rows, number_of_cols)

# Flags for end game. First scenario - Player Win , Second scenario - Players are Draw  or New game can be selected.
winner_flag = False
end_game_flag = False
new_game_flag = False

# While one of two condition is met [Winner] or [No more moves].
while not winner_flag and not end_game_flag:

    # Using for-loop to rotate players turns.
    for player_name, players_symbol in players_dict.items():

        # Printing the gaming board
        board_print(board, columns_print_for_representation, number_of_cols)

        # Checking witch columns have at least one empty space ( checking only the top row )
        free_columns = check_free_columns(board, number_of_cols)

        # Player choose where to place the token ( in witch column )
        column_to_place = player_token_placement(players_symbol, player_name, free_columns, board)

        # Placing the color token in the board
        board, r_c_last_token = place_token(board, number_of_rows, column_to_place, players_symbol)

        # Check if there is a winner ( based on last placed token )
        winner_flag = winner_check(board, players_symbol, r_c_last_token, number_of_rows, number_of_cols)

        # Check if there is more empty spaces
        end_game_flag = False if len(check_free_columns(board, number_of_cols)) > 0 else True

        # if any of the flag is raised stop the loop
        if winner_flag or end_game_flag:

            # Print the final state of the board
            board_print(board, columns_print_for_representation, number_of_cols)

            # Print Winner
            if winner_flag:
                winner_print(players_symbol, player_name)

            # Print Draw
            elif end_game_flag:
                draw_print()

            # Option for new round available only in the end of the game
            new_game_flag = another_game()
            break

    # If new round is selected the game continue after the players name and color selection.
    if new_game_flag:
        # Reset all flags and create new empty board.
        winner_flag = False
        end_game_flag = False
        new_game_flag = False
        board, columns_print_for_representation = board_creating(number_of_rows, number_of_cols)
        continue

print('\n\nThank you for playing Connect-4 made by me! Goodbye!')
