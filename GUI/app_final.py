from appJar import gui
from brClient import *

#personal information for client
personal_profiles = {}
personalInfo = ["lastName", "firstName", "city", "state", "country",
                "zipCode", "email", "phone", "language"]

#legal information for client (i.e. USCIS form information)
legal_profiles = {}
legalInfo = ["lastName1", "firstName1", "A-ID", "receipt_number", "case_status",
            "answer1", "answer2", "answer3", "answer4", "answer5", "answer6",
            "answer7", "answer8", "answer9", "answer10", "answer11", "answer12"]

#questions/answers to survey questions
questionsAnswers = {"answer3":"In what city were you born?",
                    "answer12":"What is your father’s middle name?",
                    "answer10":"In what city was your first job?",
                    "answer9":"What is your favorite animal?",
                    "answer5":"What is your favorite movie?",
                    "answer2":"What is your favorite sport?",
                    "answer11":"What is your mother’s maiden name?",
                    "answer8":"What is your oldest child’s middle name?",
                    "answer7":"What was the color of your first car?",
                    "answer1":"What was the name of your first pet?",
                    "answer6":"What year did you get married?",
                    "answer4":"What year did you graduate from high school?"}

#matches widgets with information role
infoLabel = {"A-ID":"A-ID", "lastName":"Last Name", "lastName1":"Client Last Name",
"firstName":"First Name",  "firstName1":"Client First Name", "city":"City", "country":"Country", "state":"State",
    "zipCode":"Zip Code", "email":"Email", "phone":"Phone", "language":"Language",
    "receipt_number":"Receipt Number"}


logins = {}


def new_profile(button):
    #dict stores all info for one immigrant
    immInfo = {}

    #extracts various text fields
    for info in personalInfo:
        if info not in ("zipCode", "phone", "language"):
            immInfo[info] = app.getEntry(info)
        elif info is "language":
            immInfo[info] = app.getOptionBox("language")
        else:
            immInfo[info] = int(app.getEntry(info))

    #adds to the master dictionary
    personal_profiles[immInfo["lastName"] + immInfo["firstName"]] = immInfo

    #adds to the table
    app.openTab("USCIS App", "Contact Information")
    app.addTableRow("g1", list(immInfo.values()))

    #clears out the other textfields
    app.clearAllEntries()
    resetTextBoxes()


def create_account(button):
    immInfo = {}

    #we don't have case status yet (haven't accessed account)
    for info in legalInfo:
        if info != "case_status":
            immInfo[info] = app.getEntry(info)


    if immInfo["lastName1"]+immInfo["firstName1"] not in personal_profiles:
        return

    #randomly generates a username-password pair
    immInfo["username"] = randomStringDigits()
    immInfo["password"] = randomStringDigits()
    immInfo["receipt_number"] = [int(app.getEntry("receipt_number"))]
    immInfo["added_receipts"] = []

    for info in personal_profiles[immInfo["lastName1"]+immInfo["firstName1"]]:
        immInfo[info] =  personal_profiles[immInfo["lastName1"]+ \
                            immInfo["firstName1"]][info]

    #accesses and sets up USCIS account remotely
    setupUSCIS(immInfo)

    #grabs the updates for the case and stores in dictionary
    immInfo["case_status"] = updateCases(immInfo)

    #deletes unnecessary personal information for account creation
    for info in personal_profiles[immInfo["lastName1"]+immInfo["firstName1"]]:
        del immInfo[info]

    legal_profiles[immInfo["lastName1"]+immInfo["firstName1"]] = immInfo

    #updates table
    app.openTab("USCIS App", "Case Status")
    app.addTableRow("g2", list(immInfo.values()))

    app.clearAllEntries()
    resetTextBoxes()


#resets all fields to default
def resetTextBoxes():
    app.openTab("USCIS App", "Create New Account")
    for info in legalInfo:
        if info == "case_status":
            continue
        elif info not in ("answer1", "answer2", "answer3",
            "answer4", "answer5", "answer6", "answer7", "answer8", "answer9",
            "answer10", "answer11", "answer12"):
            app.setEntryDefault(info, infoLabel[info])
        else:
            app.setEntryDefault(info, questionsAnswers[info])


    app.openTab("USCIS App", "New Profile")
    for info in personalInfo:
        if info not in ("zipCode", "phone", "language"):
            app.setEntryDefault(info, infoLabel[info])
        elif info is "language":
            app.setOptionBox("language", 0)
        else:
            app.setEntryDefault(info, infoLabel[info])

    app.openTab("USCIS App", "Delete Profile")
    app.setEntryDefault("LastName", "Last Name")
    app.setEntryDefault("FirstName", "First Name")


def deleteProfile(button):
    name = app.getEntry("LastName")+app.getEntry("FirstName")

    #checks if name is in profile, deletes if so
    if name in personal_profiles:
        contact_row = list(personal_profiles.keys()).index(name)
        del personal_profiles[name]
        app.openTab("USCIS App", "Contact Information")
        app.deleteTableRow("g1", contact_row)
    if name in legal_profiles:
        legal_row = list(legal_profiles.keys()).index(name)
        del legal_profiles[name]
        app.openTab("USCIS App", "Case Status")
        app.deleteTableRow("g2", legal_row)

    app.clearAllEntries()
    resetTextBoxes()


color_order = ("GreenYellow", "Chartreuse",
               "LawnGreen","Lime", "PaleGreen", "LimeGreen", "LightGreen",
               "MediumSpringGreen", "SpringGreen", "Aquamarine", "Aqua",
               "Cyan", "PaleTurquoise", "Turquoise", "MediumTurquoise",
               "DarkTurquoise", "LightSkyBlue", "DeepSkyBlue")

#colors in the background for each tab
def colorization(num, alpha):
    app.startFrame("Pixels"+str(num), row=0, column=0, colspan=5, rowspan=10)
    for i in range(1, 19):
        app.addLabel(alpha+str(i), text="", row=(i-1)//6, column=i%6)
    for i in range(1, 19):
        app.setLabelBg(alpha+str(i), color_order[i-1])
    app.stopFrame()


with gui("Profile", "1200x600") as app:
    app.startTabbedFrame("USCIS App")
    app.setTabbedFrameDisableAllTabs("USCIS App")
    app.setFont(24)
    
    #Login Page
    app.startTab("Login")
    app.addLabel("title", "Welcome to USCIS Assistant")
    colorization(1, "l")
    app.startFrame("loginInfo")
    app.setLabelBg("title", "White")
    app.label("username", "Username", row=0, column=1)
    app.setLabelBg("username", "White")
    app.entry("username", pos=('p', 1), row=0, column=2)
    app.setEntryDefault("username", "Username")
    app.label("password", "Password", row=1, column=1)
    app.setLabelBg("password", "White")
    app.entry("password", pos=('p', 1), secret=True, row=1, column=2)
    app.setEntryDefault("password", "Password")
    app.raiseFrame("loginInfo")
    app.stopFrame()
    app.stopTab()

    #new Profile tab
    app.startTab("New Profile")
    colorization(2, "b")
    #sets up text-fields (different types for different variables)
    for info in personalInfo:
        if info not in ("zipCode", "phone", "language"):
            app.addEntry(info)
            app.setEntryDefault(info, infoLabel[info])
        elif info is "language":
            app.addOptionBox("language", ["Select Language", "English", "Spanish"])
        else:
            app.addNumericEntry(info)
            app.setEntryDefault(info, infoLabel[info])

    #adds a submission button
    app.addButton("Enter", new_profile)
    app.stopTab()

    #new Contact Info Tab
    app.startTab("Contact Information")
    colorization(3, "c")

    app.setFont(20)
    app.addTable("g1", [["Last Name", "First Name", "City", "State",
     "Country", "Zip Code", "Email", "Phone", "Language"]])
    app.stopTab()

    #new tab: displays the case filing status
    app.startTab("Case Status")
    colorization(4, "d")
    app.addTable("g2", [["Last Name", "First Name", "A-ID", "Receipt Number",
    "Case Status"]])
    app.stopTab()

    #account creation tab
    app.startTab("Create New Account")
    colorization(5, "e")
    for info in legalInfo:
        if info == "case_status":
            continue
        elif info not in ("answer1", "answer2", "answer3",
            "answer4", "answer5", "answer6", "answer7", "answer8", "answer9",
            "answer10", "answer11", "answer12"):
            app.addEntry(info)
            app.setEntryDefault(info, infoLabel[info])
        else:
            app.addEntry(info)
            app.setEntryDefault(info, questionsAnswers[info])
    app.addButton("Submit", create_account)
    app.stopTab()

    #account deletion tab
    app.startTab("Delete Profile")



    app.addEntry("LastName")
    colorization(6, "f")
    app.setEntryDefault("LastName", "Last Name")
    app.addEntry("FirstName")
    app.setEntryDefault("FirstName", "First Name")
    app.addButton("Delete", deleteProfile)
    app.stopTab()


    app.stopTabbedFrame()

    app.go()
