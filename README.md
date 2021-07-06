## Table of contents
* [General info](#general-info)
* [Software](#software)
* [Setup](#setup)
* [Tutorial](#tutorial)

## General info
This project contains 3 main files:
* Final Test Report: Running file which generates a test report
* Mail Sender: Running file which send an automatic mail containing the report
* Bonnes pratiques procédure de test: Reading file which explains how to proceed with the test procedure, from to beginning of the sprint to the edition of test report and documentation
	
## Software
This project uses at least Python 3.9.2.

	
## Setup
To run this report editor, launch the following commands in python console to download the needed libraries:

```
$ pip install tkinter
$ pip install youtrack
$ pip install requests
$ pip install testrail
$ pip install canvas
$ pip install reportlab
```

To run the mail sender, launch the following commands in python console to download the needed libraries:

```
$ pip install smplib
$ pip install ssl
```


## Tutorial

To use this project, you must follow this procedure:
* If you are the tester, read the file "Bonnes_pratiques_procedure_de_test"
* Download this project
* Run "Final Report Editor" and a fill the tkinter window the following way:
	* Date : format DD/MM
	* Tester name : enter your name
	* Sprint number : example « Sprint 21-10 », it must be the exact same name as YouTrack
	* Sprint date : format DD/MM-DD/MM
	* Os : check IOS or Android 
	* Version number : example « Version 1.3.5 » (and not Version 1.3.5 (X) or 1.3.5 or 1.3.5 (X))
	* Uncategorized cards : check « No »
	* Version : Validated or Rejected (or algorithm but it is not functionnal at that point)
	* Unscheduled cards : cocher « Yes » if you want to add these YouTrack cards
* Open "Mail Sender" and fill it this way:
	* Fill the Python list "destinataires" with the recepients of your choice (pay attention with iOS developpers or Android developpers)
	* Fill the string variable "Version_number" with the number of the tested version (ex: Version 1.3.5 (1) or Version 3.19.1-RC2)
