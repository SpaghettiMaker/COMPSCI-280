from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import mysql.connector

#cnx = mysql.connector.connect(user='xzho684', password='f350bb3e',
                              #host='studdb-mysql.fos.auckland.ac.nz', port=3306, database='stu_xzho684_COMPSCI_280_C_S2_2017')

#cursor = cnx.cursor()

class LibrarySys:  ###IMPORTANT### Do not close toplevel screens
    def __init__(self):
        self.root = Tk()
        self.screen_size = (400, 400)
        self.style = ttk.Style()

        self.login = Login(self.screen_size, self.root, self.style)
        self.treeview = TreeView(self.root)

        # place except block when finished

        while True:
            self.start()

    def start(self):
        self.login.grid()
        self.root.mainloop()
        temp = self.login.get_state()  # if True show Librarianview if False show Userview
        print(temp)
        if temp:
            self.show_librarianview()
        else:
            pass
        return

    def show_librarianview(self):
        self.treeview.grid_tree()
        self.root.mainloop()
        return

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
        self.root.quit()

    def login(self):
        username = self.username.get()
        password = self.password.get()
        print("username is:", username, "password is:", password)
        # Admin will be True and user will be False
        self.forget()
        self.is_admin = True

    def get_state(self):
        return self.is_admin


class TreeView:
    def __init__(self, root):
        self.root = root
        self.root.title("just building")
        self.frame = ttk.Frame(self.root)

        self.tree = ttk.Treeview(self.frame, columns=("1", "2", "3", "4", "5", "6"), show=("headings"))  # show headings means that a 'label' column (tree) is hidden
        self.tree.heading("1", text="Title")
        self.tree.heading("2", text="Author")
        self.tree.heading("3", text="Genre")
        self.tree.heading("4", text="Date of Release")
        self.tree.heading("5", text="Location")
        self.tree.heading("6", text="Stock")

        self.text1 = Label(text='Enter Title:')
        self.search_entry = ttk.Entry(self.root)
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.tree.yview)
        self.logout_button = ttk.Button(self.root, text="Exit", command=lambda: self.logout())
        self.search_button = ttk.Button(self.root, text="Search", command=lambda: self.search())
        x = 0
        while x != 100:
            self.tree.insert("", "end", values=(x, 2, 3, 4, 5, 6))
            x += 1
        self.tree.config(yscrollcommand=self.scrollbar.set)  # makes the scroll bar the correct size
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        index = self.tree.selection()
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":  # if clicked on treeview heading
            self.sort_tree()
        else:
            print("you clicked on", self.tree.item(index)["values"])

    def button_click(self):
        index = self.tree.selection()
        print("you clicked on", self.tree.item(index)["values"])

    def get_selected_items(self):
        return self.tree.item(self.tree.selection())["values"]

    def grid_tree(self):
        self.text1.grid(column=0, row=0, sticky='e')
        self.search_entry.grid(column=1, row=0, columnspan=7, sticky='ew')
        self.search_button.grid(column=8, row=0, sticky='ew')
        self.frame.grid(column=0, row=1, columnspan=10, rowspan=10)
        self.logout_button.grid(column=5, row=11)
        self.scrollbar.grid(column=10, row=1, sticky='ns')  # use sticky for expanding

        self.tree.grid(column=0, row=1, sticky="nsew")

    def sort_tree(self):
        print("sorted")

    def search(self):
        print("searched")

    def logout(self):
        self.text1.grid_forget()
        self.search_entry.grid_forget()
        self.search_button.grid_forget()
        self.frame.grid_forget()
        self.logout_button.grid_forget()
        self.scrollbar.grid_forget()
        self.tree.grid_forget()
        self.root.quit()

if __name__ == "__main__":
    LibrarySys()


