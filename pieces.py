# pieces.py

import os
from typing import List, Optional, Tuple
import pygame


class Piece:
    def __init__(self, color: str, name: str):
        self.color = color
        self.name = name
        self.moved = False
        image_path = os.path.join("images", f"{self.color}{self.name}.png")
        self.image = pygame.transform.scale(pygame.image.load(image_path), (80, 80))

    def valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                   board: List[List[Optional['Piece']]]) -> bool:
        return False  # Default to False for base class


class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__(color, "p")

    def valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                   board: List[List[Optional['Piece']]]) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Determine the direction based on the color of the pawn
        if self.color == 'w':
            direction = -1  # White pawns move upwards
            start_row_initial = 6  # Initial row for white pawns
        else:
            direction = 1  # Black pawns move downwards
            start_row_initial = 1  # Initial row for black pawns

        # Moving straight forward
        if start_col == end_col:
            # Move one step forward
            if start_row + direction == end_row and board[end_row][end_col] is None:
                return True
            # Move two steps forward from the starting position
            if start_row == start_row_initial and start_row + 2 * direction == end_row and \
                    board[end_row][end_col] is None and board[start_row + direction][end_col] is None:
                return True

        # Moving diagonally to capture
        if (abs(start_col - end_col) == 1 and start_row + direction == end_row and board[end_row][end_col] is not None
                and board[end_row][end_col].color != self.color):
            return True

        return False


class Rook(Piece):
    def __init__(self, color: str):
        super().__init__(color, "r")

    def valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                   board: List[List[Optional['Piece']]]) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        if start_row != end_row and start_col != end_col:
            return False

        if start_row == end_row:
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False

        elif start_col == end_col:
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False

        move_spot = board[end_row][end_col]
        if move_spot is not None and move_spot.color == self.color:
            return False

        return True


class Knight(Piece):
    def __init__(self, color: str):
        super().__init__(color, "n")

    def valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                   board: List[List[Optional['Piece']]]) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # List of all possible knight moves
        knight_poss_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for row_move, col_move in knight_poss_moves:
            if (start_row + row_move == end_row) and (start_col + col_move == end_col):
                move_spot = board[end_row][end_col]
                if move_spot is None or move_spot.color != self.color:
                    return True
        return False


class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__(color, "b")

    def valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                   board: List[List[Optional['Piece']]]) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row == end_row or start_col == end_col:
            return False

        if abs(end_row - start_row) != abs(end_col - start_col):
            return False

        row_move = 1 if start_row < end_row else -1
        col_move = 1 if start_col < end_col else -1

        temp_row = start_row + row_move
        temp_col = start_col + col_move
        while temp_row != end_row and temp_col != end_col:
            if board[temp_row][temp_col] is not None:
                return False
            temp_row += row_move
            temp_col += col_move

        move_spot = board[end_row][end_col]
        if move_spot is not None and move_spot.color == self.color:
            return False

        return True


class Queen(Piece):
    def __init__(self, color: str):
        super().__init__(color, "q")

    def valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                   board: List[List[Optional['Piece']]]) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row != end_row and start_col != end_col:
            if abs(end_row - start_row) != abs(end_col - start_col):
                return False

            row_move = 1 if start_row < end_row else -1
            col_move = 1 if start_col < end_col else -1

            temp_row = start_row + row_move
            temp_col = start_col + col_move
            while temp_row != end_row and temp_col != end_col:
                if board[temp_row][temp_col] is not None:
                    return False
                temp_row += row_move
                temp_col += col_move

        if start_row == end_row:
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False

        elif start_col == end_col:
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False

        move_spot = board[end_row][end_col]
        if move_spot is not None and move_spot.color == self.color:
            return False

        return True


class King(Piece):
    def __init__(self, color: str):
        super().__init__(color, "k")

    def valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                   board: List[List[Optional['Piece']]]) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1:
            move_spot = board[end_row][end_col]
            if move_spot is None or move_spot.color != self.color:
                if not is_checked(board, self.color, (end_row, end_col)):
                    return True

        if not self.moved and start_row == end_row and abs(end_col - start_col) == 2:
            if end_col == 6:
                if isinstance(board[start_row][7], Rook) and not board[start_row][7].moved:
                    if all(board[start_row][col] is None for col in range(start_col + 1, 7)):
                        if not is_checked(board, self.color, (start_row, start_col)) and \
                                not is_checked(board, self.color, (start_row, start_col + 1)) and \
                                not is_checked(board, self.color, (start_row, start_col + 2)):
                            return True

                elif end_col == 2:
                    if isinstance(board[start_row][0], Rook) and not board[start_row][0].moved:
                        if all(board[start_row][col] is None for col in range(1, start_col)):
                            if not is_checked(board, self.color, (start_row, start_col)) and \
                                    not is_checked(board, self.color, (start_row, start_col - 1)) and \
                                    not is_checked(board, self.color, (start_row, start_col - 2)):
                                return True
        return False


def is_checked(board: List[List[Optional[Piece]]], color: str, king_pos: Tuple[int, int]) -> bool:
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color != color:
                if piece.valid_move((row, col), king_pos, board):
                    return True
    return False
