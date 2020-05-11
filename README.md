# Team 3 - We Showed Up - Prevent, Mitigate, and Recover (PMR) Insight Collective Knowledge System (PICK)

## About

The PICK tool is a closed platform software dedicated to allow the ingestion of log entries of different formats by cleansing and transcribing log files before sending them to be ingested in the SPLUNK application, and allowing analysts to manipulate the log entries to create a graph out of them in order to tell a story of the events in a more cohesive way rather than using several applications which is time consuming.

---

## Installation

The PICK tool utilizes a series of offline, local extensions needed for successful installation and optimized running performance. Before running the project, please ensure you have a suffecient computer with the following qualifications:

- Minimum 4 GB RAM for 32-bit (x86) or 8 GB for 64-bit (x64)
- Running a Unix (Linux) based operating system, Kali Linux strongly preferred
- 1 GHz processor or faster 32-bit (x86) or 64-bit (x64)
- Minimum 16 GB of hard disk drive space for 32-bit (x86) or 20 GB for 64-bit (x64)
- Python version 2.7 or Higher
- Pip or Pip3 (for extension installations)
- MongoDB Application
- SPLUNK Application

---

## Dependencies

The PICK Tool requires a set of required extensions which can be installed using the following commands on the terminal:

|    Purpose                |    Tool       |    Name                    |    Version      |    Command                                       |
|---------------------------|---------------|----------------------------|-----------------|--------------------------------------------------|
|    General   Downloads    |    APT        |    PyQT5                   |                 |                                                  |
|                           |    APT        |    QTDesigner              |                 |    >sudo   apt-get install qttools5-dev-tools    |
|    SPLUNK                 |    website    |    SPLUNK                  |    8.0.3        |    Follow   instructions on website              |
|                           |    website    |    splunk-sdk-python       |    1.6.12       |    Follow   instructions on github               |
|    Database               |               |    MongoDB                 |                 |                                                  |
|                           |    pip        |    PyMongo                 |                 |    >pip   install pymongo                        |
|                           |    pip        |    PyMongo(server)         |                 |    >pip   install pymongo[srv]                   |
|    Graph                  |    pip        |    QGraphViz               |    0.0.45       |    >pip   install QGraphViz                      |
|    Audio   Transcriber    |    pip        |    Speech   Recognition    |    3.8.1        |    >pip   install SpeechRecognition              |
|                           |    pip        |    PocketSphinx            |    0.1.17       |    >pip   install pocketsphinx                   |
|                           |    APT        |    LibraSound2             |    1.2.2-2.1    |    >sudo   apt-get install libasound2            |
|    OCR   Feeder           |    pip        |    PyTesseract             |    0.3.4        |    >pip install pytesseract                      |
|                           |    pip        |    Pillow                  |                 |    >pip   install pillow                         |
---


## Build

To build the main UI python inside the UI folder, run  ```pyuic -x mainwindow.ui -o mainwindow.py``` 

---

## Running the Code

In order to run the PICK tool, the following prerequisites must be running in the backround using Kali Linux:

- > splunk (cd to project directory and run SPLUNK)
- > mongod (cd to project directory to start the MongoDB database)
- > mongo[srv] (cd to project directory to start the MongoDB database server)

Once the above platforms are running in the background we can now run the program. First, change directory into the project directory by using ```cd pick-tool-team03-we-showed-up```. Once inside the directory, simply ```cd src``` which we want to access the src folder for running the main executable file. Running typing in ```python MainExecutable.py```, which then compiles and runs the program.

At start up session, you must login to SPLUNK using the Event Configuration to access user credentials.

---

## Auditing

The naming convention for the classes will follow the camel-case convention (i.e.,
UserInterface(PickUI)) and the naming conventions for the methods and variables will follow the snake-case
convention (i.e., process_image_logs(log_path)). Finally, the SRS, the client feedback from previous demos, 
and the test plan will be used as a guideline to test the behavior of each UI component in the system to ensure
that the system is functional in accordance with the clients’ specifications and requirements.

Reports on updates were traced back to the SRS and other documents such as recordings and notes taken during demos to ensure the
features that were implemented in the software complied with the client’s specifications. The executable file in the
main repository “MainExecutable.py” underwent black box and sanity testing to ensure, from the
perspective of the end-user, that the features on the update reports were included and implemented in the main
executable file, as well as considered the basic usability and accessibility of the application. The tests for the
project have been explained and the results have been documented in the test plan which is located in the /src
folder in the GitHub repository.


---

## Acknowledgements

### Guidance Team and Clients

* Thank you for allowing us to develop our skills as Software Engineers by working on this project and providing guidance.

### Team Members

* Ricardo Alvarez (Designer)
* Daniela Garcia (Systems Analyst)
* Matthew Iglesias (Systems Architect)
* Jessica Redekop (Lead Programmer)
* Diego Rincon (V&V Supervisor)

---
