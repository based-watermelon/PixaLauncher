import tkinter as tk
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
root.mainloop()
