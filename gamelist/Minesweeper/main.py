import tkinter as tk
import random

#required variables
ROWS = 9
COLS = 9
MINES = 10
BG_HIDDEN = "#9ca3af"      
BG_REVEALED = "#e5e7eb"    
BG_MINE = "#dc2626"        
BG_FLAG = "#facc15"    
NUMBER_COLORS = {
    1: "#2563eb",  
    2: "#16a34a",  
    3: "#dc2626",  
    4: "#7c3aed",  
    5: "#7f1d1d",  
    6: "#0891b2",  
    7: "#000000",
    8: "#4b5563"
}



game_over = False

#main window
root = tk.Tk()
root.title("Minesweeper")
root.resizable(False, False)

# helper function: checking limits of rows and columns
def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

#setting up the board
def init_board():
    global board
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append({
                "mine": False,
                "revealed": False,
                "flagged": False,
                "count": 0
            })
        board.append(row)
#randomized mine placement 
def place_mines():
    placed = 0
    while placed < MINES:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        if not board[r][c]["mine"]:
            board[r][c]["mine"] = True
            placed += 1

#number reveal logic
def calculate_numbers():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c]["mine"]:
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if in_bounds(nr, nc) and board[nr][nc]["mine"]:
                        count += 1
            board[r][c]["count"] = count

#logic
#updating button : unrevealed to revealed
def update_button(r, c):
    cell = board[r][c]
    btn = buttons[r][c]

    if cell["revealed"]:
        btn.config(relief="sunken", state="disabled", bg=BG_REVEALED, disabledforeground='black')
        if cell["count"] > 0:
            btn.config(text=str(cell["count"]),fg=NUMBER_COLORS.get(cell['count'],'black'))
#in case of end of game
def reveal_all_mines():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c]["mine"]:
                buttons[r][c].config(text="💣", bg=BG_MINE,fg="white", relief="sunken")

def check_win():
    for r in range(ROWS):
        for c in range(COLS):
            cell = board[r][c]
            if not cell["mine"] and not cell["revealed"]:
                return False
    return True

def win_game():
    global game_over
    game_over = True
    status_label.config(text="YOU WIN 🎉")
    for r in range(ROWS):
        for c in range(COLS):
            buttons[r][c].config(state="disabled")

def reveal_cell(r, c):
    global game_over
    if game_over or not in_bounds(r, c):
        return

    cell = board[r][c]

    if cell["revealed"] or cell["flagged"]:
        return

    if cell["mine"]:
        game_over = True
        reveal_all_mines()
        status_label.config(text="GAME OVER 💥")
        return

    cell["revealed"] = True
    update_button(r, c)

    if cell["count"] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                reveal_cell(r + dr, c + dc)

    if check_win():
        win_game()

def on_cell_click(r, c):
    reveal_cell(r, c)

def on_right_click(r, c):
    global game_over
    if game_over:
        return

    cell = board[r][c]
    btn = buttons[r][c]

    if cell["revealed"]:
        return

    cell["flagged"] = not cell["flagged"]
    if cell["flagged"]:
        btn.config(text="🚩", bg=BG_FLAG)
    else:
        btn.config(text="", bg=BG_HIDDEN)


#restart function
def restart_game():
    global game_over, buttons
    game_over = False
    status_label.config(text="Playing")

    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 0:
            widget.destroy()

    init_board()
    place_mines()
    calculate_numbers()
    build_grid()

#grid GUI
def build_grid():
    global buttons
    buttons = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            btn = tk.Button(
                root,
                width=3,
                height=1,
                bg=BG_HIDDEN,
                relief='raised',
                command=lambda r=r, c=c: on_cell_click(r, c)
            )
            btn.bind("<Button-3>", lambda e, r=r, c=c: on_right_click(r, c))
            btn.grid(row=r+1, column=c)
            row.append(btn)
        buttons.append(row)

# top bar 
status_label = tk.Label(root, text="Playing", font=("Segoe UI", 12))
status_label.grid(row=0, column=0, columnspan=COLS//2, sticky="w", padx=10)

restart_btn = tk.Button(root, text="Restart", command=restart_game)
restart_btn.grid(row=0, column=COLS-2, columnspan=2)

#init
init_board()
place_mines()
calculate_numbers()
build_grid()

root.mainloop()
