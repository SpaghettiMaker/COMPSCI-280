from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector

#cnx = mysql.connector.connect(user='xzho684', password='f350bb3e',
#                              host='studdb-mysql.fos.auckland.ac.nz', port=3306, database='stu_xzho684_COMPSCI_280_C_S2_2017')
cnx = mysql.connector.connect(user='root', password='2244668800', host='127.0.0.1', port='3306', database='stu_xzho684_COMPSCI_280_C_S2_2017')
cursor = cnx.cursor()


class LibrarySys:  # ###IMPORTANT### Do not close screens with X
    """The main library system class is meant to control login screen and treeview screen"""
    def __init__(self):
        """Contains references of all frames such as login and treeview screen"""
        self.root = Tk()
        self.screen_size = (400, 400)
        self.style = ttk.Style()

        self.login = Login(self.screen_size, self.root, self.style)
        self.treeview = TreeView(self.root)

        try:
            while True:
                self.start()
        except TclError:  # can't grid because root is destroyed
            print("Exiting Program")

    def start(self):
        """start function will grid login screen to begin
        then login class will determine if user exists and if admin"""
        self.login.grid()
        self.root.title("Login (image is just a logo placeholder)")
        self.root.mainloop()  # wont finish until logged in successfully
        is_admin = self.login.get_is_admin_state()  # if True show Librarianview if False show Userview

        if is_admin:
            self.show_librarianview()
        else:
            self.show_userview()

    def show_librarianview(self):
        """grids librarianview onto screen"""
        self.root.title("Librarian Screen")
        self.treeview.grid_librarian_view()
        self.root.mainloop()

    def show_userview(self):
        """grids userview onto screen"""
        self.root.title("User Screen")
        self.treeview.grid_user_view()
        self.root.mainloop()

class Login:
    """login screen with all entries, buttons and widgets associated with logging in"""
    def __init__(self, screen_size, root, style):
        """defines attributes of widgets"""
        self.screen_size = screen_size
        self.root = root
        self.style = style
        self.style.configure("BW.Label", background="white")
        self.frame = ttk.Frame(self.root, width=self.screen_size[0], height=self.screen_size[1], style="BW.Label")

        self.login_button = ttk.Button(self.root, text="Login", command=lambda: self.login())

        self.default_username = Label(self.root, text='Enter Username:', bg='white')
        self.username = ttk.Entry(self.root)

        self.default_password = Label(self.root, text='Enter Password:', bg='white')
        self.password = ttk.Entry(self.root, show="*")
        self.is_admin = False

        self.photo = PhotoImage(file="placeholder.gif")
        self.logo = Label(image=self.photo)
        self.logo.image = self.photo  # keep a reference!

    def grid(self):  # packs frame onto screen
        """grids widgets and frame onto the root login window"""
        self.frame.grid(column=0, row=0, columnspan=10, rowspan=10)
        self.login_button.grid(column=4, row=9, columnspan=2)
        self.username.grid(column=5, row=4)
        self.default_username.grid(column=4, row=4)
        self.password.grid(column=5, row=5)
        self.default_password.grid(column=4, row=5)
        self.logo.grid(column=3, row=0, columnspan=3)

    def forget(self):  # forgets the Frame
        """grid forgets all widgets from login screen"""
        self.frame.grid_forget()
        self.login_button.grid_forget()
        self.password.grid_forget()
        self.username.grid_forget()
        self.logo.grid_forget()
        self.username.delete(0, 'end')
        self.password.delete(0, 'end')
        self.root.quit()

    def login(self):
        """function is called when login button is pressed and evaluates if user exists and valid
        ie. correct username password and then will check if user is admin"""
        username = self.username.get()
        password = self.password.get()
        # Admin will be True and user will be False
        cursor.execute("SELECT USERNAME, IS_ADMIN FROM users WHERE USERNAME = '{}' "
                       "AND PASSWORD = SHA2('{}{}', 256);".format(username, username, password))

        user_exists = False
        is_admin = False
        for (username, is_admin) in cursor:
            user_exists = True
        if user_exists:
            if is_admin:
                self.is_admin = True
            else:
                self.is_admin = False
            self.forget()
        else:
            messagebox.showinfo("Error", "Access Denied")

    def get_is_admin_state(self):
        """returns the admin state"""
        return self.is_admin


class TreeView:
    """screen for librarianview and userview and all widgets for using the library system"""
    def __init__(self, root):
        """defines attributes of widgets"""
        self.root = root
        self.frame = ttk.Frame(self.root)
        self.tree = ttk.Treeview(self.frame, columns=("1", "2", "3"), show='headings')
        self.tree.heading("1", text="Book ID")
        self.tree.heading("2", text="Title")
        self.tree.heading("3", text="Author")

        self.data_entry = DataEntry()

        self.enter_title_text = Label(text='Enter Title:')
        self.search_entry = ttk.Entry(self.root)
        self.output_box = Text(self.root, height=10, font=('helvetica', 9), state='disabled')
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.tree.yview)
        self.logout_button = ttk.Button(self.root, text="Exit", command=lambda: self.logout())
        self.search_button = ttk.Button(self.root, text="Search", command=lambda: self.search())
        self.issue_book_button = ttk.Button(self.root, text="Issue Book", command=lambda: self.issue_book())
        self.reserve_book_button = ttk.Button(self.root, text="Reserve Book", command=lambda: self.reserve_book())
        self.return_book_button = ttk.Button(self.root, text="Return Book", command=lambda: self.return_book())

        self.tree.config(yscrollcommand=self.scrollbar.set)  # makes the scroll bar the correct size
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        """will display detailed info about selected item when user has double clicked on item"""
        index = self.tree.selection()
        region = self.tree.identify("region", event.x, event.y)
        column_id = self.tree.identify_column(event.x)
        if region == "heading":  # if clicked on treeview heading
            self.sort_tree(column_id)
        else:
            print("you clicked on", self.tree.item(index)["values"])
            book_id = self.tree.item(index)["values"][0]
            print(book_id)
            self.get_output_box_data(book_id)

    def get_output_box_data(self, book_id):
        """gets the more detailed info from database and displays it in the output_box"""
        self.output_box.config(state=NORMAL)
        self.output_box.delete(1.0, END)
        cursor.execute("SELECT BOOK_ID, TITLE, AUTHOR, genre.GENRE, IBSN, PUBLISHER, status_table.STATUS_TYPE "
                       "FROM books INNER JOIN genre ON books.GENRE = genre.GENRE_ID "
                       "INNER JOIN status_table ON books.CURRENT_STATUS = status_table.STATUS_ID "
                       "WHERE BOOK_ID = {}".format(book_id))
        for BOOK_ID, TITLE, AUTHOR, GENRE, IBSN, PUBLISHER, STATUS_TYPE in cursor:
            self.output_box.insert(END, "ID: {}, {}, by {}, Genre: {}\n".format(BOOK_ID, TITLE, AUTHOR, GENRE))
            self.output_box.insert(END, "IBSN: {}\n".format(IBSN))
            self.output_box.insert(END, "Publisher: {}\n".format(PUBLISHER))
            self.output_box.insert(END, "Status: {}".format(STATUS_TYPE))
        self.output_box.config(state=DISABLED)

    def get_selected_items(self):
        """returns the current selected item ie. the one that is highlighted"""
        return self.tree.item(self.tree.selection())["values"]

    def grid_librarian_view(self):
        """grids the librarian view with ALL widgets that accesses all the functions"""
        self.get_data()
        self.issue_book_button.grid(column=2, row=12)
        self.enter_title_text.grid(column=0, row=0, sticky='e')
        self.search_entry.grid(column=1, row=0, columnspan=7, sticky='ew')
        self.search_button.grid(column=8, row=0, sticky='ew')
        self.frame.grid(column=0, row=1, columnspan=10, rowspan=10)
        self.reserve_book_button.grid(column=3, row=12)
        self.return_book_button.grid(column=4, row=12)
        self.logout_button.grid(column=5, row=12)
        self.scrollbar.grid(column=10, row=1, sticky='ns')  # use sticky for expanding
        self.output_box.grid(column=0, row=11, columnspan=9, sticky='ew')
        self.tree.grid(column=0, row=1, sticky="nsew")

    def grid_user_view(self):
        """grids SOME of the widgets so user will not be able to access all functions"""
        self.get_data()
        self.issue_book_button.grid(column=3, row=12)
        self.enter_title_text.grid(column=0, row=0, sticky='e')
        self.search_entry.grid(column=1, row=0, columnspan=7, sticky='ew')
        self.search_button.grid(column=8, row=0, sticky='ew')
        self.frame.grid(column=0, row=1, columnspan=10, rowspan=10)
        self.return_book_button.grid(column=4, row=12)
        self.logout_button.grid(column=5, row=12)
        self.scrollbar.grid(column=10, row=1, sticky='ns')  # use sticky for expanding
        self.output_box.grid(column=0, row=11, columnspan=9, sticky='ew')
        self.tree.grid(column=0, row=1, sticky="nsew")

    def sort_tree(self, column_id):
        """sorts tree by ACS on first call and then DESC if called a second time by the same column"""
        print("sorting column UNFINISHED", column_id)

    def search(self):
        """searches database by the title and id and inserts it onto the table"""
        search = self.search_entry.get()
        self.clear_tree()
        cursor.execute("SELECT BOOK_ID, TITLE, AUTHOR FROM books INNER JOIN genre ON books.GENRE = genre.GENRE_ID "
                       "INNER JOIN status_table ON books.CURRENT_STATUS = status_table.STATUS_ID "
                       "WHERE TITLE LIKE '{}%' OR BOOK_ID = '{}';".format(search, search))
        for book_id, title, author in cursor:
            self.tree.insert("", "end", values=(book_id, title, author))

    def get_data(self):
        """displays all records from database"""
        self.clear_tree()
        cursor.execute("SELECT BOOK_ID, TITLE, AUTHOR FROM books INNER JOIN genre, status_table "
                       "WHERE books.GENRE = genre.GENRE_ID AND books.CURRENT_STATUS = status_table.STATUS_ID;")
        for book_id, title, author in cursor:
            self.tree.insert("", "end", values=(book_id, title, author))

    def clear_tree(self):
        """removes all data from treeview table"""
        self.tree.delete(*self.tree.get_children())

    def issue_book(self):
        """issues book to user if available"""
        selected_book = self.get_selected_items()
        print("issuing book", selected_book, "UNFINISHED")

    def reserve_book(self):
        """reserves book to user if available"""
        selected_book = self.get_selected_items()
        print("reserving book", selected_book, "UNFINISHED")

    def return_book(self):
        """return book by IBSN"""
        self.data_entry.grid_return_book_entry()
        self.data_entry.show()
        book = self.data_entry.get_data()
        genre = self.data_entry.get_genre()
        print("returning book", book, "UNFINISHED")
        self.data_entry.clear_data_fields()

    def logout(self):
        """grid forgets all widgets from treeview screen"""
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
        self.output_box.grid_forget()
        self.root.quit()


class DataEntry:
    """responsible for collecting input data from the user as a popup window"""
    def __init__(self):
        """defines attributes of widgets"""
        self.top = Toplevel()
        self.variable = StringVar(self.top)
        self.variable.set("Select Genre")  # default value

        self.w = ttk.OptionMenu(self.top, self.variable, "", "one", "two", "three")
        self.entry_data = Entry(self.top)
        self.button = Button(self.top, text="Confirm", command=lambda: self.hide())
        self.top.withdraw()

    def show(self):
        """reveals the toplevel window"""
        self.top.deiconify()
        self.top.mainloop()

    def hide(self):
        """hides the toplevel window"""
        self.top.withdraw()
        self.top.quit()

    def get_data(self):
        """gets data from entry"""
        return self.entry_data.get()

    def get_genre(self):
        """gets data from drop down menu"""
        return self.variable.get()

    def grid_return_book_entry(self):
        """will grid relevant data entry fields for returning a book"""
        self.button.pack()
        self.entry_data.pack()
        self.w.pack()

    def clear_data_fields(self):
        """clears and resets all data entry fields"""
        self.entry_data.delete(0, 'end')
        self.variable.set("Select Genre")


if __name__ == "__main__":
    LibrarySys()


