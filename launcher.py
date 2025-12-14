import tkinter as tk
import subprocess
import threading
import os
import pygame
pygame.mixer.init()
from PIL import Image, ImageTk
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR=os.path.join(BASE_DIR,"assets")
THUMBS_DIR=os.path.join(ASSETS_DIR, "thumbs")
AUDIO_DIR=os.path.join(ASSETS_DIR,"audio")

#initializing required variables
bg_main="#18181b"
bg_top= "#111827"
bg_right="#020617"
bg_left="#020617"
fg_text="#e5e7eb"
accent="#38bdf8"
accent_dark="#0f172a" 
font_title=("Helvetica",18, "bold")
font_label=("Segoe UI",15)
font_button=("Segoe UI",11, "bold")
click_sound=pygame.mixer.Sound(os.path.join(AUDIO_DIR,'ui_select.wav'))
click_sound2=pygame.mixer.Sound(os.path.join(AUDIO_DIR,'ui_hover.mp3'))
click_sound2.set_volume(0.5)
click_sound.set_volume(0.3)

games=[
    {'id':'snake','title':'Snake','desc': 'Eat food to grow. Avoid hitting yourself or walls.','path': os.path.join(BASE_DIR, 'gamelist', 'basicSnakeGame', 'main.py'),'thumb': os.path.join(THUMBS_DIR, 'snakelogo.png')},
    {'id':'pong','title':'Pong','desc': 'Two-player paddle game. Score by passing the opponent.','path': os.path.join(BASE_DIR, 'gamelist', 'Pong', 'main.py'),'thumb': os.path.join(THUMBS_DIR, 'ponglogo.png')},
    {'id':'tetris','title':'Tetris','desc': 'Arrange falling blocks to clear lines.','path': os.path.join(BASE_DIR, 'gamelist', 'Tetris', 'main.py'),   'thumb': os.path.join(THUMBS_DIR, 'Tetris_logo.png')},
    {'id':'minesweeper','title':'Minesweeper','desc': 'Clear tiles and avoid hidden mines using logic.','path': os.path.join(BASE_DIR, 'gamelist', 'Minesweeper', 'main.py'),'thumb': os.path.join(THUMBS_DIR, 'pngegg.png')}
]
#thumbail loading helper
thumb_cache = {}

def load_thumb(path, size=(80, 80)):
    if path in thumb_cache:
        return thumb_cache[path]
    try:
        img = Image.open(path).convert("RGBA")
        img.thumbnail(size, Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
    except Exception:
        img = Image.new("RGBA", size, (56, 189, 248, 255))
        tk_img = ImageTk.PhotoImage(img)
    thumb_cache[path] = tk_img
    return tk_img

#creating window
root=tk.Tk()
root.geometry("1000x600")
root.title("PixaLauncher")
root.configure(bg=bg_main)

#spltting window into frames
top_frame=tk.Frame(root,height=60, bg=bg_top)
left_frame=tk.Frame(root, width=600, bg=bg_left)
right_frame=tk.Frame(root, width=400, bg=bg_right)
top_frame.pack(side='top', fill='x')
left_frame.pack(side='left', expand=True, fill='both')
right_frame.pack(side='right', fill='both')

#function to update right panel labels and buttons 
def show_details(game):
    details_title.config(text=game['title'])
    detail_desc.config(text=game['desc'])
    play_btn.config(state='normal',command=lambda g=game: launch_game(g))

#game launching function using threading to open separate process
def launch_game(game):
    click_sound.play()
    status_label.config(text=f"Launching {game['title']}...")
    
    def run():
        try:
            python=os.sys.executable
            subprocess.Popen([python, game['path']])
        except Exception as e:
            status_label.config(text=f'Failed: {e}')
            return
        if not os.path.exists(game['path']):
            staticmethod.config(text="Game file not Found")
        status_label.config(text='Ready')
    threading.Thread(target=run, daemon=True).start()

#adding widgets to topframe
logo_path = os.path.join(ASSETS_DIR, 'icon.png')

logo_img = Image.open(logo_path).convert("RGBA")
logo_img.thumbnail((32, 32), Image.LANCZOS)
logo_tk = ImageTk.PhotoImage(logo_img)

logo_label = tk.Label(top_frame, image=logo_tk, bg=bg_top)
logo_label.image = logo_tk
logo_label.pack(side="left", padx=(10, 5), pady=10)


title_label=tk.Label(
    top_frame,
    text="PixaLauncher",
    font=font_title,
    bg=bg_top,
    fg=fg_text
)
title_label.pack(side="left", padx=20)
search_var=tk.StringVar()
search_entry=tk.Entry(top_frame, textvariable=search_var, width=28, font=font_label, relief='flat')
search_entry.pack(side='right', padx=20,pady=15)
search_label=tk.Label(top_frame, text='Search:', font=font_label,bg=bg_top, fg=fg_text)
search_label.pack(side='right')
search_entry.bind('<KeyRelease>',lambda event:refresh_gamecards())

#adding widgets to right panel
details_title=tk.Label(right_frame,text='Select a Game', font=('Segoe UI',16,'bold'), bg=bg_right, fg=fg_text )
details_title.pack(pady=(30,10))
detail_desc=tk.Label(right_frame,text='', font=font_label,bg=bg_right, fg='#9ca3af', wraplength=300, justify='left')
detail_desc.pack(padx=10, anchor='w')
play_btn=tk.Button(right_frame, text="Play", font=font_button, bg=accent, fg='black', activebackground="#0ea5e9", activeforeground='black',
                   relief='flat', cursor='hand2', width=12)
play_btn.pack(pady=20)
play_btn.config(state="disabled")
status_label=tk.Label(right_frame, text='Ready', bg=bg_right, fg='#9ca3af', anchor='w')
status_label.pack(pady=10, padx=20, anchor='w')

#function to refresh game cards according to search bar
def refresh_gamecards():
    for widget in left_frame.winfo_children():
        widget.destroy()
    s_query=search_var.get().lower()
    for row,game in enumerate(games):
        card=tk.Frame(left_frame, bg=accent_dark, bd=1, relief='ridge')
        card.grid(row=row, column=0, padx=15, pady=10, sticky='we', columnspan=2)
        card.grid_columnconfigure(0, weight=1)
        if s_query not in game['title'].lower() and s_query not in game['desc'].lower():
            continue
        title_label=tk.Label(card,text=game['title'], font=font_label,bg=accent_dark, fg=fg_text, anchor='w')
        title_label.grid(row=0, column=1, padx=6, pady=(8,0),sticky='w')
        details_btn=tk.Button(card,text='Details',font=font_button, bg=accent, fg="black", 
                              activebackground='#0ea5e9', activeforeground='black',
                              relief='flat', cursor='hand2',
                              command=lambda g=game: (click_sound2.play(),show_details(g)))
        details_btn.grid(row=1,column=1,padx=6, pady=(4,8),sticky='e')
        thumb=load_thumb(game.get('thumb',''))
        img_label=tk.Label(card, image=thumb, bg=accent_dark)
        img_label.image=thumb
        img_label.grid(row=0,column=0,padx=8,pady=8,rowspan=2)
        card.bind("<Enter>",lambda e,c=card: on_card_enter(c))
        card.bind("<Leave>",lambda e,c=card: on_card_leave(c))
        card.bind("<Button-1>", lambda e, g=game: show_details(g))
        title_label.bind("<Button-1>", lambda e, g=game: show_details(g))
        img_label.bind("<Button-1>", lambda e, g=game: show_details(g))
#misc ui
def on_card_enter(card):
    card.configure(bg='#1e293b')

def on_card_leave(card):
    card.configure(bg=accent_dark)

refresh_gamecards()
root.mainloop()
