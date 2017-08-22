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

        # place except block when finished and dont use destroy to close windows

        while True:
            self.start()

    def start(self):
        self.login.grid()
        self.root.title("boi image is just a placeholder")
        self.root.mainloop()
        temp = self.login.get_state()  # if True show Librarianview if False show Userview
        print(temp)
        if temp:
            self.show_librarianview()
        else:
            pass
        return

    def show_librarianview(self):
        self.root.title("just building")
        self.treeview.grid_tree()
        self.root.mainloop()
        return

class Login:
    def __init__(self, screen_size, root, style):
        self.screen_size = screen_size
        self.root = root
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

    def grid(self):  # packs frame onto screen
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
        self.frame = ttk.Frame(self.root)
        self.tree = ttk.Treeview(self.frame, columns=("1", "2", "3", "4", "5"), show=("headings"))  # show headings means that a 'label' column (tree) is hidden
        self.tree.heading("1", text="Title")
        self.tree.heading("2", text="Author")
        self.tree.heading("3", text="IBSM")
        self.tree.heading("4", text="Publisher")
        self.tree.heading("5", text="Stock")

        # create data entry
        self.data_entry = DataEntry()
        self.data_entry.hide()

        self.enter_title_text = Label(text='Enter Title:')
        self.search_entry = ttk.Entry(self.root)
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.tree.yview)
        self.logout_button = ttk.Button(self.root, text="Exit", command=lambda: self.logout())
        self.search_button = ttk.Button(self.root, text="Search", command=lambda: self.search())
        self.issue_book_button = ttk.Button(self.root, text="Issue Book", command=lambda: self.issue_book())
        self.reserve_book_button = ttk.Button(self.root, text="Reserve Book", command=lambda: self.reserve_book())
        self.return_book_button = ttk.Button(self.root, text="Return Book", command=lambda: self.return_book())
        x = 0
        #while x != 100:
        #    self.tree.insert("", "end", values=(x, 2, 3, 4, 5))
        #    x += 1
        self.tree.insert("", "end", values=("Java for dummies", "Doug Lowe", "9781119247791", "John Wiley & Sons Inc", 1))
        self.tree.config(yscrollcommand=self.scrollbar.set)  # makes the scroll bar the correct size
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        index = self.tree.selection()
        region = self.tree.identify("region", event.x, event.y)
        column_id = self.tree.identify_column(event.x)
        if region == "heading":  # if clicked on treeview heading
            self.sort_tree(column_id)
        else:
            print("you clicked on", self.tree.item(index)["values"])

    def button_click(self):
        index = self.tree.selection()
        print("you clicked on", self.tree.item(index)["values"])

    def get_selected_items(self):
        return self.tree.item(self.tree.selection())["values"]

    def grid_tree(self):
        self.issue_book_button.grid(column=2, row=11)
        self.enter_title_text.grid(column=0, row=0, sticky='e')
        self.search_entry.grid(column=1, row=0, columnspan=7, sticky='ew')
        self.search_button.grid(column=8, row=0, sticky='ew')
        self.frame.grid(column=0, row=1, columnspan=10, rowspan=10)
        self.reserve_book_button.grid(column=3, row=11)
        self.return_book_button.grid(column=4, row=11)
        self.logout_button.grid(column=5, row=11)
        self.scrollbar.grid(column=10, row=1, sticky='ns')  # use sticky for expanding

        self.tree.grid(column=0, row=1, sticky="nsew")

    def sort_tree(self, column_id):
        print("sorted column", column_id)

    def search(self):
        print("searched")

    def issue_book(self):
        self.data_entry.show()

        book = self.data_entry.get_data()
        print("issuing book", book)

    def reserve_book(self):
        selected_book = self.get_selected_items()
        print("reserving book", selected_book)

    def return_book(self):
        # call DataEntry class
        print("returning book")

    def logout(self):
        self.issue_book_button.grid_forget()
        self.reserve_book_button.grid_forget()
        self.return_book_button.grid_forget()
        self.enter_title_text.grid_forget()
        self.search_entry.grid_forget()
        self.search_button.grid_forget()
        self.frame.grid_forget()
        self.logout_button.grid_forget()
        self.scrollbar.grid_forget()
        self.tree.grid_forget()
        self.root.quit()


class DataEntry:
    def __init__(self):
        self.top = Toplevel()
        self.entry_data = Entry(self.top)
        self.entry_data.pack()
        self.button = Button(self.top, text="Confirm", command=lambda: self.hide())
        self.button.pack()

    def show(self):
        self.top.deiconify()
        self.top.mainloop()

    def hide(self):
        self.top.withdraw()
        self.top.quit()

    def get_data(self):
        return self.entry_data.get()


if __name__ == "__main__":
    LibrarySys()


