#http://appjar.info/

#1. Login Page
#2. Information
    #A. Button that toggles new profile creation
    #B. Button that fetches update to the case



from appJar import gui

def login(button):
    if button == "Cancel":
        app.stop()
    else:
        usr = app.getEntry("Username")
        pwd = app.getEntry("Password")
        app.removeAllWidgets()

app = gui("Login Window", "400x200")
app.startLabelFrame("Login Details")
app.setBg("orange")
app.setFont(18)

app.addLabel("title", "Welcome to USCIS Assistant")
app.setLabelBg("title", "white")

app.addLabelEntry("Username")
app.addLabelSecretEntry("Password")

app.addButtons(["Submit", "Cancel"], login)
app.setFocus("Username")

app.go()


main()
