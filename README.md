# HackSC 2020
## Automated Immigration Filings
For this year's HackSC, Anthony and I created a Python application that stores client information, retreives case filings from the USCIS, and remotely generates accounts for immigrants seeking green cards. By maximizing the efficiency of legal work, this would alleviate some of the burdens associated with pro-bono legal counsel -- a role that demands incredible quantities of paperwork and information. 


## Getting Started
### Prerequisites
You should make sure that Python is installed on your device. 
Additionally, this project makes heavy use of web drivers and json parsing. This requires several packages which acn be installed via:
`pip install mechanize selenium requests bs4 random re`


## Running Program
### Quick Overview
To launch the python script, type the following command-line prompt:
`python GUI/app_final.py`

This will open the graphic user-interface, and launch the application. 

You can add clients' and their personal information under the "New Profile" tab.
You can add clients' and their legal information (i.e. A-ID's and USCIS receipt numbers) by signing them up for an account under the "Create New Account" tab. 
You track the your clients' case status and contact information under the "Contact Information" and "Case Status" tabs, respectively. 
You can delete clients from your profile list under the "Delete Profile" tab. 

[February 2nd: The login/save features have yet to be implemented. You can safely ignore these.]



