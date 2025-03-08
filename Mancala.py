#!/usr/bin/env python3
"""
Mancala Game (Kalah Variant)

Rules:
- The board consists of 14 positions:
  - Player 1 pits: indices 0-5; Player 1's store: index 6.
  - Player 2 pits: indices 7-12; Player 2's store: index 13.
- Each pit starts with 4 stones; the stores start with 0.
- On a turn, a player chooses one of their own pits with stones.
- The stones are removed from that pit and distributed one by one 
  in a counterclockwise direction, skipping the opponent’s store.
- If the last stone lands in the player’s own store, they get an extra turn.
- If the last stone lands in an empty pit on the player’s side, that stone and 
  any stones in the directly opposite pit are captured and moved to the player's store.
- The game ends when one player's pits are all empty. The remaining stones on the other side
  are moved to that player's store.
- The winner is the player with the most stones in their store.
"""

def init_board():
    # Board indices:
    # 0-5: Player 1 pits, 6: Player 1 store,
    # 7-12: Player 2 pits, 13: Player 2 store.
    board = [4] * 14
    board[6] = 0
    board[13] = 0
    return board

def print_board(board):
    # Display the board with player 2's pits at the top and player 1's at the bottom.
    print("\nCurrent board state:")
    # Player 2's row (reverse order for intuitive display)
    print("      ", end="")
    for i in range(12, 6, -1):
        print(f"{board[i]:2}", end="  ")
    print()
    # Stores on left and right
    print(f"P2 Store: {board[13]:2}                      P1 Store: {board[6]:2}")
    # Player 1's row
    print("      ", end="")
    for i in range(0, 6):
        print(f"{board[i]:2}", end="  ")
    print("\n")
    print("Player 2 pits indices: 12 11 10  9  8  7")
    print("Player 1 pits indices:  0  1  2  3  4  5\n")

def is_game_over(board):
    # The game ends when one player's pits are completely empty.
    if sum(board[0:6]) == 0 or sum(board[7:13]) == 0:
        return True
    return False

def make_move(board, pit, player):
    """
    Executes a move.
    Returns a tuple: (valid_move, board, extra_turn)
    - valid_move: indicates if the move was legal.
    - board: updated board state.
    - extra_turn: True if the player gets another turn.
    """
    # Validate the pit selection based on the player.
    if player == 1:
        if pit < 0 or pit > 5 or board[pit] == 0:
            return False, board, False
    else:  # player 2
        if pit < 7 or pit > 12 or board[pit] == 0:
            return False, board, False

    stones = board[pit]
    board[pit] = 0
    index = pit

    while stones > 0:
        index = (index + 1) % 14
        # Skip the opponent's store.
        if player == 1 and index == 13:
            continue
        if player == 2 and index == 6:
            continue
        board[index] += 1
        stones -= 1

    extra_turn = False
    # Grant an extra turn if the last stone lands in the player's store.
    if (player == 1 and index == 6) or (player == 2 and index == 13):
        extra_turn = True

    # Capture rule: if the last stone lands in an empty pit on the player's side.
    if player == 1 and index in range(0, 6) and board[index] == 1:
        opposite = 12 - index
        if board[opposite] > 0:
            board[6] += board[opposite] + 1
            board[index] = 0
            board[opposite] = 0
    elif player == 2 and index in range(7, 13) and board[index] == 1:
        opposite = 12 - index
        if board[opposite] > 0:
            board[13] += board[opposite] + 1
            board[index] = 0
            board[opposite] = 0

    return True, board, extra_turn

def collect_remaining_stones(board):
    # When the game ends, move all remaining stones into the corresponding store.
    board[6] += sum(board[0:6])
    board[13] += sum(board[7:13])
    for i in range(0, 6):
        board[i] = 0
    for i in range(7, 13):
        board[i] = 0
    return board

def get_winner(board):
    if board[6] > board[13]:
        return 1
    elif board[13] > board[6]:
        return 2
    else:
        return 0  # Tie

def main():
    board = init_board()
    player = 1  # Player 1 starts
    print("Welcome to Mancala!")
    print("Rules: Choose a pit index on your side that contains stones.")
    while not is_game_over(board):
        print_board(board)
        print(f"Player {player}'s turn.")
        valid_move = False
        while not valid_move:
            try:
                pit = int(input("Select a pit by its index: "))
                # Ensure the pit belongs to the current player.
                if player == 1 and (pit < 0 or pit > 5):
                    print("Invalid pit. For Player 1, choose a pit index between 0 and 5.")
                    continue
                if player == 2 and (pit < 7 or pit > 12):
                    print("Invalid pit. For Player 2, choose a pit index between 7 and 12.")
                    continue
                valid_move, board, extra_turn = make_move(board, pit, player)
                if not valid_move:
                    print("Invalid move. The pit is empty or selection is invalid. Try again.")
            except ValueError:
                print("Please enter a valid integer for the pit index.")

        if extra_turn:
            print(f"Player {player} gets an extra turn!\n")
        else:
            # Switch players.
            player = 2 if player == 1 else 1

    # Game is over: collect remaining stones and display final board.
    board = collect_remaining_stones(board)
    print_board(board)
    print("Game over!")
    winner = get_winner(board)
    if winner == 0:
        print("It's a tie!")
    else:
        print(f"Player {winner} wins!")

if __name__ == "__main__":
    main()
