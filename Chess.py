from os import system, name
def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
class Board:
    def __init__(self):
        self.__board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        self.__turn = 0
        self.__last_double_move = None
        self.__white_king_moved = False
        self.__white_queenside_rook_moved = False
        self.__white_kingside_rook_moved = False
        self.__black_king_moved = False
        self.__black_queenside_rook_moved = False
        self.__black_kingside_rook_moved = False
        self.__under_check = False
        self.__importance_strength = {'Q': (9, 9), 'R': (5, 5), 'N': (3, 3), 'B': (3, 3), 'K': (float('inf'), 2), 'P': (1, 1), 'q': (-9, 9), 'r': (-5, 5), 'n': (-3, 3), 'b': (-3, 3), 'k': (-float('inf'), 2), 'p': (-1, 1)}
    def insufficient_material(self):
        total_material_strength = 0
        for i in range(8):
            for j in range(8):
                if self.__board[i][j].isalpha():
                    piece = self.__board[i][j]
                    if piece.lower() == 'p':
                        return False
                    total_material_strength += self.__importance_strength[piece][1]
        return total_material_strength <= 5
    def under_check(self):
        return self.__under_check
    def turn(self):
        return self.__turn
    def copy(self):
        res = Board()
        for i in range(8):
            for j in range(8):
                res.__board[i][j] = self.__board[i][j]
        res.__turn, res.__last_double_move, res.__white_king_moved = self.__turn, self.__last_double_move, self.__white_king_moved
        res.__white_queenside_rook_moved, res.__white_kingside_rook_moved, res.__black_king_moved, res.__black_queenside_rook_moved = self.__white_queenside_rook_moved, self.__white_kingside_rook_moved, self.__black_king_moved, self.__black_queenside_rook_moved
        res.__black_kingside_rook_moved, res.__under_check = self.__black_kingside_rook_moved, self.__under_check
        return res
    def move(self, square: str, dest_square: str, _promoted_piece=None):
        coordinates = (8 - int(square[1]), ord(square[0]) - 97)
        piece = self.__board[coordinates[0]][coordinates[1]]
        if piece.isupper() and self.__turn % 2 or piece.islower() and not self.__turn % 2 or square == dest_square or piece == ' ':
            raise ValueError
        dest_coord = (8 - int(dest_square[1]), ord(dest_square[0]) - 97)
        if dest_coord not in self.possible_moves(square):
            raise ValueError
        if coordinates[0] == (1, 6)[self.__turn % 2] and piece == 'Pp'[self.__turn % 2] and _promoted_piece not in list(['QRBN', 'qrbn'][self.__turn % 2]):
            raise ValueError
        if piece.lower() == 'r':
            if square == 'h1':
                self.__white_kingside_rook_moved = True
            elif square == 'a1':
                self.__white_queenside_rook_moved = True
            elif square == 'h8':
                self.__black_kingside_rook_moved = True
            elif square == 'a8':
                self.__black_queenside_rook_moved = True
        elif piece.lower() == 'k':
            if abs(coordinates[1] - dest_coord[1]) == 2:
                if self.__turn % 2:
                    if dest_coord[1] == 6:
                        self.__board[0][5], self.__board[0][7] = 'r', ' '
                    elif dest_coord[1] == 2:
                        self.__board[0][0], self.__board[0][3] = ' ', 'r'
                else:
                    if dest_coord[1] == 6:
                        self.__board[7][5], self.__board[7][7] = 'R', ' '
                    elif dest_coord[1] == 2:
                        self.__board[7][0], self.__board[7][3] = ' ', 'R'
            if self.__turn % 2:
                self.__black_king_moved = True
            else:
                self.__white_king_moved = True
        elif piece.lower() == 'p':
            if self.__turn % 2:
                if coordinates[1] == dest_coord[1] and coordinates[0] == 1 and dest_coord[0] == 3:
                    self.__last_double_move = dest_coord
            else:
                if coordinates[1] == dest_coord[1] and coordinates[0] == 6 and dest_coord[0] == 4:
                    self.__last_double_move = dest_coord
            if self.__last_double_move is not None and abs(dest_coord[0] - self.__last_double_move[0]) == 1 and dest_coord[1] == self.__last_double_move[1]:
                self.__board[coordinates[0]][dest_coord[1]] = ' '
        res = (piece, _promoted_piece)[bool(_promoted_piece)]
        self.__board[coordinates[0]][coordinates[1]], self.__board[dest_coord[0]][dest_coord[1]] = ' ', res
        if not (piece.lower() == 'p' and (coordinates[0] == 6 and dest_coord[0] == 4, coordinates[0] == 1 and dest_coord[0] == 3)[self.__turn % 2]):
            self.__last_double_move = None
        if not self.possible_position():
            self.__under_check = True
        self.__turn += 1
        nowhere_to_move = True
        for i in range(8):
            for j in range(8):
                square = chr(j + 97) + str(8 - i)
                if self.__board[i][j].islower() and self.__turn % 2 or self.__board[i][j].isupper() and not self.__turn % 2:
                    if self.possible_moves(square):
                        nowhere_to_move = False
                        break
            if not nowhere_to_move:
                break
        return nowhere_to_move
    def possible_moves(self, square: str):
        i, j = 8 - int(square[1]), ord(square[0]) - 97
        piece = self.__board[i][j]
        moves = []
        if piece == ' ':
            return moves
        if piece.islower() == self.__turn % 2:
            if piece.lower() == 'k':
                white_kingside_castling_possible, white_queenside_castling_possible, black_kingside_castling_possible, black_queenside_castling_possible = self.__board[7][4:] == ['K', ' ', ' ', 'R'], self.__board[7][:5] == ['R', ' ', ' ', ' ', 'K'], self.__board[0][4:] == ['k', ' ', ' ', 'r'], self.__board[0][:5] == ['r', ' ', ' ', ' ', 'k']
                if piece.isupper() and (white_kingside_castling_possible or white_queenside_castling_possible):
                    for I in range(8):
                        for J in range(8):
                            if self.__board[I][J] == 'k':
                                for _i in range(max(I - 1, 0), min(I + 2, 8)):
                                    for _j in range(max(J - 1, 0), min(J + 2, 8)):
                                        if (_i, _j) in [(7, 5), (7, 6)]:
                                            white_kingside_castling_possible = False
                                            if not white_queenside_castling_possible:
                                                break
                                        elif (_i, _j) in [(7, 2), (7, 3)]:
                                            white_queenside_castling_possible = False
                                            if not white_kingside_castling_possible:
                                                break
                                    if not white_kingside_castling_possible and not white_queenside_castling_possible:
                                        break
                                if not white_kingside_castling_possible and not white_queenside_castling_possible:
                                    break
                            elif self.__board[I][J] == 'n':
                                if (I, J) in [(6, 7), (5, 6), (5, 4), (6, 3), (5, 7), (5, 5), (6, 4)]:
                                    white_kingside_castling_possible = False
                                    if not white_queenside_castling_possible:
                                        break
                                if (I, J) in [(6, 5), (5, 2), (5, 4), (6, 1), (6, 4), (5, 3), (5, 1), (6, 0)]:
                                    white_queenside_castling_possible = False
                                    if not white_kingside_castling_possible:
                                        break
                            elif self.__board[I][J] == 'r':
                                if J in (2, 3, 5, 6):
                                    for _i in range(I + 1, 8):
                                        if (_i, J) in [(7, 3), (7, 2)]:
                                            white_queenside_castling_possible = False
                                            if not white_kingside_castling_possible:
                                                break
                                        elif (_i, J) in [(7, 5), (7, 6)]:
                                            white_kingside_castling_possible = False
                                            if not white_queenside_castling_possible:
                                                break
                                        if self.__board[_i][J].isalpha():
                                            break
                                    if not white_kingside_castling_possible and not white_queenside_castling_possible:
                                        break
                            elif self.__board[I][J] == 'b':
                                if I + J in (12, 13) or I - J in (2, 1) or I + J in (10, 9) or I - J in (4, 5):
                                    ii, jj = I + 1, J - 1
                                    while 0 <= ii <= 7 and 0 <= jj <= 7:
                                        if (ii, jj) in [(7, 3), (7, 2)]:
                                            white_queenside_castling_possible = False
                                            if not white_kingside_castling_possible:
                                                break
                                        elif (ii, jj) in [(7, 5), (7, 6)]:
                                            white_kingside_castling_possible = False
                                            if not white_queenside_castling_possible:
                                                break
                                        if self.__board[ii][jj].isalpha():
                                            break
                                        ii += 1
                                        jj -= 1
                                    ii, jj = I + 1, J + 1
                                    while 0 <= ii <= 7 and 0 <= jj <= 7:
                                        if (ii, jj) == (7, 3):
                                            white_queenside_castling_possible = False
                                            if not white_kingside_castling_possible:
                                                break
                                        elif (ii, jj) == (7, 5):
                                            white_kingside_castling_possible = False
                                            if not white_queenside_castling_possible:
                                                break
                                        if self.__board[ii][jj].isalpha():
                                            break
                                        ii += 1
                                        jj += 1
                            elif self.__board[I][J] == 'q':
                                if J in (3, 5):
                                    for _i in range(I + 1, 8):
                                        if (_i, J) in [(7, 3), (7, 2)]:
                                            white_queenside_castling_possible = False
                                            if not white_kingside_castling_possible:
                                                break
                                        elif (_i, J) in [(7, 5), (7, 6)]:
                                            white_kingside_castling_possible = False
                                            if not white_queenside_castling_possible:
                                                break
                                        if self.__board[_i][J].isalpha():
                                            break
                                if I + J in (12, 13) or I - J in (2, 1) or I + J in (10, 9) or I - J in (4, 5):
                                    ii, jj = I + 1, J - 1
                                    while 0 <= ii <= 7 and 0 <= jj <= 7:
                                        if (ii, jj) in [(7, 3), (7, 2)]:
                                            white_queenside_castling_possible = False
                                            if not white_kingside_castling_possible:
                                                break
                                        elif (ii, jj) in [(7, 5), (7, 6)]:
                                            white_kingside_castling_possible = False
                                            if not white_queenside_castling_possible:
                                                break
                                        if self.__board[ii][jj].isalpha():
                                            break
                                        ii += 1
                                        jj -= 1
                                    ii, jj = I + 1, J + 1
                                    while 0 <= ii <= 7 and 0 <= jj <= 7:
                                        if (ii, jj) in [(7, 3), (7, 2)]:
                                            white_queenside_castling_possible = False
                                            if not white_kingside_castling_possible:
                                                break
                                        elif (ii, jj) in [(7, 5), (7, 6)]:
                                            white_kingside_castling_possible = False
                                            if not white_queenside_castling_possible:
                                                break
                                        if self.__board[ii][jj].isalpha():
                                            break
                                        ii += 1
                                        jj += 1
                            elif self.__board[I][J] == 'p':
                                if (I + 1, J + 1) in [(7, 3), (7, 2)]:
                                    white_queenside_castling_possible = False
                                    if not white_kingside_castling_possible:
                                        break
                                elif (I + 1, J + 1) in [(7, 5), (7, 6)]:
                                    white_kingside_castling_possible = False
                                    if not white_queenside_castling_possible:
                                        break
                            if not white_kingside_castling_possible and not white_queenside_castling_possible:
                                break
                        if not white_kingside_castling_possible and not white_queenside_castling_possible:
                            break
                elif piece.islower() and (black_kingside_castling_possible or black_queenside_castling_possible):
                    for I in range(8):
                        for J in range(8):
                            if self.__board[I][J] == 'K':
                                for _i in range(max(I - 1, 0), min(I + 2, 8)):
                                    for _j in range(max(J - 1, 0), min(J + 2, 8)):
                                        if (_i, _j) in [(0, 5), (0, 6)]:
                                            black_kingside_castling_possible = False
                                            if not black_queenside_castling_possible:
                                                break
                                        elif (_i, _j) in [(0, 2), (0, 3)]:
                                            black_queenside_castling_possible = False
                                            if not black_kingside_castling_possible:
                                                break
                                    if not black_kingside_castling_possible and not black_queenside_castling_possible:
                                        break
                                if not black_kingside_castling_possible and not black_queenside_castling_possible:
                                    break
                            elif self.__board[I][J] == 'N':
                                if (I, J) in [(1, 7), (2, 6), (2, 4), (1, 3), (2, 7), (2, 5), (1, 4)]:
                                    black_kingside_castling_possible = False
                                    if not black_queenside_castling_possible:
                                        break
                                if (I, J) in [(1, 5), (2, 2), (2, 4), (1, 1), (1, 4), (2, 3), (2, 1), (1, 0)]:
                                    black_queenside_castling_possible = False
                                    if not black_kingside_castling_possible:
                                        break
                            elif self.__board[I][J] == 'R':
                                if J in (2, 3, 5, 6):
                                    for _i in range(I - 1, -1, -1):
                                        if (_i, J) in [(0, 3), (0, 2)]:
                                            black_queenside_castling_possible = False
                                            if not black_kingside_castling_possible:
                                                break
                                        elif (_i, J) in [(0, 5), (0, 6)]:
                                            black_kingside_castling_possible = False
                                            if not black_queenside_castling_possible:
                                                break
                                        if self.__board[_i][J].isalpha():
                                            break
                                    if not black_kingside_castling_possible and not black_queenside_castling_possible:
                                        break
                            elif self.__board[I][J] == 'B':
                                if I + J in (5, 6) or I - J in (2, 1) or I + J in (2, 1) or I - J in (6, 5):
                                    ii, jj = I - 1, J - 1
                                    while 0 <= ii <= 7 and 0 <= jj <= 7:
                                        if (ii, jj) in [(0, 3), (0, 2)]:
                                            black_queenside_castling_possible = False
                                            if not black_kingside_castling_possible:
                                                break
                                        elif (ii, jj) in [(0, 5), (0, 6)]:
                                            black_kingside_castling_possible = False
                                            if not black_queenside_castling_possible:
                                                break
                                        if self.__board[ii][jj].isalpha():
                                            break
                                        ii -= 1
                                        jj -= 1
                                    ii, jj = I - 1, J + 1
                                    while 0 <= ii <= 7 and 0 <= jj <= 7:
                                        if (ii, jj) == (0, 3):
                                            black_queenside_castling_possible = False
                                            if not black_kingside_castling_possible:
                                                break
                                        elif (ii, jj) == (0, 5):
                                            black_kingside_castling_possible = False
                                            if not black_queenside_castling_possible:
                                                break
                                        if self.__board[ii][jj].isalpha():
                                            break
                                        ii -= 1
                                        jj += 1
                            elif self.__board[I][J] == 'Q':
                                if J in (3, 5):
                                    for _i in range(I - 1, -1, -1):
                                        if (_i, J) in [(0, 3), (0, 2)]:
                                            black_queenside_castling_possible = False
                                            if not black_kingside_castling_possible:
                                                break
                                        elif (_i, J) in [(0, 5), (0, 6)]:
                                            black_kingside_castling_possible = False
                                            if not black_queenside_castling_possible:
                                                break
                                        if self.__board[_i][J].isalpha():
                                            break
                                if I + J in (5, 6) or I - J in (2, 1) or I + J in (2, 1) or I - J in (6, 5):
                                    ii, jj = I - 1, J - 1
                                    while 0 <= ii <= 7 and 0 <= jj <= 7:
                                        if (ii, jj) in [(0, 3), (0, 2)]:
                                            black_queenside_castling_possible = False
                                            if not black_kingside_castling_possible:
                                                break
                                        elif (ii, jj) in [(0, 5), (0, 6)]:
                                            black_kingside_castling_possible = False
                                            if not black_queenside_castling_possible:
                                                break
                                        if self.__board[ii][jj].isalpha():
                                            break
                                        ii -= 1
                                        jj -= 1
                                    ii, jj = I - 1, J + 1
                                    while 0 <= ii <= 7 and 0 <= jj <= 7:
                                        if (ii, jj) in [(0, 3), (0, 2)]:
                                            black_queenside_castling_possible = False
                                            if not black_kingside_castling_possible:
                                                break
                                        elif (ii, jj) in [(0, 5), (0, 6)]:
                                            black_kingside_castling_possible = False
                                            if not black_queenside_castling_possible:
                                                break
                                        if self.__board[ii][jj].isalpha():
                                            break
                                        ii -= 1
                                        jj += 1
                            elif self.__board[I][J] == 'P':
                                if (I - 1, J + 1) in [(0, 3), (0, 2)]:
                                    black_queenside_castling_possible = False
                                    if not black_kingside_castling_possible:
                                        break
                                elif (I - 1, J + 1) in [(0, 5), (0, 6)]:
                                    black_kingside_castling_possible = False
                                    if not black_queenside_castling_possible:
                                        break
                            if not black_kingside_castling_possible and not black_queenside_castling_possible:
                                break
                        if not black_kingside_castling_possible and not black_queenside_castling_possible:
                            break
                for _i in range(max(i - 1, 0), min(i + 2, 8)):
                    for _j in range(max(j - 1, 0), min(j + 2, 8)):
                        if self.__board[_i][_j] == ' ' or self.__board[_i][_j].isalpha() and self.__board[_i][_j].isupper() == self.__board[i][j].islower():
                            self.__board[_i][_j], self.__board[i][j], self.__turn = self.__board[i][j], self.__board[_i][_j], self.__turn + 1
                            if self.possible_position():
                                moves.append((_i, _j))
                            self.__board[_i][_j], self.__board[i][j], self.__turn = self.__board[i][j], self.__board[_i][_j], self.__turn - 1
                if not self.__under_check:
                    if piece.isupper():
                        if not self.__white_king_moved:
                            if not self.__white_kingside_rook_moved and white_kingside_castling_possible:
                                moves.append((7, 6))
                            if not self.__white_queenside_rook_moved and white_queenside_castling_possible:
                                moves.append((7, 2))
                    else:
                        if not self.__black_king_moved:
                            if not self.__black_kingside_rook_moved and black_kingside_castling_possible:
                                moves.append((0, 6))
                            if not self.__black_queenside_rook_moved and black_queenside_castling_possible:
                                moves.append((0, 2))
            elif piece.lower() == 'n':
                if i >= 1:
                    if j >= 2:
                        if self.__board[i - 1][j - 2] == ' ' or self.__board[i - 1][j - 2].isalpha() and self.__board[i - 1][j - 2].isupper() == piece.islower():
                            curr_piece = self.__board[i - 1][j - 2]
                            self.__board[i - 1][j - 2], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i - 1, j - 2))
                            self.__board[i - 1][j - 2], self.__board[i][j], self.__turn = curr_piece, self.__board[i - 1][j - 2], self.__turn - 1
                    if j <= 5:
                        if self.__board[i - 1][j + 2] == ' ' or self.__board[i - 1][j + 2].isalpha() and self.__board[i - 1][j + 2].isupper() == piece.islower():
                            curr_piece = self.__board[i - 1][j + 2]
                            self.__board[i - 1][j + 2], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i - 1, j + 2))
                            self.__board[i - 1][j + 2], self.__board[i][j], self.__turn = curr_piece, self.__board[i - 1][j + 2], self.__turn - 1
                if i >= 2:
                    if j >= 1:
                        if self.__board[i - 2][j - 1] == ' ' or self.__board[i - 2][j - 1].isalpha() and self.__board[i - 2][j - 1].isupper() == piece.islower():
                            curr_piece = self.__board[i - 2][j - 1]
                            self.__board[i - 2][j - 1], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i - 2, j - 1))
                            self.__board[i - 2][j - 1], self.__board[i][j], self.__turn = curr_piece, self.__board[i - 2][j - 1], self.__turn - 1
                    if j <= 6:
                        if self.__board[i - 2][j + 1] == ' ' or self.__board[i - 2][j + 1].isalpha() and self.__board[i - 2][j + 1].isupper() == piece.islower():
                            curr_piece = self.__board[i - 2][j + 1]
                            self.__board[i - 2][j + 1], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i - 2, j + 1))
                            self.__board[i - 2][j + 1], self.__board[i][j], self.__turn = curr_piece, self.__board[i - 2][j + 1], self.__turn - 1
                if i <= 6:
                    if j >= 2:
                        if self.__board[i + 1][j - 2] == ' ' or self.__board[i + 1][j - 2].isalpha() and self.__board[i + 1][j - 2].isupper() == piece.islower():
                            curr_piece = self.__board[i + 1][j - 2]
                            self.__board[i + 1][j - 2], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i + 1, j - 2))
                            self.__board[i + 1][j - 2], self.__board[i][j], self.__turn = curr_piece, self.__board[i + 1][j - 2], self.__turn - 1
                    if j <= 5:
                        if self.__board[i + 1][j + 2] == ' ' or self.__board[i + 1][j + 2].isalpha() and self.__board[i + 1][j + 2].isupper() == piece.islower():
                            curr_piece = self.__board[i + 1][j + 2]
                            self.__board[i + 1][j + 2], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i + 1, j + 2))
                            self.__board[i + 1][j + 2], self.__board[i][j], self.__turn = curr_piece, self.__board[i + 1][j + 2], self.__turn - 1
                if i <= 5:
                    if j >= 1:
                        if self.__board[i + 2][j - 1] == ' ' or self.__board[i + 2][j - 1].isalpha() and self.__board[i + 2][j - 1].isupper() == piece.islower():
                            curr_piece = self.__board[i + 2][j - 1]
                            self.__board[i + 2][j - 1], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i + 2, j - 1))
                            self.__board[i + 2][j - 1], self.__board[i][j], self.__turn = curr_piece, self.__board[i + 2][j - 1], self.__turn - 1
                    if j <= 6:
                        if self.__board[i + 2][j + 1] == ' ' or self.__board[i + 2][j + 1].isalpha() and self.__board[i + 2][j + 1].isupper() == piece.islower():
                            curr_piece = self.__board[i + 2][j + 1]
                            self.__board[i + 2][j + 1], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i + 2, j + 1))
                            self.__board[i + 2][j + 1], self.__board[i][j], self.__turn = curr_piece, self.__board[i + 2][j + 1], self.__turn - 1
            elif piece.lower() == 'r':
                for _i in range(i - 1, -1, -1):
                    if self.__board[_i][j].isalpha() and self.__board[_i][j].islower() == piece.islower():
                        break
                    curr_piece = self.__board[_i][j]
                    self.__board[_i][j], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                    if self.possible_position():
                        moves.append((_i, j))
                    self.__board[_i][j], self.__board[i][j], self.__turn = curr_piece, self.__board[_i][j], self.__turn - 1
                    if self.__board[_i][j].isalpha():
                        break
                for _i in range(i + 1, 8):
                    if self.__board[_i][j].isalpha() and self.__board[_i][j].islower() == piece.islower():
                        break
                    curr_piece = self.__board[_i][j]
                    self.__board[_i][j], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                    if self.possible_position():
                        moves.append((_i, j))
                    self.__board[_i][j], self.__board[i][j], self.__turn = curr_piece, self.__board[_i][j], self.__turn - 1
                    if self.__board[_i][j].isalpha():
                        break
                for _j in range(j - 1, -1, -1):
                    if self.__board[i][_j].isalpha() and self.__board[i][_j].islower() == piece.islower():
                        break
                    curr_piece = self.__board[i][_j]
                    self.__board[i][_j], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                    if self.possible_position():
                        moves.append((i, _j))
                    self.__board[i][_j], self.__board[i][j], self.__turn = curr_piece, self.__board[i][_j], self.__turn - 1
                    if self.__board[i][_j].isalpha():
                        break
                for _j in range(j + 1, 8):
                    if self.__board[i][_j].isalpha() and self.__board[i][_j].islower() == piece.islower():
                        break
                    curr_piece = self.__board[i][_j]
                    self.__board[i][_j], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                    if self.possible_position():
                        moves.append((i, _j))
                    self.__board[i][_j], self.__board[i][j], self.__turn = curr_piece, self.__board[i][_j], self.__turn - 1
                    if self.__board[i][_j].isalpha():
                        break
            elif piece.lower() == 'b':
                ii, jj = i - 1, j - 1
                while 0 <= ii <= 7 and 0 <= jj <= 7:
                    if self.__board[ii][jj].isalpha():
                        if piece.isupper() == self.__board[ii][jj].isupper():
                            break
                    taken_piece = self.__board[ii][jj]
                    self.__board[i][j], self.__board[ii][jj], self.__turn = ' ', self.__board[i][j], self.__turn + 1
                    if self.possible_position():
                        moves.append((ii, jj))
                    self.__board[i][j], self.__board[ii][jj], self.__turn = self.__board[ii][jj], taken_piece, self.__turn - 1
                    if taken_piece != ' ':
                        break
                    ii -= 1
                    jj -= 1
                ii, jj = i - 1, j + 1
                while 0 <= ii <= 7 and 0 <= jj <= 7:
                    if self.__board[ii][jj].isalpha():
                        if piece.isupper() == self.__board[ii][jj].isupper():
                            break
                    taken_piece = self.__board[ii][jj]
                    self.__board[i][j], self.__board[ii][jj], self.__turn = ' ', self.__board[i][j], self.__turn + 1
                    if self.possible_position():
                        moves.append((ii, jj))
                    self.__board[i][j], self.__board[ii][jj], self.__turn = self.__board[ii][jj], taken_piece, self.__turn - 1
                    if taken_piece != ' ':
                        break
                    ii -= 1
                    jj += 1
                ii, jj = i + 1, j - 1
                while 0 <= ii <= 7 and 0 <= jj <= 7:
                    if self.__board[ii][jj].isalpha():
                        if piece.isupper() == self.__board[ii][jj].isupper():
                            break
                    taken_piece = self.__board[ii][jj]
                    self.__board[i][j], self.__board[ii][jj], self.__turn = ' ', self.__board[i][j], self.__turn + 1
                    if self.possible_position():
                        moves.append((ii, jj))
                    self.__board[i][j], self.__board[ii][jj], self.__turn = self.__board[ii][jj], taken_piece, self.__turn - 1
                    if taken_piece != ' ':
                        break
                    ii += 1
                    jj -= 1
                ii, jj = i + 1, j + 1
                while 0 <= ii <= 7 and 0 <= jj <= 7:
                    if self.__board[ii][jj].isalpha():
                        if piece.isupper() == self.__board[ii][jj].isupper():
                            break
                    taken_piece = self.__board[ii][jj]
                    self.__board[i][j], self.__board[ii][jj], self.__turn = ' ', self.__board[i][j], self.__turn + 1
                    if self.possible_position():
                        moves.append((ii, jj))
                    self.__board[i][j], self.__board[ii][jj], self.__turn = self.__board[ii][jj], taken_piece, self.__turn - 1
                    if taken_piece != ' ':
                        break
                    ii += 1
                    jj += 1
            elif piece.lower() == 'q':
                for _i in range(i - 1, -1, -1):
                    if self.__board[_i][j].isalpha() and self.__board[_i][j].islower() == piece.islower():
                        break
                    curr_piece = self.__board[_i][j]
                    self.__board[_i][j], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                    if self.possible_position():
                        moves.append((_i, j))
                    self.__board[_i][j], self.__board[i][j], self.__turn = curr_piece, self.__board[_i][j], self.__turn - 1
                    if self.__board[_i][j].isalpha():
                        break
                for _i in range(i + 1, 8):
                    if self.__board[_i][j].isalpha() and self.__board[_i][j].islower() == piece.islower():
                        break
                    curr_piece = self.__board[_i][j]
                    self.__board[_i][j], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                    if self.possible_position():
                        moves.append((_i, j))
                    self.__board[_i][j], self.__board[i][j], self.__turn = curr_piece, self.__board[_i][j], self.__turn - 1
                    if self.__board[_i][j].isalpha():
                        break
                for _j in range(j - 1, -1, -1):
                    if self.__board[i][_j].isalpha() and self.__board[i][_j].islower() == piece.islower():
                        break
                    curr_piece = self.__board[i][_j]
                    self.__board[i][_j], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                    if self.possible_position():
                        moves.append((i, _j))
                    self.__board[i][_j], self.__board[i][j], self.__turn = curr_piece, self.__board[i][_j], self.__turn - 1
                    if self.__board[i][_j].isalpha():
                        break
                for _j in range(j + 1, 8):
                    if self.__board[i][_j].isalpha() and self.__board[i][_j].islower() == piece.islower():
                        break
                    curr_piece = self.__board[i][_j]
                    self.__board[i][_j], self.__board[i][j], self.__turn = self.__board[i][j], ' ', self.__turn + 1
                    if self.possible_position():
                        moves.append((i, _j))
                    self.__board[i][_j], self.__board[i][j], self.__turn = curr_piece, self.__board[i][_j], self.__turn - 1
                    if self.__board[i][_j].isalpha():
                        break
                ii, jj = i - 1, j - 1
                while 0 <= ii <= 7 and 0 <= jj <= 7:
                    if self.__board[ii][jj].isalpha():
                        if piece.isupper() == self.__board[ii][jj].isupper():
                            break
                    taken_piece = self.__board[ii][jj]
                    self.__board[i][j], self.__board[ii][jj], self.__turn = ' ', self.__board[i][j], self.__turn + 1
                    if self.possible_position():
                        moves.append((ii, jj))
                    self.__board[i][j], self.__board[ii][jj], self.__turn = self.__board[ii][jj], taken_piece, self.__turn - 1
                    if taken_piece != ' ':
                        break
                    ii -= 1
                    jj -= 1
                ii, jj = i - 1, j + 1
                while 0 <= ii <= 7 and 0 <= jj <= 7:
                    if self.__board[ii][jj].isalpha():
                        if piece.isupper() == self.__board[ii][jj].isupper():
                            break
                    taken_piece = self.__board[ii][jj]
                    self.__board[i][j], self.__board[ii][jj], self.__turn = ' ', self.__board[i][j], self.__turn + 1
                    if self.possible_position():
                        moves.append((ii, jj))
                    self.__board[i][j], self.__board[ii][jj], self.__turn = self.__board[ii][jj], taken_piece, self.__turn - 1
                    if taken_piece != ' ':
                        break
                    ii -= 1
                    jj += 1
                ii, jj = i + 1, j - 1
                while 0 <= ii <= 7 and 0 <= jj <= 7:
                    if self.__board[ii][jj].isalpha():
                        if piece.isupper() == self.__board[ii][jj].isupper():
                            break
                    taken_piece = self.__board[ii][jj]
                    self.__board[i][j], self.__board[ii][jj], self.__turn = ' ', self.__board[i][j], self.__turn + 1
                    if self.possible_position():
                        moves.append((ii, jj))
                    self.__board[i][j], self.__board[ii][jj], self.__turn = self.__board[ii][jj], taken_piece, self.__turn - 1
                    if taken_piece != ' ':
                        break
                    ii += 1
                    jj -= 1
                ii, jj = i + 1, j + 1
                while 0 <= ii <= 7 and 0 <= jj <= 7:
                    if self.__board[ii][jj].isalpha():
                        if piece.isupper() == self.__board[ii][jj].isupper():
                            break
                    taken_piece = self.__board[ii][jj]
                    self.__board[i][j], self.__board[ii][jj], self.__turn = ' ', self.__board[i][j], self.__turn + 1
                    if self.possible_position():
                        moves.append((ii, jj))
                    self.__board[i][j], self.__board[ii][jj], self.__turn = self.__board[ii][jj], taken_piece, self.__turn - 1
                    if taken_piece != ' ':
                        break
                    ii += 1
                    jj += 1
            elif piece.lower() == 'p':
                if piece.isupper():
                    if i == 6:
                        if self.__board[5][j] == ' ':
                            self.__board[i][j], self.__board[5][j], self.__turn = ' ', 'P', self.__turn + 1
                            if self.possible_position():
                                moves.append((5, j))
                            self.__board[i][j], self.__board[5][j], self.__turn = 'P', ' ', self.__turn - 1
                            if self.__board[4][j] == ' ':
                                self.__board[i][j], self.__board[4][j], self.__turn = ' ', 'P', self.__turn + 1
                                if self.possible_position():
                                    moves.append((4, j))
                                self.__board[i][j], self.__board[4][j], self.__turn = 'P', ' ', self.__turn - 1
                    else:
                        if self.__board[i - 1][j] == ' ':
                            self.__board[i][j], self.__board[i - 1][j], self.__turn = ' ', 'P', self.__turn + 1
                            if self.possible_position():
                                moves.append((i - 1, j))
                            self.__board[i][j], self.__board[i - 1][j], self.__turn = 'P', ' ', self.__turn - 1
                        if self.__last_double_move == (i, j - 1):
                            self.__board[i][j], self.__board[i - 1][j - 1], self.__board[i][j - 1], self.__turn = ' ', 'P', ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i - 1, j - 1))
                            self.__board[i][j], self.__board[i - 1][j - 1], self.__board[i][j - 1], self.__turn = 'P', ' ', 'p', self.__turn - 1
                        elif self.__last_double_move == (i, j + 1):
                            self.__board[i][j], self.__board[i - 1][j + 1], self.__board[i][j + 1], self.__turn = ' ', 'P', ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i - 1, j + 1))
                            self.__board[i][j], self.__board[i - 1][j + 1], self.__board[i][j + 1], self.__turn = 'P', ' ', 'p', self.__turn - 1
                    if self.__board[i - 1][j - 1].islower() and j:
                        taken_piece = self.__board[i - 1][j - 1]
                        self.__board[i][j], self.__board[i - 1][j - 1], self.__turn = ' ', 'P', self.__turn + 1
                        if self.possible_position():
                            moves.append((i - 1, j - 1))
                        self.__board[i][j], self.__board[i - 1][j - 1], self.__turn = 'P', taken_piece, self.__turn - 1
                    if self.__board[i - 1][min(j + 1, 7)].islower() and j < 7:
                        taken_piece = self.__board[i - 1][j + 1]
                        self.__board[i][j], self.__board[i - 1][j + 1], self.__turn = ' ', 'P', self.__turn + 1
                        if self.possible_position():
                            moves.append((i - 1, j + 1))
                        self.__board[i][j], self.__board[i - 1][j + 1], self.__turn = 'P', taken_piece, self.__turn - 1
                else:
                    if i == 1:
                        if self.__board[2][j] == ' ':
                            self.__board[1][j], self.__board[2][j], self.__turn = self.__board[2][j], self.__board[1][j], self.__turn + 1
                            if self.possible_position():
                                moves.append((2, j))
                            self.__board[1][j], self.__board[2][j], self.__turn = self.__board[2][j], self.__board[1][j], self.__turn - 1
                            if self.__board[3][j] == ' ':
                                self.__board[1][j], self.__board[3][j], self.__turn = self.__board[3][j], self.__board[1][j], self.__turn + 1
                                if self.possible_position():
                                    moves.append((3, j))
                                self.__board[1][j], self.__board[3][j], self.__turn = self.__board[3][j], self.__board[1][j], self.__turn - 1
                    else:
                        if self.__board[i + 1][j] == ' ':
                            self.__board[i][j], self.__board[i + 1][j], self.__turn = self.__board[i + 1][j], self.__board[i][j], self.__turn + 1
                            if self.possible_position():
                                moves.append((i + 1, j))
                            self.__board[i][j], self.__board[i + 1][j], self.__turn = self.__board[i + 1][j], self.__board[i][j], self.__turn - 1
                        if self.__last_double_move == (i, j - 1):
                            self.__board[i][j], self.__board[i + 1][j - 1], self.__board[i][j - 1], self.__turn = ' ', 'p', ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i + 1, j - 1))
                            self.__board[i][j], self.__board[i + 1][j - 1], self.__board[i][j - 1], self.__turn = 'p', ' ', 'P', self.__turn - 1
                        elif self.__last_double_move == (i, j + 1):
                            self.__board[i][j], self.__board[i + 1][j + 1], self.__board[i][j + 1], self.__turn = ' ', 'p', ' ', self.__turn + 1
                            if self.possible_position():
                                moves.append((i + 1, j + 1))
                            self.__board[i][j], self.__board[i + 1][j + 1], self.__board[i][j + 1], self.__turn = 'p', ' ', 'P', self.__turn - 1
                    if self.__board[i + 1][j - 1].isupper() and j:
                        taken_piece = self.__board[i + 1][j - 1]
                        self.__board[i][j], self.__board[i + 1][j - 1], self.__turn = ' ', 'p', self.__turn + 1
                        if self.possible_position():
                            moves.append((i + 1, j - 1))
                        self.__board[i][j], self.__board[i + 1][j - 1], self.__turn = 'p', taken_piece, self.__turn - 1
                    if self.__board[i + 1][min(j + 1, 7)].isupper() and j < 7:
                        taken_piece = self.__board[i + 1][j + 1]
                        self.__board[i][j], self.__board[i + 1][j + 1], self.__turn = ' ', 'p', self.__turn + 1
                        if self.possible_position():
                            moves.append((i + 1, j + 1))
                        self.__board[i][j], self.__board[i + 1][j + 1], self.__turn = 'p', taken_piece, self.__turn - 1
        return moves
    def possible_position(self):
        if self.__turn % 2:
            for i in range(8):
                for j in range(8):
                    if self.__board[i][j] == 'k':
                        for _i in range(max(i - 1, 0), min(i + 2, 8)):
                            for _j in range(max(j - 1, 0), min(j + 2, 8)):
                                if self.__board[_i][_j] == 'K':
                                    return False
                    elif self.__board[i][j] == 'n':
                        if i >= 1:
                            if j >= 2:
                                if self.__board[i - 1][j - 2] == 'K':
                                    return False
                            if j <= 5:
                                if self.__board[i - 1][j + 2] == 'K':
                                    return False
                        if i >= 2:
                            if j >= 1:
                                if self.__board[i - 2][j - 1] == 'K':
                                    return False
                            if j <= 6:
                                if self.__board[i - 2][j + 1] == 'K':
                                    return False
                        if i <= 5:
                            if j >= 1:
                                if self.__board[i + 2][j - 1] == 'K':
                                    return False
                            if j <= 6:
                                if self.__board[i + 2][j + 1] == 'K':
                                    return False
                        if i <= 6:
                            if j >= 2:
                                if self.__board[i + 1][j - 2] == 'K':
                                    return False
                            if j <= 5:
                                if self.__board[i + 1][j + 2] == 'K':
                                    return False
                    elif self.__board[i][j] == 'r':
                        for _i in range(i - 1, -1, -1):
                            if self.__board[_i][j] == 'K':
                                return False
                            if self.__board[_i][j].isalpha():
                                break
                        for _i in range(i + 1, 8):
                            if self.__board[_i][j] == 'K':
                                return False
                            if self.__board[_i][j].isalpha():
                                break
                        for _j in range(j - 1, -1, -1):
                            if self.__board[i][_j] == 'K':
                                return False
                            if self.__board[i][_j].isalpha():
                                break
                        for _j in range(j + 1, 8):
                            if self.__board[i][_j] == 'K':
                                return False
                            if self.__board[i][_j].isalpha():
                                break
                    elif self.__board[i][j] == 'b':
                        ii, jj = i - 1, j - 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'K':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii -= 1
                            jj -= 1
                        ii, jj = i - 1, j + 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'K':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii -= 1
                            jj += 1
                        ii, jj = i + 1, j - 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'K':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii += 1
                            jj -= 1
                        ii, jj = i + 1, j + 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'K':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii += 1
                            jj += 1
                    elif self.__board[i][j] == 'q':
                        for _i in range(i - 1, -1, -1):
                            if self.__board[_i][j] == 'K':
                                return False
                            if self.__board[_i][j].isalpha():
                                break
                        for _i in range(i + 1, 8):
                            if self.__board[_i][j] == 'K':
                                return False
                            if self.__board[_i][j].isalpha():
                                break
                        for _j in range(j - 1, -1, -1):
                            if self.__board[i][_j] == 'K':
                                return False
                            if self.__board[i][_j].isalpha():
                                break
                        for _j in range(j + 1, 8):
                            if self.__board[i][_j] == 'K':
                                return False
                            if self.__board[i][_j].isalpha():
                                break
                        ii, jj = i - 1, j - 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'K':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii -= 1
                            jj -= 1
                        ii, jj = i - 1, j + 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'K':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii -= 1
                            jj += 1
                        ii, jj = i + 1, j - 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'K':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii += 1
                            jj -= 1
                        ii, jj = i + 1, j + 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'K':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii += 1
                            jj += 1
                    elif self.__board[i][j] == 'p':
                        if self.__board[i + 1][j - 1] == 'K' and j or self.__board[i + 1][min(j + 1, 7)] == 'K' and j < 7:
                            return False
        else:
            for i in range(8):
                for j in range(8):
                    if self.__board[i][j] == 'K':
                        for _i in range(max(i - 1, 0), min(i + 2, 8)):
                            for _j in range(max(j - 1, 0), min(j + 2, 8)):
                                if self.__board[_i][_j] == 'k':
                                    return False
                    elif self.__board[i][j] == 'N':
                        if i >= 1:
                            if j >= 2:
                                if self.__board[i - 1][j - 2] == 'k':
                                    return False
                            if j <= 5:
                                if self.__board[i - 1][j + 2] == 'k':
                                    return False
                        if i >= 2:
                            if j >= 1:
                                if self.__board[i - 2][j - 1] == 'k':
                                    return False
                            if j <= 6:
                                if self.__board[i - 2][j + 1] == 'k':
                                    return False
                        if i <= 5:
                            if j >= 1:
                                if self.__board[i + 2][j - 1] == 'k':
                                    return False
                            if j <= 6:
                                if self.__board[i + 2][j + 1] == 'k':
                                    return False
                        if i <= 6:
                            if j >= 2:
                                if self.__board[i + 1][j - 2] == 'k':
                                    return False
                            if j <= 5:
                                if self.__board[i + 1][j + 2] == 'k':
                                    return False
                    elif self.__board[i][j] == 'R':
                        for _i in range(i - 1, -1, -1):
                            if self.__board[_i][j] == 'k':
                                return False
                            if self.__board[_i][j].isalpha():
                                break
                        for _i in range(i + 1, 8):
                            if self.__board[_i][j] == 'k':
                                return False
                            if self.__board[_i][j].isalpha():
                                break
                        for _j in range(j - 1, -1, -1):
                            if self.__board[i][_j] == 'k':
                                return False
                            if self.__board[i][_j].isalpha():
                                break
                        for _j in range(j + 1, 8):
                            if self.__board[i][_j] == 'k':
                                return False
                            if self.__board[i][_j].isalpha():
                                break
                    elif self.__board[i][j] == 'B':
                        ii, jj = i - 1, j - 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'k':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii -= 1
                            jj -= 1
                        ii, jj = i - 1, j + 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'k':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii -= 1
                            jj += 1
                        ii, jj = i + 1, j - 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'k':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii += 1
                            jj -= 1
                        ii, jj = i + 1, j + 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'k':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii += 1
                            jj += 1
                    elif self.__board[i][j] == 'Q':
                        for _i in range(i - 1, -1, -1):
                            if self.__board[_i][j] == 'k':
                                return False
                            if self.__board[_i][j].isalpha():
                                break
                        for _i in range(i + 1, 8):
                            if self.__board[_i][j] == 'k':
                                return False
                            if self.__board[_i][j].isalpha():
                                break
                        for _j in range(j - 1, -1, -1):
                            if self.__board[i][_j] == 'k':
                                return False
                            if self.__board[i][_j].isalpha():
                                break
                        for _j in range(j + 1, 8):
                            if self.__board[i][_j] == 'k':
                                return False
                            if self.__board[i][_j].isalpha():
                                break
                        ii, jj = i - 1, j - 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'k':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii -= 1
                            jj -= 1
                        ii, jj = i - 1, j + 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'k':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii -= 1
                            jj += 1
                        ii, jj = i + 1, j - 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'k':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii += 1
                            jj -= 1
                        ii, jj = i + 1, j + 1
                        while 0 <= ii <= 7 and 0 <= jj <= 7:
                            if self.__board[ii][jj] == 'k':
                                return False
                            if self.__board[ii][jj].isalpha():
                                break
                            ii += 1
                            jj += 1
                    elif self.__board[i][j] == 'P':
                        if self.__board[i - 1][j - 1] == 'k' and j or self.__board[i - 1][min(j + 1, 7)] == 'k' and j < 7:
                            return False
        return True
    def game_over(self):
        if self.__turn % 2:
            for i in range(8):
                for j in range(8):
                    if self.__board[i][j].islower():
                        if self.possible_moves(chr(j + 97) + str(8 - i)):
                            return False
        else:
            for i in range(8):
                for j in range(8):
                    if self.__board[i][j].isupper():
                        if self.possible_moves(chr(j + 97) + str(8 - i)):
                            return False
        return True
    def evaluate(self):
        def material_value():
            strength_value = 0
            for i in range(8):
                for j in range(8):
                    if self.__board[i][j] != ' ':
                        piece = self.__board[i][j]
                        if abs(self.__importance_strength[piece][0]) != float('inf'):
                            strength_value += self.__importance_strength[piece][0]
            return strength_value
        def pawn_structure():
            black_pawns, white_pawns = [], []
            for i in range(8):
                for j in range(8):
                    if self.__board[i][j] == 'p':
                        black_pawns.append((i, j))
                    elif self.__board[i][j] == 'P':
                        white_pawns.append((i, j))
                    if len(black_pawns) == 8 and len(white_pawns) == 8:
                        break
                if len(black_pawns) == 8 and len(white_pawns) == 8:
                    break
            black_pawns, white_pawns = list(sorted(black_pawns, key=lambda p: p[::-1])), list(sorted(white_pawns, key=lambda p: (p[1], -p[0])))
            def black():
                if not black_pawns:
                    return 0
                taken_files = []
                for _, _j in black_pawns:
                    if _j not in taken_files:
                        taken_files.append(_j)
                isles = [[black_pawns[0]]]
                _i = 0
                while _i < len(black_pawns):
                    a = black_pawns[_i][1]
                    b = isles[-1][-1]
                    while a <= 1 + b[1]:
                        isles[-1].append(black_pawns[_i])
                        _i += 1
                        if _i == len(black_pawns):
                            break
                    if _i == len(black_pawns):
                        break
                    isles.append([])
                    _i += 1
                protection = 0
                for isle in isles:
                    covered_squares = []
                    for pawn in isle:
                        if 1 <= pawn[1] <= 8:
                            covered_squares.append((pawn[0] + 1, pawn[1] - 1))
                        if -1 <= pawn[1] <= 6:
                            covered_squares.append((pawn[0] + 1, pawn[1] + 1))
                    for pawn in isle:
                        protection += covered_squares.count(pawn)
                return len(black_pawns) / 40 + 2 * (len(taken_files) / len(black_pawns)) / 5 + 3 / (20 * len(isles)) + protection / (4 * len(black_pawns))
            def white():
                if not white_pawns:
                    return 0
                taken_files = []
                for _, _j in white_pawns:
                    if _j not in taken_files:
                        taken_files.append(_j)
                isles = [[white_pawns[0]]]
                _i = 0
                while _i < len(white_pawns):
                    a = white_pawns[_i][1]
                    b = isles[-1][-1]
                    while a <= 1 + b[1]:
                        isles[-1].append(white_pawns[_i])
                        _i += 1
                        if _i == len(white_pawns):
                            break
                    if _i == len(white_pawns):
                        break
                    isles.append([])
                    _i += 1
                protection = 0
                for isle in isles:
                    covered_squares = []
                    for pawn in isle:
                        if 1 <= pawn[1] <= 8:
                            covered_squares.append((pawn[0] + 1, pawn[1] - 1))
                        if -1 <= pawn[1] <= 6:
                            covered_squares.append((pawn[0] + 1, pawn[1] + 1))
                    for pawn in isle:
                        protection += covered_squares.count(pawn)
                return len(white_pawns) / 40 + 2 * (len(taken_files) / len(white_pawns)) / 5 + 3 / (20 * len(isles)) + protection / (4 * len(white_pawns))
            return white() - black()
        def king_safety():
            return 0
        def influence_on_the_board():
            return 0
        if self.game_over():
            if self.__under_check:
                return -float('inf') * (-1) ** (self.__turn % 2)
            return 0
        res = material_value() / 5 + pawn_structure() / 4 + king_safety() / 4 + 3 * influence_on_the_board() / 10
        return res
    def __getitem__(self, item):
        if isinstance(item, str):
            return self.__board[8 - int(item[1])][ord(item[0]) - 97]
        if isinstance(item, int):
            return self.__board[item]
    def __eq__(self, other):
        if isinstance(other, Board):
            if self.__board != other.__board or self.__last_double_move != other.__last_double_move or self.__turn % 2 != other.__turn % 2:
                return False
            if self.__white_castled or other.__white_castled:
                white_side = True
            else:
                queenside_same = (self.__white_king_moved or self.__white_queenside_rook_moved) == (other.__white_king_moved or other.__white_queenside_rook_moved)
                kingside_same = (self.__white_king_moved or self.__white_kingside_rook_moved) == (other.__white_king_moved or other.__white_kingside_rook_moved)
                white_side = queenside_same and kingside_same
            if self.__black_castled or other.__black_castled:
                black_side = True
            else:
                queenside_same = (self.__black_king_moved or self.__black_queenside_rook_moved) == (other.__black_king_moved or other.__black_queenside_rook_moved)
                kingside_same = (self.__black_king_moved or self.__black_kingside_rook_moved) == (other.__black_king_moved or other.__black_kingside_rook_moved)
                black_side = queenside_same and kingside_same
            return white_side and black_side
        return False
    def __str__(self):
        res = '  a b c d e f g h\n'
        for i, row in enumerate(self.__board):
            res += f'{8 - i}|' + '|'.join(row) + f'|{8 - i}' + '\n'
        res += '  a b c d e f g h'
        return res
    def __repr__(self):
        return str(self)
if __name__ == '__main__':
    board = Board()
    while True:
        print(board)
        start_square = input().lower()
        for _i_, _j_ in board.possible_moves(start_square):
            print(chr(_j_ + 97) + str(8 - _i_))
        destination_square = input().lower()
        promoted_piece = None
        if board[start_square] == 'P' and start_square[1] == '7' or board[start_square] == 'p' and start_square[1] == '2':
            promoted_piece = input()
        try:
            if board.move(start_square, destination_square, promoted_piece):
                if board.under_check():
                    clear(), print(board, 'Mate!', sep='\n')
                    break
                else:
                    clear(), print(board, 'Draw!\nNowhere to move.', sep='\n')
                    break
            if board.insufficient_material():
                clear(), print(board, 'Draw!\nInsufficient material.', sep='\n')
        except ValueError:
            print(f'Invalid move from {start_square} to {destination_square}!')
        clear()
