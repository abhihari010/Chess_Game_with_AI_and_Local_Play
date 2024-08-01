# main.py

import pygame
from board import Board
from chessai import ChessAI
from move import get_square_under_mouse
from utils import draw_message, board_to_fen
from pieces import King, is_checked

def display_possible_moves(win, possible_moves):
    for move in possible_moves:
        row, col = move
        pygame.draw.circle(win, (0, 255, 0), (col * 80 + 40, row * 80 + 40), 10)

def get_possible_moves(piece, pos, board):
    possible_moves = []
    for row in range(8):
        for col in range(8):
            if piece.valid_move(pos, (row, col), board.board):
                temp_piece = board.board[row][col]
                board.board[row][col] = piece
                board.board[pos[0]][pos[1]] = None

                king_pos = None
                for r in range(8):
                    for c in range(8):
                        if isinstance(board.board[r][c], King) and board.board[r][c].color == piece.color:
                            king_pos = (r, c)
                            break

                if king_pos and not is_checked(board.board, piece.color, king_pos):
                    possible_moves.append((row, col))

                board.board[pos[0]][pos[1]] = piece
                board.board[row][col] = temp_piece

    return possible_moves

def restart_game():
    return Board()

def main():
    pygame.init()
    win = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    board = Board()
    try:
        ai = ChessAI(difficulty=2)
    except Exception as e:
        print(f"Failed to initialize ChessAI: {e}")
        return

    selected_piece = None
    possible_moves = []
    run = True
    ai_color = 'b'

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                piece, pos = get_square_under_mouse(board.board)
                if piece and piece.color == board.current_turn and piece.color != ai_color:
                    selected_piece = pos
                    possible_moves = get_possible_moves(piece, pos, board)

            if event.type == pygame.MOUSEBUTTONUP:
                if selected_piece:
                    piece, new_pos = get_square_under_mouse(board.board)
                    if new_pos and new_pos != selected_piece:
                        if board.move_piece(selected_piece, new_pos, win):
                            board.draw(win)
                            selected_piece = None
                            possible_moves = []

                            if board.is_checkmate('b'):
                                draw_message(win, "Checkmate, white wins!", 3)  # Display message for 3 seconds
                                pygame.display.flip()
                                pygame.time.delay(3000)  # Wait for 3 seconds
                                board = restart_game()
                                selected_piece = None
                                possible_moves = []

        if board.current_turn == ai_color:
            board_fen = board_to_fen(board.board, board.current_turn)
            best_move = ai.get_best_move(board_fen)
            start_pos = (7 - int(best_move.from_square / 8), best_move.from_square % 8)
            end_pos = (7 - int(best_move.to_square / 8), best_move.to_square % 8)
            if board.move_piece(start_pos, end_pos, win):
                board.draw(win)

                if board.is_checkmate('w'):
                    draw_message(win, "Checkmate, black wins!", 3)  # Display message for 3 seconds
                    pygame.display.flip()
                    pygame.time.delay(3000)  # Wait for 3 seconds
                    board = restart_game()
                    selected_piece = None
                    possible_moves = []

        board.draw(win)
        if selected_piece:
            display_possible_moves(win, possible_moves)
        pygame.display.flip()
        clock.tick(60)

    ai.close()
    pygame.quit()

if __name__ == "__main__":
    main()
