from tkinter import *

window = Tk()

titleLabel = Label(window, text = "Enter your information: ", font = ("Arial", 23)).grid(row = 0, column = 0)

firstNameLabel = Label(window, text = "First Name: ", width = 30, bg = 'red').grid(row = 1, column = 0)
firstNameEntry = Entry(window).grid(row = 1, column = 1)

lastNameLabel = Label(window, text = "Last Name: ", width = 30, bg = 'green').grid(row = 2, column = 0)
lastNameEntry = Entry(window).grid(row = 2, column = 1)

emailLabel = Label(window, text = "Email: ", width = 30, bg = 'blue').grid(row = 3, column = 0)
emailEntry = Entry(window).grid(row = 3, column = 1)

submitButton = Button(window, text = "Submit").grid(row = 4, column = 0, columnspan = 3)

window.mainloop()
