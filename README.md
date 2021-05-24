![Sunset Storage Logo](static/favicon/favicon.png)
#'Sunset Storage'

### Institution, Module, & Student Information
- **Institution:** Griffith College Dublin
- **Course Name:** B.Sc. (Hons) in Computing Science
- **Module Name:** Cloud Services & Platforms
- **Module Code:** BSCH-CSP/Dub/PT
- **Student Name:** Alex Meade Wilson
- **Student Number:** 2950871

### Assignment Information
- **Title:** Application Development Assignment
- **Description:** Building Dropbox with Google App Engine
- **Issue Date:** Thursday 15th April 2021
- **Due Date:** Thursday 27th May 2021

### Online Application & Source Code (For a limited time only)
- **Application Name:** _"Sunset Storage" - Cloud File & Directory Service_ 
- **Web Application:** [https://amw-csp-dropbox.nw.r.appspot.com/login](https://amw-csp-dropbox.nw.r.appspot.com/login)
- **Application Code:** [https://github.com/AlexMeadeWilson/CSP.Dropbox](https://github.com/AlexMeadeWilson/CSP.Dropbox)

### Local Installation Steps
_To install and run this application locally, please follow these simple steps._

####Pre-Requisites
- An installation of Python 3.9 that is accessible from anywhere on the command line. 
- You can download Python 3.9 from here: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- A decent syntax highlighting text editor or IDE with support for Python, HTML, CSS, JS, Yaml, and JSON.
- I recommend PyCharm by JetBrains for this. 
- You can download PyCharm from here: [https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)

#####Command Line Installation Steps
- Clone this GitHub repository into a local Virtual Environment directory.
- Open up the Google Cloud SDK Shell Command Line editor.
- Navigate to the local Project directory and Scripts sub: `cd ../CSP.Dropbox/venv/Scripts`
- Type `activate` to start the Python Virtual Environment.
- Once the venv has activated, you should see a command line prefix of `(venv)`
- Navigate back to the Project root directory CSP.Dropbox directory: `cd ../CSP.Dropbox/`.
- You now need to install the necessary libraries to run this application.
- To do this, from the Project root directory again, type: `pip install -r requirements.txt`.
- Next, set the GOOGLE APPLICATION CREDENTIALS: `set GOOGLE_APPLICATION_CREDENTIALS=creds/amw-csp-dropbox-4372ed7880d9.json`
- Once set, type: `python main.py` to run the main Python application. 
- This should begin running a local instance of the Application and Web Service
- In your browser, go to `http://localhost:8080/` or `http://127.0.0.1:8080/`

### How to use this Application
- To understand the UI, and how to use this Application;
- Refer to the embedded documentation found here: [2950871_AlexMeadeWilson_CSP_Assignment_Document.pdf](docs/2950871_AlexMeadeWilson_CSP_Assignment_Document.pdf).

_Thank you, and enjoy "Sunset Storage"._
_Alex Meade Wilson._