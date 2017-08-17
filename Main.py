from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk


class LibrarySys:  ###IMPORTANT### Do not close toplevel screens use "return" button
    def __init__(self):
        self.root = Tk()
        self.screen_size = (400, 400)
        self.style = ttk.Style()

        self.login = Login(self.screen_size, self.root, self.style)
        self.login.grid()
        self.root.mainloop()
        print(self.login.get_state())
        self.treeview = TreeView(self.root)
        self.treeview.pack_tree()
        self.root.mainloop()


class Login:
    def __init__(self, screen_size, root, style):
        self.screen_size = screen_size
        self.root = root
        self.root.title("boi image is just a placeholder")
        self.style = style
        self.style.configure("BW.Label", background="white")
        self.frame = ttk.Frame(self.root, width=self.screen_size[0], height=self.screen_size[1], style="BW.Label")

        self.login_button = ttk.Button(self.root, text="Login", command=lambda: self.login())

        self.default_username = StringVar(self.root, value='Enter Username')
        self.username = ttk.Entry(self.root, textvariable=self.default_username)

        self.default_password = StringVar(self.root, value='Enter Password')
        self.password = ttk.Entry(self.root, textvariable=self.default_password)

        self.is_admin = False

        self.photo = PhotoImage(file="placeholder.gif")
        self.logo = Label(image=self.photo)
        self.logo.image = self.photo  # keep a reference!

    def grid(self):  # packs canvas onto screen
        self.frame.grid(column=0, row=0, columnspan=10, rowspan=10)
        self.login_button.grid(column=5, row=9)
        self.username.grid(column=5, row=6)
        self.password.grid(column=5, row=7)
        self.logo.grid(column=5, row=0)

    def forget(self):  # forgets the Frame
        self.frame.grid_forget()
        self.login_button.grid_forget()
        self.password.grid_forget()
        self.username.grid_forget()
        self.logo.grid_forget()

    def login(self):
        username = self.username.get()
        password = self.password.get()
        print("username is:", username, "password is:", password)
        # Admin will be True and user will be False
        self.forget()
        self.root.quit()
        self.is_admin = True

    def get_state(self):
        return self.is_admin


class TreeView:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(self.root, height=500)

        self.tree = ttk.Treeview(self.frame, columns=("1", "2", "3", "4", "5", "6"), show=("headings")) # show headings means that a 'label' column (tree) is hidden
        self.tree.heading("1", text="Title")
        self.tree.heading("2", text="Genre")
        self.tree.heading("3", text="Age Restriction")
        self.tree.heading("4", text="Console")
        self.tree.heading("5", text="Price")
        self.tree.heading("6", text="Stock")

        self.tree.insert("", "end", values=(1, 2, 3, 4, 5, 6))
        self.entries = []
        self.box_text = ["Title", "Genre", "Age Restriction", "Console", "Price", "Stock"]
        for i in self.box_text:
            self.entries.append(Entry(self.frame))

        self.entry = Entry(self.frame)

    def on_double_click(self, event):
        index = self.tree.selection()
        print("you clicked on", self.tree.item(index)["values"])

    def button_click(self):
        index = self.tree.selection()
        print("you clicked on", self.tree.item(index)["values"])

    def get_selected_items(self):
        return self.tree.item(self.tree.selection())["values"]

    def pack_tree(self):
        self.frame.pack()
        scrollbar = ttk.Scrollbar(self.frame, command=self.tree.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        # packs the scrollbar beside the treeview object. If you want to keep them together, put both in a frame
        self.tree.config(yscrollcommand=scrollbar.set)  # makes the scroll bar the correct size
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(side=tk.LEFT)

if __name__ == "__main__":
    LibrarySys()


