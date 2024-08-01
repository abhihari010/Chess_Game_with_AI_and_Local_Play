# board.py

import pygame
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, is_checked
from typing import List, Optional, Tuple
from utils import draw_message  # Import from the new utils module

class Board:
    def __init__(self):
        self.board: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'w'
        self.setup_board()

    def setup_board(self):
        # Setup pawns
        for i in range(8):
            self.board[1][i] = Pawn('b')
            self.board[6][i] = Pawn('w')

        # Setup rooks
        self.board[0][0] = self.board[0][7] = Rook('b')
        self.board[7][0] = self.board[7][7] = Rook('w')

        # Setup knights
        self.board[0][1] = self.board[0][6] = Knight('b')
        self.board[7][1] = self.board[7][6] = Knight('w')

        # Setup bishops
        self.board[0][2] = self.board[0][5] = Bishop('b')
        self.board[7][2] = self.board[7][5] = Bishop('w')

        # Setup queens and kings
        self.board[0][3] = Queen('b')
        self.board[0][4] = King('b')

        self.board[7][3] = Queen('w')
        self.board[7][4] = King('w')

    def draw(self, win: pygame.Surface):
        colors = [pygame.Color(235, 236, 208), pygame.Color(119, 149, 86)]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(win, color, pygame.Rect(col * 80, row * 80, 80, 80))
                piece = self.board[row][col]
                if piece:
                    win.blit(piece.image, pygame.Rect(col * 80, row * 80, 80, 80))

    def find_king(self, color: str) -> Optional[Tuple[int, int]]:
        for row_id, row in enumerate(self.board):
            for col_id, piece in enumerate(row):
                if piece and isinstance(piece, King) and piece.color == color:
                    return row_id, col_id
        return None

    def move_piece(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], win) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col]
        if piece and piece.valid_move(start_pos, end_pos, self.board):

            if isinstance(piece, King) and abs(start_col - end_col) == 2:
                if end_col == 6:
                    self.board[start_row][5] = self.board[start_row][7]  # Move rook
                    self.board[start_row][7] = None
                elif end_col == 2:
                    self.board[start_row][3] = self.board[start_row][0]  # Move rook
                    self.board[start_row][0] = None

            temp_piece = self.board[end_row][end_col]
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None

            king_pos = self.find_king(self.current_turn)
            if king_pos and is_checked(self.board, self.current_turn, king_pos):
                self.board[start_row][start_col] = piece
                self.board[end_row][end_col] = temp_piece
                draw_message(win, "King is in Check")
                return False

            piece.moved = True
            self.current_turn = 'b' if self.current_turn == 'w' else 'w'

            return True
        else:
            draw_message(win, "Invalid Move")
            return False

    def is_checkmate(self, color: str) -> bool:
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        if not is_checked(self.board, color, king_pos):
            return False


        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for r in range(8):
                        for c in range(8):
                            if piece.valid_move((row, col), (r, c), self.board):
                                temp_piece = self.board[r][c]
                                self.board[r][c] = piece
                                self.board[row][col] = None

                                new_king_pos = king_pos
                                if isinstance(piece, King):
                                    new_king_pos = (r, c)

                                if not is_checked(self.board, color, new_king_pos):
                                    self.board[row][col] = piece
                                    self.board[r][c] = temp_piece
                                    return False

                                self.board[row][col] = piece
                                self.board[r][c] = temp_piece
        return True
