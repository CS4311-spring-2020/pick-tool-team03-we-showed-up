# Team 3 - We Showed Up

## Build

The Prevent, Mitigate, Recovery (PMR) Insight Collective Knowledge (PICK) tool is a closed platform dedicated to allow the ingestion of log entires of different formats, to be suffeciently ingested in the SPLUNK application.

---

## Deployment

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

The PICK Tool requires a set of required extensions which can be installed using the following commands on the terminal:
    
**Audio Transcriber**

    > pip install SpeechRecognition
    > pip install pocketsphinx
    > sudo apt-get install libasound2-dev

**Database**

    > pip install pymongo
    > pip install pymongo[srv]

**Graphing**

    > pip intsall QGraphViz

**SPLUNK**

    > pip install splunk-python-sdk

## Versioning
---

## Acknowledegements


### Team Members
* Ricardo Alvarez (Designer)
* Daniela Garcia (Systems Analyst)
* Matthew Iglesias (Systems Architect)
* Jessica Redekop (Lead Programmer)
* Diego Rincon (V&V Supervisor)
---
