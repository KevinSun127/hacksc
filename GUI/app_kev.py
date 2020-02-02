from appJar import gui
from brClient import *

check = 0
personal_profiles = {}
personalInfo = ["lastName", "firstName", "city", "state", "country",
                "zipCode", "email", "phone", "language"]

legal_profiles = {}
legalInfo = ["lastName1", "firstName1", "A-ID", "receipt_number", "case_status",
            "answer1", "answer2", "answer3", "answer4", "answer5", "answer6",
            "answer7", "answer8", "answer9", "answer10", "answer11", "answer12"]

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

infoLabel = {"A-ID":"A-ID", "lastName":"Last Name", "lastName1":"Client Last Name",
"firstName":"First Name",  "firstName1":"Client First Name", "city":"City", "country":"Country", "state":"State",
    "zipCode":"Zip Code", "email":"Email", "phone":"Phone", "language":"Language",
    "receipt_number":"Receipt Number"}


logins = {}


def new_profile(button):
    immInfo = {}

    for info in personalInfo:
        if info not in ("zipCode", "phone", "language"):
            immInfo[info] = app.getEntry(info)
        elif info is "language":
            immInfo[info] = app.getOptionBox("language")
        else:
            immInfo[info] = int(app.getEntry(info))


    personal_profiles[immInfo["lastName"] + immInfo["firstName"]] = immInfo
    print(personal_profiles)

    app.openTab("USCIS App", "Contact Information")
    app.addTableRow("g1", list(immInfo.values()))

    app.clearAllEntries()
    resetTextBoxes()


def deleteEntry():
    return
    #write later


def create_account(button):
    immInfo = {}

    for info in legalInfo:
        if info != "case_status":
            immInfo[info] = app.getEntry(info)


    if immInfo["lastName1"]+immInfo["firstName1"] not in personal_profiles:
        return

    immInfo["username"] = randomStringDigits()
    immInfo["password"] = randomStringDigits()
    immInfo["receipt_number"] = [int(app.getEntry("receipt_number"))]
    immInfo["added_receipts"] = []

    for info in personal_profiles[immInfo["lastName1"]+immInfo["firstName1"]]:
        immInfo[info] =  personal_profiles[immInfo["lastName1"]+ \
                            immInfo["firstName1"]][info]


    # setupUSCIS(immInfo)
    # immInfo["case_status"] = updateCases(immInfo)

    for info in personal_profiles[immInfo["lastName1"]+immInfo["firstName1"]]:
        del immInfo[info]

    legal_profiles[immInfo["lastName1"]+immInfo["firstName1"]] = immInfo


    app.openTab("USCIS App", "Case Status")
    app.addTableRow("g2", list(immInfo.values()))

    app.clearAllEntries()
    resetTextBoxes()


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



def login(button):
    app.setTabbedFrameDisableAllTabs("USCIS App", False)


####LOGIN PAGE
with gui("Profile", "1200x600") as app:
    app.startTabbedFrame("USCIS App")
    app.setTabbedFrameDisableAllTabs("USCIS App")





    app.startTab("Login")
    app.label("username", "Username", sticky="ew")
    app.entry("username", pos=('p', 1), focus=True)
    app.label("password", "Password")
    app.entry("password", pos=('p', 1), secret=True)
    app.addButton("Login", login)
    app.stopTab()

###LOGINPAGE


    app.startTab("New Profile")

    for info in personalInfo:
        if info not in ("zipCode", "phone", "language"):
            app.addEntry(info)
            app.setEntryDefault(info, infoLabel[info])
        elif info is "language":
            app.addOptionBox("language", ["Select Language", "English", "Spanish"])
        else:
            app.addNumericEntry(info)
            app.setEntryDefault(info, infoLabel[info])

    app.addButton("Enter", new_profile)
    app.stopTab()


    app.startTab("Contact Information")
    app.setFont(20)
    app.addTable("g1", [["Last Name", "First Name", "City", "State",
     "Country", "Zip Code", "Email", "Phone", "Language"]])
    app.stopTab()

    app.startTab("Case Status")
    app.addTable("g2", [["Last Name", "First Name", "A-ID", "Receipt Number",
    "Case Status"]])
    app.stopTab()


    app.startTab("Create New Account")

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

    app.stopTabbedFrame()

    app.go()
