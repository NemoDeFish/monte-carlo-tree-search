def generate_tetrimino_positions():
    tetriminos = tetriminos = [[(1, 0), (-1, 0), (0, 1), (0, -1)]]

    return tetriminos


def coordinates_to_bitboard(coordinates):
    # Initialize an empty 11x11 bitboard
    bitboard = [[0] * 11 for _ in range(11)]
    # Set the bits corresponding to the coordinates to 1
    for x, y in coordinates:
        bitboard[x][y] = 1
    # Flatten the 2D binary representation into a single binary string
    flattened_bitboard = "".join(str(bit) for row in bitboard for bit in row)
    return flattened_bitboard


def generate_board_with_tetriminos():
    binary = 1329227995784915872903807060280344576
    board = {}
    for i in range(11):
        for j in range(11):
            board[binary] = []
            for positions in generate_tetrimino_positions():
                coordinates = [((i + dx) % 11, (j + dy) % 11) for dx, dy in positions]
                bitboard_representation = coordinates_to_bitboard(coordinates)
                board[binary] = int(bitboard_representation, 2)
            binary = binary >> 1
    return board


board_with_tetriminos = generate_board_with_tetriminos()
print(board_with_tetriminos)
