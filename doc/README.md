# Team 3 - We Showed Up - Prevent, Mitigate, and Recover (PMR) Insight Collective Knowledge System (PICK)

## About

The Prevent, Mitigate, Recovery (PMR) Insight Collective Knowledge (PICK) tool is a closed platform dedicated to allow the ingestion of log entires of different formats, to be suffeciently ingested in the SPLUNK application.

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

## SPLUNK

After following instruction setup up for SPLUNK up. There are a couple things to note:

### Adding users to an account:

Open up the SPLUNK web application, go to ```Settings > Users``` then add the user name and a password for each analyst that will connect.

### Other notes:

As our application retrieves the log entries as a stream per the clients, there is no capability implemented to modify the descriptions for the individual entries.

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
