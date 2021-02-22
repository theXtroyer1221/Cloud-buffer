from cloudBuffer.models import db, User, Post
from cloudBuffer import bcrypt
from tkinter import *
from tkinter import messagebox

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_email = Label(self, text="Email")
        self.label_password = Label(self, text="Password")

        self.entry_email = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_email.grid(row=0, sticky=E, pady=13)
        self.label_password.grid(row=1, sticky=E, pady=13)
        self.entry_email.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2, pady=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked, width=10, height=3)
        self.logbtn.grid(columnspan=2, pady=6)

        self.pack()

    def _login_btn_clicked(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            messagebox.showinfo("Login info", "Welcome John")
        else:
            messagebox.showerror("Login error", "Incorrect login details")


root = Tk()
lf = LoginFrame(root)
root.minsize(300, 250)
root.mainloop()