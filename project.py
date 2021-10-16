from tkinter import *
from tkinter import messagebox        # Open error windows
import tkinter.filedialog as dialog   # Save notes
from tkcalendar import *              # Calendar to pick date of birth
import re                             # Check valid/unvalid email type
import time                           # Clock
import sqlite3                        # Create sqlite3 database
import os                             # Check to see if Database has been created



def mainWindow():
    global root
    global generalFont, bgColorMain, bgColorSecond, textColor, btnColor

    # Set general styling stuff
    generalFont = ("Calibri", 12)
    bgColorMain = "#447294"
    bgColorSecond = "#8FBCDB"
    textColor = "#153450"
    btnColor = "#B0C4DE"

    root = Tk()
    cwd = os.getcwd()
    root.iconbitmap(cwd + "\icon.ico")
    width = 350
    height = 130
    root.title("Login/Register")
    root.resizable(width=False, height=False)
    root.config(background=bgColorMain)
    
    # Get my screen dimensions
    global myScreenHeight, myScreenWidth
    myScreenWidth = root.winfo_screenwidth()
    myScreenHeight = root.winfo_screenheight()
    # Calculate x and y coordinates for the root window
    x = (myScreenWidth/2) - (width/2)
    y = (myScreenHeight/2) - ((height + 500)/2)  # +500 since our window will expand when registration is being done
    # Set the dimensions of the screen and where it is placed
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    
    global userLogin, passLogin, registerEntry1, userEntry1, passwordEntry1, registerLF    
    userLogin = StringVar()
    passLogin = StringVar()    

    # Create Widgets         
    usernameLabel = Label(text="Username:", background=bgColorMain, fg=textColor, font=generalFont)
    userEntry1 = Entry(textvariable=userLogin)
    passwordLabel = Label(text="Password:", background=bgColorMain, fg=textColor, font=generalFont)
    passwordEntry1 = Entry(textvariable=passLogin, show="*")
    btnLogin = Button(text="Login", command=loginVerify, bd=3, bg=btnColor, fg=textColor, activebackground="#994C00", font=generalFont, border=3)
    btnRegisterNow = Button(text="Register Now", command=register, bd=3, bg=btnColor, fg=textColor, activebackground="#994C00", font=generalFont, border=3)

    # Place widgets 
    usernameLabel.grid(row=0, column=1, padx=15, pady=15)
    userEntry1.grid(row=0, column=2)
    passwordLabel.grid(row=1, column=1, padx=15)
    passwordEntry1.grid(row=1, column=2)
    btnLogin.place(x=270, y=25, width=50, height=50)    
    btnRegisterNow.grid(row=3, column=2, pady=10)
    
    # Register LabelFrame
    registerLF = LabelFrame(text="Enter your information", width=310, height=400, background=bgColorSecond, fg=textColor, font=("Calibri", 15))
    registerLF.place(x=20, y=140)      

    root.mainloop()

def register():
    global genderReg, userReg, passReg, countryReg, emailReg, ageReg, regUserEntry, regPassEntry, regEmailEntry, regAgeEntry, regCountryEntry
    
    # Expand root when button 'Register Now' is clicked       
    root.geometry("350x570")
    
    userReg = StringVar()
    passReg = StringVar()
    countryReg = StringVar()
    emailReg = StringVar()
    ageReg = StringVar()
    genderReg = IntVar()
    
    # USERNAME
    regLabel = Label(registerLF, text="Username:", background=bgColorSecond, fg=textColor, font=generalFont)
    regLabel.place(x=10, y=10)    
    regUserEntry = Entry(registerLF, textvariable=userReg, width=45)
    regUserEntry.place(x=15, y=40)
    
    # PASSWORD
    passLabel = Label(registerLF, text="Password:", background=bgColorSecond, fg=textColor, font=generalFont)
    passLabel.place(x=10, y=70)
    regPassEntry = Entry(registerLF, textvariable=passReg, show="*", width=45)
    regPassEntry.place(x=15, y=100)

    # EMAIL
    emailLabel = Label(registerLF, text="Email:", background=bgColorSecond, fg=textColor, font=generalFont)
    emailLabel.place(x=10, y=130)
    regEmailEntry = Entry(registerLF, textvariable=emailReg, width=45)
    regEmailEntry.place(x=15, y=160)

    # COUNTRY
    countryLabel = Label(registerLF, text="Country:", background=bgColorSecond, fg=textColor, font=generalFont)
    countryLabel.place(x=10, y=190)
    regCountryEntry = Entry(registerLF, textvariable=countryReg, width=45)
    regCountryEntry.place(x=15, y=220)

    # DATE OF BIRTH    
    ageBtn = Button(registerLF, text="Click to pick your Date of Birth", command=dateEntryView,
                    bg=bgColorSecond, fg=textColor, font=generalFont, border=2)
    ageBtn.place(x=10, y=260) 

    # MALE/FEMALE 
    radioMale = Radiobutton(registerLF, text="M", variable=genderReg, value=0, background=bgColorSecond, fg=textColor, font=generalFont,
    selectcolor="white")
    radioMale.place(x=10, y=310)
    radioFemale = Radiobutton(registerLF, text="F", variable=genderReg, value=1, background=bgColorSecond, fg=textColor, font=generalFont, 
    selectcolor="white")
    radioFemale.place(x=50, y=310)

    # FINALIZE 'DONE' BUTTON
    btnRegister = Button(text="Create Account", command=checkForInputErrors, bg=btnColor,fg=textColor, activebackground="#994C00", font=generalFont)
    btnRegister.place(x=210, y=500, width=110, height=30)

def dateEntryView():
    global screenDate
    screenDate = Toplevel(root)
    screenDate.geometry("100x100+1150+625")    # Place date picker closer to the root window when it appears on screen

    def pickDate(i):       # Create calendar to pick Date of Birth
        global dateStr
        datetime = cal.get_date()
        dateStr = str(datetime)
    
    datePattern = "d/m/y"
    Label(screenDate, text="Choose Date").pack()
    cal = DateEntry(screenDate, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern=datePattern)
    cal.pack(padx=10, pady=10)
    cal.bind("<<DateEntrySelected>>", pickDate)
    exitBtn = Button(screenDate, text="Exit", command=screenDate.destroy)
    exitBtn.pack()

def checkForInputErrors():
    global registerUserrr, registerPass, registerEmail, registerCountry, registerGender
    global userInfo
    # Get the information each user typed in, in the register 'form'
    registerUserrr = userReg.get()
    registerPass = passReg.get()
    registerEmail = emailReg.get()
    registerCountry = countryReg.get()
    registerGender = genderReg.get()
   
    # Give the values (0 or 1) of the radiobutton a 'string value' so I can use it 
    if registerGender == 0:
        registerGender = "Male"
    else:
        registerGender = "Female"

    # Check if username and email entered by user are valid:
    symbols = ["#", "%", "&", "/", "\\", "?", "`", "~", "!", "@", "$", "^", "*", "(", ")", "-", "+", "=", "_",
    "[", "]", "{", "}", "|", ":", ";", ".", ",", "<", ">"]

    for i in symbols:
        symbol = i

    # Stackoverflow valid email address regular expression 
    emailValidRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'    
    # Variable filesList is to see if the Database has alredy been created or if its the first user registering
    filesList = os.listdir()
    # Select error messages based on what the user failed to type in properly!
    if len(registerUserrr) == 0 or len(registerUserrr) > 15 or registerUserrr[0].isdigit() or registerUserrr.startswith(symbol):
        messagebox.showinfo("Error", "Username must follow these rules:\n\n --Start with a letter (a-z, A-Z)\n--Contain NO symbols\n--Less than 15 characters long\n\nTry Again!")
    elif not (re.fullmatch(emailValidRegex, str(registerEmail))):
        messagebox.showinfo("Error", "Enter valid Email!")
    elif len(registerPass) < 5:
        messagebox.showinfo("Error", "Password must be at least 5 characters long!")
    elif len(registerCountry) == 0:
        messagebox.showinfo("Error", "Must enter a valid Country!")
    else:
        if "usersInfo.sqlite" in filesList:
            checkEmailUsername()
        else:
            registerUser()                          

def checkEmailUsername():
    conn = sqlite3.connect("usersInfo.sqlite")
    cur = conn.cursor() 
    cur.execute('''SELECT name, email FROM Users''')
    allUsersTupleList = cur.fetchall()
    conn.commit()

    # Get usernames and emails from Database so I can verify if the user's chosen username and email are alredy in the Database   
    # Only get the name and email if the Database has alredy been created. 
    allUsersList = []
    allEmailsList = []
    for item in allUsersTupleList:
        allUsersList.append(item[0])
        allEmailsList.append(item[1])

    # Check if chosen username and emails are alredy in use
    if registerUserrr in allUsersList:
        messagebox.showinfo("Error", "Username alredy in use!\nPlease choose another one.")
    elif registerEmail in allEmailsList:
        messagebox.showinfo("Error", "Email alredy in use!\nPlease choose another one.")
    else:
        registerUser()                           


def registerUser():    
    # I apologise for this function's name. Does not make much sense.
    # Check to see if Database has alredy been created
    filesList = os.listdir()
    if "usersInfo.sqlite" in filesList:
        updateDB()
        print("Database has been updated!")
    else:
        createDB()   # Call createDB() ONLY after the first user is registered. After that I just update it
        print("Database has been created!")
    
    regUserEntry.delete(0, END)
    regPassEntry.delete(0, END)
    regEmailEntry.delete(0, END)
    regCountryEntry.delete(0, END)

def createDB():
    conn = sqlite3.connect("usersInfo.sqlite")
    cur = conn.cursor()

    # Create Database 
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        countryID  INTEGER, 
        genderID   INTEGER,
        dateID     INTEGER,
        name       TEXT UNIQUE,
        password   TEXT,
        email      TEXT UNIQUE
    );''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Countries (
        id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        country    TEXT      
    );''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Dates (
        id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        birthDate    TEXT       
    )''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Gender (
        id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        gender    TEXT 
    );''')

    conn.commit()
    updateDB()

def updateDB():
    conn = sqlite3.connect("usersInfo.sqlite")
    cur = conn.cursor()  

    # Use .title() on countries
    registerCountryCapitalized = registerCountry.title()

    # Insert new information to Database everytime a new user registers
    cur.execute('''INSERT OR IGNORE INTO Countries(country)
    VALUES (?)''', (registerCountryCapitalized, ))
    cur.execute('SELECT id FROM Countries WHERE country = ?', (registerCountryCapitalized, ))
    countryID = cur.fetchone()[0]   

    cur.execute('''INSERT OR IGNORE INTO Gender(gender)
    VALUES (?)''', (registerGender, ))
    cur.execute('SELECT id FROM Gender WHERE gender = ?', (registerGender, ))
    genderID = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Dates(birthDate)
    VALUES (?)''', (dateStr, ))
    cur.execute('SELECT id FROM Dates WHERE birthDate = ?', (dateStr, ))
    dateID = cur.fetchone()[0]
    
    cur.execute('''INSERT INTO Users(countryID, genderID, dateID, name, password, email)
    VALUES (?, ?, ?, ?, ?, ?)''', (countryID, genderID, dateID, registerUserrr, registerPass, registerEmail)) 

    conn.commit()    

def loginVerify():
    global userFullInfo
    global infoUserName, infoUserEmail, infoUserCountry, infoUserGender, infoUserDate
    global username
    username = userLogin.get()   # Use .get() on these because they are declared StrigVar above.
    password = passLogin.get()   # Work with the information I get from users 

    # Delete entries after user tries to log in
    userEntry1.delete(0, END)
    passwordEntry1.delete(0,END)

    # Get usernames and passwords from Database so I can verify the login
    conn = sqlite3.connect("usersInfo.sqlite")
    cur = conn.cursor()    

    cur.execute('''SELECT name, password FROM Users''')
    resultUsrPass = cur.fetchall()

    conn.commit()

    # Create a tuple with the information the user tries to login with so I can check if that information is in the Database or not
    loginTry = (username, password) 
    tempUsersList= []
    tempPasswordsList = [] 
    # Using the loginTry tuple created above. User can either login or try again, based on the (username AND password) the user types in! 
    if loginTry in resultUsrPass:
        # Record exists - Success!      
        loginSucess() 
        clock()
    else: 
        # Record non existent. Now I must find out if its because of the password or username.
        # The 2 lists created just above contain ALL the passwords and ALL the usernames on the Database so far.
        # Must check both 
        for item in resultUsrPass:
            tempUsersList.append(item[0])
            tempPasswordsList.append(item[1])
        if loginTry[0] not in tempUsersList:
            messagebox.showerror("Error", "Username not found.\n Try again!")
        else:
            messagebox.showerror("Error", "Password not found.\n Try again!") 

def loginSucess():
    global screen2
    global resultAll, resultCountries, resultDates, resultDates, resultGender, resultUsrPass
    screen2 = Toplevel(root)
    screen2.title("Create a Note")
    screen2.iconbitmap("icon.ico")
    screen2.geometry("550x350+1150+225")
    screen2.resizable(width=False, height=False)
    screen2.config(background=bgColorSecond)

    # Create the area for the user to write the text
    notesText = Text(screen2, width=64, height=15, wrap=WORD)
    notesText.grid(row=2, padx=15, pady=5)

    # Create the menu to save the file or quit
    menuBar = Menu(screen2)
    options = Menu(menuBar, activebackground="#C7C7C7", activeforeground="black")
    options.add_command(label="Save", command=lambda: saveNote(screen2, notesText))
    options.add_command(label="Quit", command=lambda: close())
    menuBar.add_cascade(label="File", menu=options)

    screen2.configure(menu=menuBar)

    # Fetch the personal information of each user so I can display it in the screen2
    # 1. First I get all the information of each table
    conn = sqlite3.connect("usersInfo.sqlite")
    cur = conn.cursor()  

    cur.execute('''SELECT * FROM Users''')
    resultAll = cur.fetchall()

    cur.execute('''SELECT * FROM Dates''')
    resultDates = cur.fetchall()

    cur.execute('''SELECT * FROM Countries''')
    resultCountries = cur.fetchall()

    cur.execute('''SELECT * FROM Gender''')
    resultGender = cur.fetchall()

    conn.commit()

    # 2. Then I select what I want to display from each table.
    # All these variables defined bellow:
    # infoUserName, infoUserEmail, infoUserCountry, infoUserGender, infoUserDate
    # contain the individual information of each user that has successfully loged in!
    global allEmailsList
    allEmailsList = []
    for item in resultAll:
        if username == item[4]:    
            infoUserEmail = item[6]
            infoUserName = item[4]
            dateid = item[3]
            genderid = item[2]
            countryid = item[1] 

    for item in resultDates:
        if dateid == item[0]:
            infoUserDate = item[1]

    for item in resultCountries:        
        if countryid == item[0]:
            infoUserCountry = item[1]    
          
    for item in resultGender:
        if genderid == item[0]:
            infoUserGender = item[1]

    # Display user information on "Create a Note" screen - (screen2)
    accountInfo = Label(screen2, text="User: " + infoUserName + " | " + infoUserGender + " | " + "Date of birth: " + infoUserDate +
                     " | " + "Place of birth: " + infoUserCountry, background=bgColorSecond, fg=textColor, font=generalFont)
    accountInfo2 = Label(screen2, text="-" + infoUserEmail + "-", background=bgColorSecond, fg=textColor, font=generalFont)
    accountInfo.grid(row=0, pady=5)
    accountInfo2.grid(row=1,column=0, pady=5) 

def saveNote(screen2, text):
    # The point of screen2 is to be able to create a text file and save it anywhere on the computer
    data = text.get('0.0', END)
    file = dialog.asksaveasfilename(parent=screen2, filetypes=[('text files', '.txt')])

    fileOut = open(file, "w")
    fileOut.write(data)
    fileOut.close()

def close():
    screen2.destroy()
    
def clock():
    # Put in a clock on screen2 just for fun
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    hourLabel = Label(screen2, text="", font=generalFont, fg=textColor, bg=bgColorSecond)
    hourLabel.place(x=15, y=45)
    hourLabel.config(text=hour + ":" + minute + ":" + second)
    hourLabel.after(1000, clock)
 

mainWindow()