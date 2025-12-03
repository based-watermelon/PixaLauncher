import tkinter as tk
games=[
    {'id':'snake','title':'Snake','desc': 'Eat food to grow. Avoid hitting yourself or walls.'},
    {'id':'pong','title':'Pong','desc': 'Two-player paddle game. Score by passing the opponent.'},
    {'id':'tetris','title':'Tetris','desc': 'Arrange falling blocks to clear lines.'},
    {'id':'minesweeper','title':'Minesweeper','desc': 'Clear tiles and avoid hidden mines using logic.'}
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

#adding game cards to left panel
for row,game in enumerate(games):
    title_label=tk.Label(left_frame, text=game['title'], font=('Segoe UI',15),bg='#2e2e2e', fg="white")
    title_label.grid(row=row, column=0, padx=15, pady=10,sticky='w')

    details_btn=tk.Button(left_frame, text='Details',command=lambda g=game: show_details(g))
    details_btn.grid(row=row,column=1,padx=10)
#function to update right panel labels
def show_details(game):
    details_title.config(text=game['title'])
    detail_desc.config(text=game['desc'])
#adding widgets to right panel
details_title=tk.Label(right_frame,text='Select a Game', font=('Segoe UI',16), bg='#3d3d3d', fg='white' )
details_title.pack(pady=20)
detail_desc=tk.Label(right_frame,text='Game desc', font=('Segoe UI',11),bg='#3d3d3d', fg='white', wraplength=150, justify='left')
detail_desc.pack(padx=10)
root.mainloop()
