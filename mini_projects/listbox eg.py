from tkinter import *

def submit():

    food = []

    for index in listbox.curselection():
        food.insert(index, listbox.get(index))
    
    print("You have ordered: ")
    #print(listbox.get(listbox.curselection()))
    for index in food:
        print(index)

def add():
    print(listbox.insert(listbox.size(), entryBox.get()))
    listbox.config(height = listbox.size())

def delete():
    for index in reversed(listbox.curselection()):
        listbox.delete(index)
    #listbox.delete(listbox.curselection())
    listbox.config(height = listbox.size())

window = Tk()

listbox = Listbox(window,
                  bg = '#548ba8',
                  font = ('Constantia', 35),
                  width = 10,
                  selectmode = MULTIPLE
                  )
listbox.pack()

listbox.insert(1,'Pizza')
listbox.insert(2,'Pasta')
listbox.insert(3,'Burger')
listbox.insert(4,'Fries')
listbox.insert(5,'Soup')

listbox.config(height = listbox.size())

entryBox = Entry(window)
entryBox.pack()

submitButton = Button(window, text = 'Submit', command = submit)
submitButton.pack()

addButton = Button(window, text = 'Add', command = add)
addButton.pack()

deleteButton = Button(window, text = 'Delete', command = delete)
deleteButton.pack()

window.mainloop()
