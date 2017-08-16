from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk


class LibrarySys:  ###IMPORTANT### Do not close toplevel screens use "return" button
    def __init__(self):
        self.root = Tk()
        self.screen_size = (400, 400)
        self.login = Login(self.screen_size, self.root)
        self.login.pack()
        self.root.mainloop()
        print(self.login.getit())

        self.login2 = Login2(self.screen_size, self.root)
        self.login2.grid()
        self.root.mainloop()


class Login:
    def __init__(self, screen_size, window):
        self.screen_size = screen_size
        self.window = window
        self.window.title("Login")
        self.canvas = Canvas(self.window, width=self.screen_size[0], height=self.screen_size[1], bg='white')
        self.text = ''''''
        # dictionary for button sizes and colours when mouse hovers over
        self.font = {"Arial 25": "Arial 20", "Arial 20": "Arial 25"}
        self.colour = {"red": "blue", "blue": "red"}
        self.canvas.create_text(self.screen_size[0] // 2, self.screen_size[1] // 6,
                                text='Login', fill="blue", font=("arial", 40))
        self.state = True
        self.start()

    def start(self):
        # buttons on the screen

        self.login_button = self.canvas.create_text(self.screen_size[0]//2, self.screen_size[1] - self.screen_size[1]//5, text="Login", font=("Arial", 20), fill="blue")
        self.canvas.tag_bind(self.login_button, '<Button-1>', self.login)
        self.canvas.tag_bind(self.login_button, '<Enter>', lambda x: self.change_font(self.login_button))
        self.canvas.tag_bind(self.login_button, '<Leave>', lambda x: self.change_font(self.login_button))
        self.canvas.update()

    def change_font(self, button):  # changes the colour of the  button when mouse hovers over the button
        self.canvas.itemconfig(button, font=self.font[self.canvas.itemcget(button, "font")])
        self.canvas.itemconfig(button, fill=self.colour[self.canvas.itemcget(button, "fill")])

    def pack(self):  # packs canvas onto screen
        self.canvas.pack()

    def forget(self):  # forgets the canvas
        self.canvas.pack_forget()

    def login(self, event):

        self.forget()
        self.window.quit()
        self.state = False

    def getit(self):
        return self.state


class Login2:
    def __init__(self, screen_size, root):
        self.screen_size = screen_size
        self.root = root
        self.root.title("noi")
        self.frame = ttk.Frame(self.root, width=self.screen_size[0], height=self.screen_size[1])

        self.ok = ttk.Button(self.root, text="Okay", command=lambda: self.buttonclick())
        self.state = True

    def buttonclick(self):
        print("hi")

    def grid(self):  # packs canvas onto screen
        self.frame.grid()
        self.frame.grid(column=0, row=0, columnspan=10, rowspan=10)
        self.ok.grid(column=5, row=5)

    def forget(self):  # forgets the canvas
        self.frame.grid_forget()

    def login(self, event):
        self.forget()
        self.root.quit()
        self.state = False

    def getit(self):
        return self.state


if __name__ == "__main__":
    LibrarySys()


