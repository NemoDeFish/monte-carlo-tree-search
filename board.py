from .lookup_table import lookup_table
from .adjacency_table import adjacency_table
from random import choice
from referee.game import PlaceAction, Coord
import copy


class BitBoard:
    def __init__(self):
        self.red_board = 0  # Bitboard for red
        self.blue_board = 0  # Bitboard for blue
        self.current_player = "r"  # Player whose turn it is
        self.turn_count = 1  # Turn count
        self.last_move = None  # Last move made in terms of binary number

    def clear_filled(self):
        # Define winning combinations using bitboards
        winning_combinations = [
            0b11111111111,
            0b1111111111100000000000,
            0b111111111110000000000000000000000,
            0b11111111111000000000000000000000000000000000,
            0b1111111111100000000000000000000000000000000000000000000,
            0b111111111110000000000000000000000000000000000000000000000000000000,
            0b11111111111000000000000000000000000000000000000000000000000000000000000000000,
            0b1111111111100000000000000000000000000000000000000000000000000000000000000000000000000000,
            0b111111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
            0b11111111111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
            0b1111111111100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
            0b100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000001,
            0b1000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010,
            0b10000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100,
            0b100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000,
            0b1000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000,
            0b10000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000,
            0b100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000,
            0b1000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000,
            0b10000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000,
            0b100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000000,
            0b1000000000010000000000100000000001000000000010000000000100000000001000000000010000000000100000000001000000000010000000000,
        ]

        # Check if any winning combination matches the entire board
        all_winning_row_col = 0
        for combination in winning_combinations:
            if (self.red_board | self.blue_board) & combination == combination:
                all_winning_row_col |= combination

        # Clear the filled row or column
        self.red_board &= ~all_winning_row_col
        self.blue_board &= ~all_winning_row_col

    def order_moves(self, moves):
        # Order moves based on the heuristic of limiting opponent's moves
        ordered_moves = []

        for move in moves:
            # Apply the move to a hypothetical state
            hypothetical_state = self.make_move(move)
            # Count the opponent's available moves after the hypothetical move
            num_opponent_moves = hypothetical_state.get_num_moves()

            ordered_moves.append((hypothetical_state, num_opponent_moves))

        # Sort moves based on the number of opponent moves
        ordered_moves.sort(key=lambda x: x[1])

        # Extract sorted moves
        sorted_moves = [hypothetical_state for hypothetical_state, _ in ordered_moves]
        return sorted_moves

    def get_num_moves(self):
        if self.terminal:  # If the game is finished then no moves can be made
            return 0
        # Otherwise, you can make a move in each of the empty spots
        for empty in self.generate_empty_spots(self.current_player):
            valid_moves_count = sum(
                1 for move in lookup_table[empty] if self.is_valid_move(move)
            )
        return valid_moves_count

    def find_ordered_children(self):
        if self.terminal:  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        children = set()
        for empty in self.generate_empty_spots(self.current_player):
            children.update(list(filter(self.is_valid_move, lookup_table[empty])))

        return self.order_moves(children)

    def generate_empty_spots(self, player):
        # Generate a list of binary representations of possible moves
        empty_spots = []

        player_board = self.red_board if player == "r" else self.blue_board

        # Iterate through each position on the board
        for i in range(121):
            position = 1 << i
            if not ((self.red_board | self.blue_board) & position):
                # If the bit is not set in both red and blue boards, it's an empty spot
                if player_board & adjacency_table[position]:
                    empty_spots.append(position)
        return empty_spots

    def is_valid_move(self, move):
        # Check if all moves in the list of coordinates are valid
        if (self.red_board | self.blue_board) & move:
            return False
        return True

    def display(self):
        # Display the current state of the board
        for row in range(11):
            for col in range(11):
                position = row * 11 + col
                bit = 1 << position
                if self.red_board & bit:
                    print("r", end=" ")
                elif self.blue_board & bit:
                    print("b", end=" ")
                else:
                    print("-", end=" ")
            print()

    def last_move_to_coordinates(self):
        # Convert the last move stored as a binary number into (x, y) coordinates
        if self.last_move is None:
            return None  # No last move made
        piece_coords = []
        for i in range(121):
            if self.last_move & (1 << i):
                row = i // 11
                col = i % 11
                piece_coords.append(Coord(row, col))

        return PlaceAction(*piece_coords)

    def move_binary(self, binary_position):
        # Set the bit for the player's board using the binary position
        if self.current_player == "r":
            self.red_board |= binary_position
        elif self.current_player == "b":
            self.blue_board |= binary_position

        # Switch the turn to the other player
        self.current_player = "b" if self.current_player == "r" else "r"
        self.turn_count += 1
        self.last_move = binary_position
        self.clear_filled()

    def move_coordinates(self, place_action):
        for coord in place_action.coords:
            # Calculate the position on the board based on row and column
            position = coord.r * 11 + coord.c

            # Calculate the bit to set based on the position
            bit = 1 << position

            # Set the bit for the current player's board
            if self.current_player == "r":
                self.red_board |= bit
            elif self.current_player == "b":
                self.blue_board |= bit

        # Switch the turn to the other player
        self.turn_count += 1
        self.current_player = "b" if self.current_player == "r" else "r"
        self.clear_filled()

    @property
    def terminal(self):
        if self.turn_count <= 2:
            return False
        elif self.turn_count == 150:
            return True
        elif self.current_player == "r":
            possible_moves = self.generate_empty_spots("r")
            for empty in possible_moves:
                filter_occupied = list(filter(self.is_valid_move, lookup_table[empty]))
                if (len(filter_occupied)) != 0:
                    return False
        elif self.current_player == "b":
            possible_moves = self.generate_empty_spots("b")
            for empty in possible_moves:
                filter_occupied = list(filter(self.is_valid_move, lookup_table[empty]))
                if (len(filter_occupied)) != 0:
                    return False

        return True

    def find_children(self):
        if self.terminal:  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        children = set()
        for empty in self.generate_empty_spots(self.current_player):
            children.update(list(filter(self.is_valid_move, lookup_table[empty])))

        return {self.make_move(child) for child in children}

    def find_random_child(self):
        if self.terminal:
            return None  # If the game is finished then no moves can be made
        possible_moves = []
        for empty in self.generate_empty_spots(self.current_player):
            possible_moves += list(filter(self.is_valid_move, lookup_table[empty]))

        return self.make_move(choice(possible_moves))

    def reward(self):
        if not self.terminal:
            raise RuntimeError(f"reward called on nonterminal board {self}")
        if self._find_winner is self.current_player:
            return 1
        if self._find_winner == "b" if self.current_player == "r" else "r":
            return 0  # Your opponent has just won. Bad.
        if self._find_winner is None:
            return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type {self._find_winner}")

    def _player_token_count(self, color):
        if color == "r":
            binary_num = self.red_board
        elif color == "b":
            binary_num = self.blue_board

        count = 0
        while binary_num:
            count += binary_num & 1
            binary_num >>= 1
        return count

    def is_terminal(self):
        return self.terminal

    @property
    def _find_winner(self):
        if not self.terminal:
            return None

        if self.turn_count == 150:
            # In this case the player with the most tokens wins, or if equal,
            # the game ends in a draw.
            red_count = self._player_token_count("r")
            blue_count = self._player_token_count("b")
            balance = red_count - blue_count

            if balance == 0:
                return None

            return "r" if balance > 0 else "b"

        else:
            # Current player cannot place any more pieces. Opponent wins.
            return "b" if self.current_player == "r" else "r"

    def make_move(self, move):
        # Perform the move  using binary representation
        new_bitboard = copy.deepcopy(self)
        new_bitboard.move_binary(move)
        return new_bitboard
