#Purpose
This is a POC to try and identify passwords from  key log file from metasploit

#Run Project
* You need to install Python 3.6 64-bit as this version of tensorflow only supports Python 3.5/3.6 64-bit
* Install dependencies, run on root of the project 'pip install -r requirements.txt'
* Start program, run on root of the project 'python RunModel.py'
* A GUI should should appear
![PictureOfGui][PictureOfGui.PNG]
* Do one of the following tests
** Test a password in isolation
** Test a line in a key log in isolation
** Test an entire key log text file
*** Can choose 3 options to analyze file
*** The results come up in a separate window

#Structure Of Project
