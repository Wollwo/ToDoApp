# ToDoApp
small application in python to track your To Do's

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

DB will be created after first run. sqlite3 is used
