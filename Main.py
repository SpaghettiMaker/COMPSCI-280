from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk


class LibrarySys:  ###IMPORTANT### Do not close toplevel screens
    def __init__(self):
        self.root = Tk()
        self.screen_size = (400, 400)
        self.style = ttk.Style()

        self.login = Login(self.screen_size, self.root, self.style)
        self.treeview = TreeView(self.root)

        try:
            while True:
                self.start()
        except:
            pass

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
        self.frame = Canvas(self.root, height=500)

        self.tree = ttk.Treeview(self.frame, columns=("1", "2", "3", "4", "5", "6"), show=("headings"))  # show headings means that a 'label' column (tree) is hidden
        self.tree.heading("1", text="Title")
        self.tree.heading("2", text="Author")
        self.tree.heading("3", text="Genre")
        self.tree.heading("4", text="Date of Release")
        self.tree.heading("5", text="Location")
        self.tree.heading("6", text="Stock")

        self.scrollbar = ttk.Scrollbar(self.frame, command=self.tree.yview)
        self.logout_button = ttk.Button(self.root, text="Exit", command=lambda: self.logout())

        self.tree.insert("", "end", values=(1, 2, 3, 4, 5, 6))
        self.tree.config(yscrollcommand=self.scrollbar.set)  # makes the scroll bar the correct size
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        index = self.tree.selection()
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":  # if clicked on treeview heading
            print("hi")
        else:
            print("you clicked on", self.tree.item(index)["values"])

    def button_click(self):
        index = self.tree.selection()
        print("you clicked on", self.tree.item(index)["values"])

    def get_selected_items(self):
        return self.tree.item(self.tree.selection())["values"]

    def grid_tree(self):
        self.frame.grid(column=0, row=0)
        self.logout_button.grid(column=5, row=10)
        self.scrollbar.grid(column=10, row=0, rowspan=10)
        # packs the scrollbar beside the treeview object. If you want to keep them together, put both in a frame

        self.tree.grid(column=0, row=0)

    def sort_tree(self):
        print("hi")

    def logout(self):
        self.frame.grid_forget()
        self.logout_button.grid_forget()
        self.scrollbar.grid_forget()
        self.tree.grid_forget()
        self.root.quit()

if __name__ == "__main__":
    LibrarySys()


