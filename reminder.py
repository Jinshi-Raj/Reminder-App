import tkinter.ttk
from tkinter import *
from sqlite3 import *
sqliteCur = None
sqliteCon = None
reminderTree = None
def connectDB():
    global sqliteCon
    global sqliteCur 
    sqliteCon = connect("reminder.db")
    sqliteCur = sqliteCon.cursor()
    q = "CREATE TABLE IF NOT EXISTS reminder(id INTEGER primary key AUTOINCREMENT,title varchar(50),time varchar(20))"
    sqliteCur.execute(q)

  

def loadReminder():
   #for i in reminderTree.get_children():
    reminderTree.delete(*reminderTree.get_children())

    q = "SELECT * FROM reminder"
    sqliteCur.execute(q)
    rows = sqliteCur.fetchall()
    i = 1
    for r in rows :
        reminderTree.insert('',END,text=i,values=(r[1],r[2],r[0]))
        i = i + 1

def createRemider(title, time):
    q = "INSERT INTO reminder (title,time) values('{}','{}')".format(title,time)
    sqliteCur.execute(q)
    sqliteCon.commit()
    loadReminder()

def upadateRemider(title,time,id):
    q = "UPDATE reminder SET title = '{}',time = '{}' WHERE id = {}".format(title,time,id)
    sqliteCur.execute(q)
    sqliteCon.commit()
    loadReminder()

def deleteRemider():
    curItem =  reminderTree.focus()
    items = reminderTree.item(curItem)
    id = items.get('values')
    if(id == ''):
        return
    id = id[2] 
    q = "DELETE FROM reminder WHERE id = {}".format(id)
    sqliteCur.execute(q)
    sqliteCon.commit()
    loadReminder()

def fetchUpdate(Event):
    curItem =  reminderTree.focus()
    items = reminderTree.item(curItem)
    id = items.get('values')
    if(id == ''):
        return
    id = id[2]
    createWindow(id)

def createWindow(id=None):
    win = Tk()
    topLabel = Label(win,text = "Create Reminder")
    lblTitle = Label(win,text = "Title : ")
    txtTitle = Entry(win)
    
    
    lblTime = Label(win,text = "Time : ")
    txtTime = Entry(win)
    if(id == None):
        btnCreate2 = Button(win,text="Create",command=lambda :createRemider(txtTitle.get(),txtTime.get()))
    else:
        q = "SELECT * FROM reminder WHERE id = {}".format(id)
        sqliteCur.execute(q)
        rows = sqliteCur.fetchall()
        print(id)
        row = rows[0]
        txtTitle.insert(0,row[1])
        txtTime.insert(0,row[2])
        btnCreate2 = Button(win,text="Update",command=lambda :upadateRemider(txtTitle.get(),txtTime.get(),id))
    
    topLabel.grid(row=0,column=0,columnspan=3)

    lblTitle.grid(row=1,column=0)
    txtTitle.grid(row=1,column=1)

    lblTime.grid(row=2,column=0)
    txtTime.grid(row=2,column=1)

    btnCreate2.grid(row=3,column=0,columnspan=2)

def main():
    global reminderTree
    win = Tk()
    topLabel = Label(win,text = "Reminder")
    
    reminderTree = ttk.Treeview(win,columns=("title","time","id"))
    reminderTree['displaycolumns'] = ("title","time")
    reminderTree.heading('#0',text="SlNo")
    reminderTree.heading('title',text="Title")
    reminderTree.heading('time',text="Time")
    reminderTree.heading('id',text="ID")

    
    btnCreate = Button(win,text="Create",command=createWindow)
    btnUpdate = Button(win,text="Update")
    btnDelete = Button(win,text="Delete",command=deleteRemider)

    topLabel.grid(row=0,column=0,columnspan=3)
    reminderTree.grid(row=1,column=0,columnspan=3)
    

    btnCreate.grid(row=2,column=0)
    btnUpdate.grid(row=2,column=1)
    btnDelete.grid(row=2,column=2)

    btnUpdate.bind("<Button-1>",fetchUpdate)
    connectDB()
    loadReminder()
    win.mainloop()
    

main()
