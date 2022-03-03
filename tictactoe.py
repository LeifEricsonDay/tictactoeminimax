import random


class Move:
    def __init__(self, index, score):
        self.index = index
        self.score = score


def minimax(board, shape):
    possible_moves = available_squares(board)
    score = 0
    if get_state(board) == "X wins":
        score = Move([], -10)
        return score
    elif get_state(board) == "O wins":
        score = Move([], 10)
        return score
    elif len(possible_moves) == 0:
        score = Move([], 0)
        return score
    scored_moves = []
    for current_move in possible_moves:
        move_object = Move([current_move[0], current_move[1]], 0)
        new_board = board_update(board, [move_object.index[0], move_object.index[1]])
        if shape == "X":
            result = minimax(new_board, "O")
            move_object.score = result.score
        else:
            result = minimax(new_board, "X")
            move_object.score = result.score
        new_board[move_object.index[0] - 1][move_object.index[1] - 1] = " "
        scored_moves.append(move_object)
    best_move = []
    if shape == "X":
        best_score = 100
        for current_move in scored_moves:
            if current_move.score < best_score:
                best_score = current_move.score
                best_move = current_move
    else:
        best_score = -100
        for current_move in scored_moves:
            if current_move.score > best_score:
                best_score = current_move.score
                best_move = current_move
    return best_move


def check_win(board, shape): # Checks to see if the shape has a winning move and returns winning move
    for index, row in enumerate(board):
        if row.count(shape) == 2 and row.count(" ") == 1:
            winning_index = row.index(" ")
            return[index+1, winning_index+1]
    for index in range(3):
        if [row[index] for row in board].count(shape) == 2 and [row[index] for row in board].count(" ") == 1:
            winning_index = [row[index] for row in board].index(" ")
            return [winning_index + 1, index + 1]
    if [board[i][i] for i in range(3)].count(shape) == 2 and [board[i][i] for i in range(3)].count(" ") == 1:
        winning_index = [board[i][i] for i in range(3)].index(" ")
        return [winning_index + 1, winning_index + 1]
    if [board[2-i][i] for i in range(3)].count(shape) == 2 and [board[2-i][i] for i in range(3)].count(" ") == 1:
        winning_index = [board[2-i][i] for i in range(3)].index(" ")
        return [3 - winning_index, winning_index + 1]
    return False


def get_state(board):
    for row in board:
        if all(x == "X" for x in row):
            return "X wins"
        elif all(x == "O" for x in row):
            return "O wins"
    for i in range(3):
        if all(row[i] == "X" for row in board):
            return "X wins"
        elif all(row[i] == "O" for row in board):
            return "O wins"
    if all(board[i][i] == "X" for i in range(3)) or all(board[2 - i][i] == "X" for i in range(3)):
        return "X wins"
    elif all(board[i][i] == "O" for i in range(3)) or all(board[2 - i][i] == "O" for i in range(3)):
        return "O wins"
    if sum(row.count("X") for row in board) + sum(row.count("O") for row in board) == 9:
        return "Draw"
    else:
        return "Game not finished"


def available_squares(board):
    available = []
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == " ":
                available.append([i+1, j+1])
    return available


def computer_move(board, player_type, shape):
    possible_moves = available_squares(board)
    if player_type == "easy":
        computers_move = random.choice(possible_moves)
    elif player_type == "medium":
        winning_move = check_win(board, shape)
        if not winning_move:
            blocking_move = check_win(board, ("X" if shape == "O" else "O"))
            if not blocking_move:
                computers_move = random.choice(possible_moves)
            else:
                computers_move = blocking_move
        else:
            computers_move = winning_move
    else:
        hard_move_object = minimax(board, shape)
        computers_move = [hard_move_object.index[0], hard_move_object.index[1]]
    return computers_move


def board_print(board):
    print("-" * 9)
    for row in board:
        print("|", *row, "|")
    print("-" * 9)


def board_input():
    while True:
        cell_values = list(input("Enter the cells:\n"))
        if len(cell_values) != 9:
            print("Invalid input!")
            continue
        for index, x in enumerate(cell_values):
            if x == "_":
                cell_values[index] = " "
        for val in cell_values:
            if val not in ["X", "O", " "]:
                print("Invalid input!")
                continue
        break
    listed_board = []
    for j in range(3):
        temp_row = []
        for i in range(3):
            temp_row.append(cell_values[i + 3 * j])
        listed_board.append(temp_row)
    return listed_board


def move(board, players_type, shape):
    if players_type == "user":
        players_move = user_move(board)
    else:
        if players_type == "easy":
            print("Making move level \"easy\"")
            players_move = computer_move(board, "easy", shape)
        elif players_type == "medium":
            print("Making move level \"medium\"")
            players_move = computer_move(board, "medium", shape)
        else:
            print("Making move level \"hard\"")
            players_move = computer_move(board, "hard", shape)
    return players_move


def user_move(board):
    while True:
        users_move = input("Enter the coordinates:\n")
        try:
            users_move = list(map(int, users_move.split()))
        except ValueError:
            print("You should enter numbers!")
            continue
        if not all([coordinate in range(1, 4) for coordinate in users_move]):
            print("Coordinates should be from 1 to 3!")
            continue
        if board[users_move[0] - 1][users_move[1] - 1] != " ":
            print("This cell is occupied! Choose another one!")
            continue
        break
    return users_move


def board_update(board, move_input):
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    if x_count == o_count:
        next_symbol = "X"
    else:
        next_symbol = "O"
    board[move_input[0] - 1][move_input[1] - 1] = next_symbol
    return board


def play_game(player_1, player_2):
    board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    moves_made = 0
    while True:
        board_print(board)
        if moves_made % 2 == 0:
            next_move = move(board, player_1, "X")
        else:
            next_move = move(board, player_2, "O")
        board = board_update(board, next_move)
        moves_made += 1
        if moves_made >= 3:
            game_state = get_state(board)
            if game_state == "Game not finished":
                continue
            else:
                board_print(board)
                print(game_state)
                break


def main():
    while True:
        command = input("Input command:").split()
        if command[0] not in ["start", "exit"]:
            print("Bad parameters!")
            continue
        if command[0] == "exit":
            quit()
        if len(command) < 3:
            print("Bad parameters!")
            continue
        if command[1] not in ["user", "easy", "medium", "hard"] or command[2] not in ["user", "easy", "medium", "hard"]:
            print("Bad parameters!")
            continue
        player_1 = command[1]
        player_2 = command[2]
        play_game(player_1, player_2)


if __name__ == '__main__':
    main()
