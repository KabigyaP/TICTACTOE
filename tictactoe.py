

import math
import pygame

X = "X"
O = "O"
EMPTY = None

# -----------------------------
# Game Logic
# -----------------------------

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_co = sum(row.count(X) for row in board)
    o_co = sum(row.count(O) for row in board)
    if x_co > o_co:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    new_board = [row[:] for row in board]  # Create a copy of the board
    new_board[i][j] = player(board)  # Place the current player's mark
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check columns
    for col in range(3):
        if all(board[row][col] == X for row in range(3)):
            return X
        if all(board[row][col] == O for row in range(3)):
            return O
    # Check rows
    for row in range(3):
        if all(board[row][column] == X for column in range(3)):
            return X
        if all(board[row][column] == O for column in range(3)):
            return O
    # Check diagonals
    if all(board[i][i] == X for i in range(3)):
        return X
    if all(board[i][i] == O for i in range(3)):
        return O
    if all(board[i][2 - i] == X for i in range(3)):
        return X
    if all(board[i][2 - i] == O for i in range(3)):
        return O
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def minimax_value(board):
        if terminal(board):
            return utility(board)
        if player(board) == X:
            return max(minimax_value(result(board, action)) for action in actions(board))
        else:
            return min(minimax_value(result(board, action)) for action in actions(board))

    if player(board) == X:
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            value = minimax_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    else:
        best_value = math.inf
        best_action = None
        for action in actions(board):
            value = minimax_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
        return best_action

# -----------------------------
# Pygame GUI
# -----------------------------

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == O:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                          int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS,
                                   CIRCLE_WIDTH)
            elif board[row][col] == X:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

def display_winner(text):
    font = pygame.font.Font(None, 74)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (WIDTH // 4, HEIGHT // 2 - 50))

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    return initial_state()

draw_lines()
board = initial_state()
game_over = False
human_player = X   # You play as X
ai_player = O

# -----------------------------
# Main Loop
# -----------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and player(board) == human_player:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if board[mouseY][mouseX] == EMPTY:
                    board = result(board, (mouseY, mouseX))

        if not game_over and player(board) == ai_player:
            ai_move = minimax(board)
            if ai_move:
                board = result(board, ai_move)

        if terminal(board) and not game_over:
            win = winner(board)
            if win:
                display_winner(f"{win} wins!")
            else:
                display_winner("Draw!")
            game_over = True

        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board = restart()
                game_over = False

    draw_figures(board)
    pygame.display.update()

pygame.quit()
