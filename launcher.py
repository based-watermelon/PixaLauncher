import tkinter as tk
import subprocess
import threading
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


games=[
    {'id':'snake','title':'Snake','desc': 'Eat food to grow. Avoid hitting yourself or walls.','path': os.path.join(BASE_DIR, 'gamelist', 'basicSnakeGame', 'main.py')},
    {'id':'pong','title':'Pong','desc': 'Two-player paddle game. Score by passing the opponent.','path': os.path.join(BASE_DIR, 'gamelist', 'Pong', 'main.py')},
    {'id':'tetris','title':'Tetris','desc': 'Arrange falling blocks to clear lines.','path': '\\gamelist\\basicSnakeGame'},
    {'id':'minesweeper','title':'Minesweeper','desc': 'Clear tiles and avoid hidden mines using logic.','path': 'PixaLauncher\\gamelist\\basicSnakeGame'}
]
#creating window
root=tk.Tk()
root.geometry("1000x600")
root.title("PixaLauncher")

#spltting window into frames
top_frame=tk.Frame(root,height=60, bg='#1f1f1f')
left_frame=tk.Frame(root, width=600, bg='#2e2e2e')
right_frame=tk.Frame(root, width=400, bg='#3d3d3d')
top_frame.pack(side='top', fill='x')
left_frame.pack(side='left', expand=True, fill='both')
right_frame.pack(side='right', fill='both')

#function to update right panel labels and buttons 
def show_details(game):
    details_title.config(text=game['title'])
    detail_desc.config(text=game['desc'])
    play_btn.config(command=lambda g=game: launch_game(g))

#game launching function using threading to open separate process
def launch_game(game):
    status_label.config(text=f"Launching {game['title']}...")
    
    def run():
        try:
            python=os.sys.executable
            subprocess.Popen([python, game['path']])
        except Exception as e:
            status_label.config(text=f'Failed: {e}')
            return
        status_label.config(text='Ready')
    threading.Thread(target=run, daemon=True).start()

#adding searchbar to topframe
search_var=tk.StringVar()
search_entry=tk.Entry(top_frame, textvariable=search_var, width=30)
search_entry.pack(side='right', padx=10,pady=10)
search_label=tk.Label(top_frame, text='Search:', font=('Segoe UI',15),bg='#1f1f1f', fg='white')
search_label.pack(side='right', padx=5)
search_entry.bind('<KeyRelease>',lambda event:refresh_gamecards())

#adding widgets to right panel
details_title=tk.Label(right_frame,text='Select a Game', font=('Segoe UI',16), bg='#3d3d3d', fg='white' )
details_title.pack(pady=20)
detail_desc=tk.Label(right_frame,text='Game desc', font=('Segoe UI',11),bg='#3d3d3d', fg='white', wraplength=150, justify='left')
detail_desc.pack(padx=10)
play_btn=tk.Button(right_frame, text="Play", font=('Segoe UI',12) )
play_btn.pack(pady=20)
status_label=tk.Label(right_frame, text='Ready', bg='#3d3d3d', fg='white')
status_label.pack(pady=10)

#function to refresh game cards according to search bar
def refresh_gamecards():
    for widget in left_frame.winfo_children():
        widget.destroy()
    s_query=search_var.get().lower()
    for row,game in enumerate(games):
        if s_query not in game['title'].lower() and s_query not in game['desc'].lower():
            continue
        title_label=tk.Label(left_frame, text=game['title'], font=('Segoe UI',15),bg='#2e2e2e', fg="white")
        title_label.grid(row=row, column=0, padx=15, pady=10,sticky='w')
        details_btn=tk.Button(left_frame, text='Details',command=lambda g=game: show_details(g))
        details_btn.grid(row=row,column=1,padx=10)
refresh_gamecards()
root.mainloop()

