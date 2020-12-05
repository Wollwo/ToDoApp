# ToDoApp
small application in python to track your To Do's

_Prerequisities_:
python3, tkinter, sqlite3

Config File "ToDoConfig.cfg" will be created after first run
_Default config settings:_
DB_NAME=ToDo.db
MY_USER=Default
TRASH=True
KEEP_TRASH=D30
TABLE=main
TODO_SORTING_NEW_TO_OLD=False

_DB_NAME_ - how db file will be named
_TABLE_ - how table in DB will be named
_MY_USER_ - only tasks of specified user are shown and trashed
_TRASH_ - if true, then tab for trash will be visible
_KEEP_TRASH_ - this is how long trashed ToDo will be keeped after last change
D10 - keep 10 Days from last change
M1 - keep 1 Month from last change
Y2 - keep 2 Years from last change
h2 - keep 2 hours from last change
m2 - keep 2 minutes from last change
s2 - keep 2 seconds from last change
_TODO_SORTING_NEW_TO_OLD_ - sorting of ToDos, if False, than old are on top

_DB Header_
time_created (integer PRIMARY KEY)
time_last_changed (integer NOT NULL)
checked (integer NOT NULL) 0 or 1
title (text NOT NULL)
notes (text)
trashed (integer NOT NULL) 0 or 1
user (text NOT NULL)

_CSV for import_
row: [YYYY][MM][DD][hh][mm][ss];[YYYY][MM][DD][hh][mm][ss];0;My Title;My Note&#10&#34Note&#59Note&#34;0;Default
YYYY (year)   = 2020
MM (month)    = 12
DD (day)      = 24
hh (hour 24H) = 13
mm (minutes)  = 01
ss (seconds)  = 01

_Special characters in Notes_
new line, \n, &#10
double quote, ", &#34
semicolon, ;, &#59

