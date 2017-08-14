from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk


class LibrarySys:  ###IMPORTANT### Do not close toplevel screens use "return" button
    def __init__(self):
        self.window = Tk()
        self.screen_size = (400, 400)
        #self.librarianview = LibrarianView()
        #self.userview = UserView()
        #self.console = Console(self.screen_size, self.window, self.treeview, self.userview)
        self.state = False
        self.login = Login(self.screen_size, self.window)#, self.console)


        self.login.pack()
        self.window.mainloop()

    def setstate(self, state):
        self.state = state
        print(self.state)



class Login(LibrarySys):
    def __init__(self, screen_size, window):#, console):
        #self.console = console
        self.screen_size = screen_size
        self.window = window
        self.window.title("Login")
        self.canvas = Canvas(self.window, width=self.screen_size[0], height=self.screen_size[1], bg='white')
        self.text = ''''''
        # dictionary for button sizes and colours when mouse hovers over
        self.font = {"Arial 25": "Arial 20", "Arial 20": "Arial 25"}
        self.colour = {"red": "blue", "blue": "red"}
        self.canvas.create_text(self.screen_size[0] // 2, self.screen_size[1] // 6,
                                text='Vapour Login', fill="blue", font=("arial", 40))
        self.start()

    def start(self):
        # buttons on the screen
        self.login_button = self.canvas.create_text(self.screen_size[0]//2, self.screen_size[1] - self.screen_size[1]//5, text="Login", font=("Arial", 20), fill="blue")
        self.canvas.tag_bind(self.login_button, '<Button-1>', self.login)
        self.canvas.tag_bind(self.login_button, '<Enter>', lambda x: self.change_font(self.login_button))
        self.canvas.tag_bind(self.login_button, '<Leave>', lambda x: self.change_font(self.login_button))
        self.canvas.update()

    def change_font(self, button):  # changes the colour of the button when mouse hovers over the button
        self.canvas.itemconfig(button, font=self.font[self.canvas.itemcget(button, "font")])
        self.canvas.itemconfig(button, fill=self.colour[self.canvas.itemcget(button, "fill")])

    def pack(self):  # packs canvas onto screen
        self.canvas.pack()

    def forget(self):  # forgets the canvas
        self.canvas.pack_forget()

    def login(self, event):
        self.setstate(True)
        self.forget()



__author__ = 'jerry'

LibrarySys()


