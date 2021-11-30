# OpenClassRooms-Project-4
Chess Tournament

## About / Synopsis

* This is a project to use the OOP and the MVC pattern
* It's a program to manage a chess tournament with rounds and matchs

## Installation

### On a Windows OS:
* paste:   ``` https://github.com/micLand76/OpenClassRooms-Project-4 on your navigator   ```
* There, clic on "Code" and on "Download.zip"
* Execute a Windows Terminal and enter the command to execute Python: 
	* change the place you are to go to the repo of python
	* open a Git Bash window, use the commande: ``` python -m venv OC ``` 
	* activate the virtual environment: ```  OC/Scripts/activate.bat ``` 
	* try to execute the application: ``` python c://"emplacement repo"/main.py ```
* install some librairies with pip:
  ```
  python -m pip install tinydb
  python -m pip install tinydb_serialization
  ```
* execute main.py 
* install flake8: 
  ```
  python -m pip install flake8
  ```
* execute flake8 on main.py: 
  ``` 
  python -m flake8 c://"emplacement repo"/main.py
  ```

### On a linux OS:
* Open a Terminal window
* Clone the project on your computer: ``` "git clone https://github.com/micLand76/OpenClassRooms-Project-4.git" ```
* in the repo of the project, open a Bash window:
	* create the virtual environment; if you can't use venv, install it with: ```sudo apt install python3.8-venv```
	* use the commande: ``` python3 -m venv OC ``` 
	* activate the virtual environment: ``` source OC/bin/activate ``` 
* To use the app, install the librairies "tinydb" and "tinydb_serialization":
```
 'pip install tinydb'
 'pip install tinydb_serialization'
```
* You can use the app with this chain: ``` python3 "repo of the app/"main.py ```
* Finally, install Flake8: ``` "sudo apt install flake8" ``` (enter "o" when it asks if you want to continue)
* And ``` flake8 main.py ```


## Usage

* With this application, you can save tournaments datas with the ranking of the players, even your connection is not working.

## Features

* The script is written in Python 3.7.3<br>
* I used the internal librairies datetime, json and tinydb.<br>
* datetime is used to save and display the dates and times of the tournaments and rounds.<br>
* tinydb is used to save the datas into the Tinydb with the JSON format.<br>

## Content

The program is begining with a menu with 3 choices: Tournament, Players and Reports.
* In the Tournament menu you can create a tournament and create rounds with generating pairs of players based on the swiss algorithme.<br>
* In the player menu, you can add players and manage their ranking.<br>
* In the report menu, you can display the tournaments, the rounds, the matchs, the players and the actors.<br>

