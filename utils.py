#utils.py

from typing import List, Optional

import pygame

from pieces import Piece


def draw_message(win, message, duration=2):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(win.get_width() // 2, win.get_height() // 2))
    win.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(duration * 1000)


def board_to_fen(board: List[List[Optional[Piece]]], chosen_color: str) -> str:
    piece_to_fen = {
        'P': 'P', 'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K',
        'p': 'p', 'r': 'r', 'n': 'n', 'b': 'b', 'q': 'q', 'k': 'k'
    }
    fen_rows = []

    for row in board:
        empty_count = 0
        fen_row = ''
        for piece in row:
            if piece is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece_to_fen[piece.name.upper() if piece.color == 'w' else piece.name]
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    fen_board = '/'.join(fen_rows)
    active_color = 'w' if chosen_color == 'w' else 'b'
    return f"{fen_board} {active_color} - - 0 1"


