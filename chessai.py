# chessai.py

import chess.engine
import os
class ChessAI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        stockfish_path = "./ChessEngine/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"

        if not os.path.exists(stockfish_path):
            raise FileNotFoundError(f"Stockfish executable not found at path: {stockfish_path}")

        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        except PermissionError as e:
            raise PermissionError(f"Permission denied when trying to open Stockfish engine at path: {stockfish_path}. "
                                  f"Please check the file permissions and try again. Original error: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while trying to open Stockfish engine: {e}")

    def get_best_move(self, board_fen):
        board = chess.Board(board_fen)
        result = self.engine.play(board, chess.engine.Limit(time=0.1 * self.difficulty))
        return result.move

    def close(self):
        self.engine.quit()
