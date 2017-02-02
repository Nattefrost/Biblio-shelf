import tkinter as tk
from tkinter import messagebox
import random
import time


__author__ = 'nattefrost'

class TkPlot:
    def __init__(self, data, parent):
        self.root = tk.Tk()
        self.data = data
        self.parent = parent
        random.shuffle(self.data)

        self.root.title('Biblio Stats')
        self.root.geometry("600x680")
        self.root.resizable(0,0)
        self.CAN_SIZE = (600, 450)
        self.CELLS_SIZE = 20
        self.can = tk.Canvas(self.root, bg = 'white',width=600,height=450)
        self.can.pack()
        self.draw_grid()
        self.draw_chart(self.data)
        self.root.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self.root.mainloop()

        
    def draw_grid(self):
        for i in range(30): 
            self.can.create_line(self.CELLS_SIZE * i, 0, self.CELLS_SIZE * i, 450, fill="gray") # corresponds to canvas height
            self.can.create_line(0, self.CELLS_SIZE * i, 600, self.CELLS_SIZE * i, fill="gray") # corresponds to canvas width


    def draw_chart(self, data):
        """
        The data arg must be a list of tuples or it will fail
        example : [('Apples', 5), ('Oranges', 6)]
        """
        pos_x = 0.3
        pos_ori_y = 430
        graduations = range(self.CAN_SIZE[1]//self.CELLS_SIZE)
        for it in graduations:
            grad = tk.Label(self.can, text=it, fg="black",bg='white', font= 'Verdana 10 italic')
            grad.place(x=pos_x,y=pos_ori_y)
            pos_ori_y -= 20
            
        i = 0
        position = 40
        colours = [ '#814800','dodgerblue','cyan','olivedrab','firebrick','dark green', '#E13500', '#FF284E', '#4EEC09', '#4C00B5', '#7E7E7E']
        
        while i < len(data):
            chosen_colour = random.choice(colours)
            colours.remove(chosen_colour)
            self.can.create_rectangle(position, self.CAN_SIZE[0], 
                                      position+20, self.CAN_SIZE[1]-((data[i][1]*20)+self.CELLS_SIZE//2), # Proper setup to scale on canvas/img
                                        fill=chosen_colour) 
            tk.Label(self.root, text="{} : {} ".format(data[i][0],data[i][1]),bg=chosen_colour, font="Consolas 8 bold").pack(anchor=tk.N)
            
            position+=40
            i+=1

    def ask_quit(self, event=None):
        if messagebox.askokcancel("Quit", "Quit statistics window?"):
            self.exit()

    def exit(self):
        self.parent.PLOT_WINDOW = 0
        self.root.destroy()
    


