# move.py

import pygame
from typing import Optional, Tuple, List
from pieces import Piece


def get_square_under_mouse(board: List[List[Optional[Piece]]]) -> Tuple[Optional[Piece], Tuple[int, int]]:
    mouse_pos = pygame.mouse.get_pos()
    col, row = mouse_pos[0] // 80, mouse_pos[1] // 80
    if 0 <= col < 8 and 0 <= row < 8:
        return board[row][col], (row, col)
    return None, (0, 0)


