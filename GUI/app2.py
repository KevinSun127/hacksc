from appJar import gui

app = gui("Profile", "1200x600")
check = 0

def enter(button):
    if button == "Enter":

        last_temp = app.getEntry("last")
        first_temp = app.getEntry("first")
        city_temp = app.getEntry("city")
        country_temp = app.getEntry("country")
        state_temp = app.getEntry("state")
        zip_temp = int(app.getEntry("zip"))
        email_temp = app.getEntry("email")
        phone_temp = int(app.getEntry("phone"))
        lang_temp = app.getOptionBox("lang")
        anum_temp = int(app.getEntry("anum"))
        app.removeAllWidgets()

        app.addButton("Add Profile", profile)

        app.addLabel("l0", "Last Name", 1, 0)
        app.addLabel("l1", "First Name", 1, 1)
        app.setLabelBg("l1", "WhiteSmoke")
        app.addLabel("l2", "Country", 1, 2)
        app.addLabel("l3", "City", 1, 3)
        app.setLabelBg("l3", "WhiteSmoke")
        app.addLabel("l4", "State", 1, 4)
        app.addLabel("l5", "zipCode", 1, 5)
        app.setLabelBg("l5", "WhiteSmoke")
        app.addLabel("l6", "Email", 1, 6)
        app.addLabel("l7", "Phone", 1, 7)
        app.setLabelBg("l7", "WhiteSmoke")
        app.addLabel("l8", "Language", 1, 8)
        app.addLabel("l9", "A-Number", 1, 9)
        app.setLabelBg("l9", "WhiteSmoke")

        r = app.getRow()
        app.setStretch("both")
        app.setSticky("nesw")

        app.addLabel("last1", text=anum_temp, row=r, column=0)
        app.addLabel("first1", text=first_temp, row=r, column=1)
        app.setLabelBg("first1", "WhiteSmoke")
        app.addLabel("country1", text=country_temp, row=r, column=2)
        app.addLabel("city1", text=city_temp, row=r, column=3)
        app.setLabelBg("city1", "WhiteSmoke")
        app.addLabel("state1", text=state_temp, row=r, column=4)
        app.addLabel("zip1", text=zip_temp, row=r, column=5)
        app.setLabelBg("zip1", "WhiteSmoke")
        app.addLabel("email1", text=email_temp, row=r, column=6)
        app.addLabel("phone1", text=phone_temp, row=r, column=7)
        app.setLabelBg("phone1", "WhiteSmoke")
        app.addLabel("lang1", text=lang_temp, row=r, column=8)
        app.addLabel("anum1", text=anum_temp, row=r, column=9)
        app.setLabelBg("anum1", "WhiteSmoke")

        if button == "Add Profile":
            app.hideWidgetType("Label", "last1", collapse=True)
            check = 1

def profile(button):
    if button == "New Profile" or check == 1:
        check = 0
        app.addEntry("last")
        app.setEntryDefault("last", "Last Name")
        app.addEntry("first")
        app.setEntryDefault("first", "First Name")
        app.addEntry("country")
        app.setEntryDefault("country", "Country")
        app.addEntry("city")
        app.setEntryDefault("city", "City")
        app.addEntry("state")
        app.setEntryDefault("state", "State")
        app.addNumericEntry("zip")
        app.setEntryDefault("zip", "ZipCode")
        app.addEntry("email")
        app.setEntryDefault("email", "Email")
        app.addNumericEntry("phone")
        app.setEntryDefault("phone", "Phone Number")
        app.addOptionBox("lang", ["Select Language", "English", "Spanish", "Both"])
        app.addNumericEntry("anum")
        app.setEntryDefault("anum", "A-Number")
        app.addButton("Enter", enter)

app.addButton("New Profile", profile)

app.go()