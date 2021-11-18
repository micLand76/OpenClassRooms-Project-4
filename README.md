# OpenClassRooms-Project-4
Chess Tournament

## About / Synopsis

* This is a project to use the OOP and the MVC pattern
* It's a program to manage a chess tournament with rounds and matchs

## Installation

* Install Python on your PC, for your OS, by downloading it on the Python website: https://www.python.org/downloads/
* download the application on https://github.com/micLand76/OpenClassRooms-Project-4 by cliquing on 'Code' and download zip
* extract the zip you've downloaded
* with a terminal, change the repositorie where you are to be in the reporsitorie of the repositorie of the app
* in the terminal, run pip command to install tinydb and tinydb_serialization (the command is 'pip install tinydb' for ex)
* run the command 'python (or python3 on Linux) main.py'

## Usage

* With this application, you can save tournaments datas with the ranking of the players, even your connection is not working.

### Features

* The script is written in Python 3.7.3<br>
* I used the internal librairies datetime, json and tinydb.<br>
* datetime is used to save and display the dates and times of the tournaments and rounds.<br>
* tinydb is used to save the datas into the Tinydb with the JSON format.<br>

### Content

The program is begining with a menu with 3 choices: Tournament, Players and Reports.
* In the Tournament menu you can create a tournament and create rounds with generating pairs of players based on the swiss algorithme.<br>
* In the player menu, you can add players and manage their ranking.<br>
* In the report menu, you can display the tournaments, the rounds, the matchs, the players and the actors.<br>

