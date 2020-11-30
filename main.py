from Classes.getcurrentdatetime import GetCurrentDatetime
from Classes.allaboutdatabase import AllAboutDatabase
from Classes.configclass import ConfigClass

from sys import argv
from os.path import dirname

import tkinter as tk
from tkinter import Tk
from tkinter import ttk


#: ----------------
#: what can be set in config for cleaning DB
#: KEEP_TRASH=m1
#: D10 - keep 10 Days from last change
#: M1 - keep 1 Month from last change
#: Y2 - keep 2 Years from last change
#: h2 - keep 2 hours from last change
#: m2 - keep 2 minutes from last change
#: s2 - keep 2 seconds from last change
#: ----------------
# ToDo : System Try ico, close to TRY
# ToDo : Always on top
# ToDo : Opacity of main window
#: ----------------

#############
# VARIABLES #
#############


#############
#  CLASSES  #
#############

class MyGui:
    def __init__(self, parent, config_object, sql_create_main_table, my_debug=False):
        self.parent = parent
        self.sqlCreateMainTable = sql_create_main_table
        self.myDebug = my_debug

        #: config
        self.configObject = config_object
        self.myConfig = self.configObject.get_my_conf_dict()
        self.myConfFileNameWithPath = self.configObject.get_my_conf_file_name()
        self.my_user = self.myConfig['MY_USER']
        self.keep_trash_list = self.change_keep_trash_to_list(self.myConfig['KEEP_TRASH'])

        #: database object
        self.dbObject = AllAboutDatabase(self.myConfig['DB_NAME'], self.sqlCreateMainTable, self.myConfig['TABLE'],
                                         my_debug=myDebug)
        #: clean DB
        self.clean_db(self.keep_trash_list)

        #: #############
        #: main window #
        #: #############

        self.parent.title('"To Do" list')
        self.parent.geometry("700x300")
        self.parent.resizable(False, False)

        #: ###############
        #: file menu bar #
        #: ###############
        file_name = "File"
        file_menu_bar = tk.Menu(parent)
        self.parent.config(menu=file_menu_bar)
        file = tk.Menu(file_menu_bar, tearoff=False)

        #: add new to do task
        file.add_command(
            label='ADD',
            command=lambda: [self.command_button_show_edit(f'"ADD" button in {file_name} menu pressed',
                                                           my_user=self.my_user)])

        #: open config
        file.add_command(
            label="Config",
            command=lambda: [self.command_button_show_config(f'"Config" button in {file_name} menu pressed')])

        #: exit app
        file.add_command(
            label="Exit",
            command=lambda: [self.command_button_exit(f'"Exit" button in {file_name} menu pressed')]
        )
        #: initialize
        file_menu_bar.add_cascade(label="File", menu=file)

        #: preparation for tabs: active, done, trash
        self.tabs = {}
        self.create_tabs()

    #: Debug method
    def debug(self, text='nothing specified'):
        if self.myDebug:
            print(f'DEBUG INFO: {text}')

    #: ################################
    #: Commands for File menu Buttons #
    #: ################################

    def command_button_show_edit(self, to_print, my_user, new=True):
        self.debug(to_print)
        if new:
            todo_task_dict = {}
            self.edit_popup(new, my_user, todo_task_dict)

    def command_button_show_config(self, to_print):
        self.debug(to_print)
        self.config_popup()

    def command_button_exit(self, to_print):
        self.debug(to_print)
        self.parent.destroy()

    #: ##############
    #: Reload Logic #
    #: ##############

    def command_reload_tabs(self):
        self.tabs['tab_parent'].destroy()
        self.create_tabs()

    #: ##########
    #: Cleaning #
    #: ##########
    def clean_db(self, in_list):
        current_time = int(self.change_to_seconds(GetCurrentDatetime().get_compact_datetime()))
        db_list = self.dbObject.print_table()
        self.debug(f'cleaning DB: current time:{str(current_time)}, in_list: {str(in_list)}')
        my_time = int(in_list[1])
        my_str = in_list[0]

        line_limit = 946080000
        if my_str == 'Y':
            line_limit = current_time - (my_time * 946080000)
        elif my_str == 'M':
            line_limit = current_time - (my_time * 2592000)
        elif my_str == 'D':
            line_limit = current_time - (my_time * 86400)
        elif my_str == 'h':
            line_limit = current_time - (my_time * 3600)
        elif my_str == 'm':
            line_limit = current_time - (my_time * 60)
        elif my_str == 's':
            line_limit = current_time - my_time

        for line in db_list:
            if line['trashed'] == '1' and line['user'] == self.myConfig['MY_USER']:
                if self.change_to_seconds(line['time_last_changed']) <= line_limit:
                    self.debug(f'math: db_time: {line["time_last_changed"]} -- limit: {line_limit}')
                    self.dbObject.remove_lines_in_table([line['time_created']])

    #: ################
    #: Transformation #
    #: ################

    @staticmethod
    def change_quotes_in_text(task, text):
        if task == 'write':
            text = text.replace('"', '&#34')
        elif task == 'read':
            text = text.replace('&#34', '"')
        return text

    @staticmethod
    def change_keep_trash_to_list(in_string):
        out_list = [in_string[0:1], in_string[1:]]
        return out_list

    @staticmethod
    def change_time_to_readable(date):
        date = f'{date[0:4]}.{date[4:6]}.{date[6:8]} {date[8:10]}:{date[10:12]}:{date[12:]}'
        return date

    @staticmethod
    def change_to_seconds(in_time):
        in_time = int(in_time[0:4])*60*60*24*30*12 \
                  + int(in_time[4:6])*60*60*24*30 \
                  + int(in_time[6:8])*60*60*24 \
                  + int(in_time[8:10])*60*60 \
                  + int(in_time[10:12])*60 \
                  + int(in_time[12:])
        return in_time

    @staticmethod
    def change_to_shorter_string(string_text, max_char=10):
        if len(string_text) > max_char + 3:
            string_text = string_text[0:max_char] + '...'
        return string_text

    #: ############################
    #: Commands for popup buttons #
    #: ############################

    def command_save_config(self, my_text, my_parent):
        my_dict = {}

        try:
            my_list = my_text.split('\n')

            for line in my_list:
                if not line == "":
                    my_key, my_value = line.split("=", 1)
                    my_dict[my_key] = my_value

            self.myConfig = self.configObject.force_set_my_conf_dict(my_dict)
            self.configObject.save_my_conf_dict()
            self.command_reload_tabs()
            self.debug(f'saved and loaded {self.myConfig}')
            self.my_user = self.myConfig['MY_USER']
            self.dbObject = AllAboutDatabase(self.myConfig['DB_NAME'], self.sqlCreateMainTable, self.myConfig['TABLE'],
                                             my_debug=myDebug)
        except ValueError as e:
            text = f'ERROR: {e}\n' +\
                   f'HINT: check for missing "="'
            self.debug(text)
            self.warning_popup(text, my_parent)

    def command_save_todo(self, todo_task_dict, title='', notes='', checked='', trashed='', task="insert"):
        update_array = []
        notes = self.change_quotes_in_text('write', notes)

        if task == 'insert':
            #: insert into DB new task
            todo_task_dict = {'time_created': str(GetCurrentDatetime().get_compact_datetime()),
                              'time_last_changed': str(GetCurrentDatetime().get_compact_datetime()),
                              'checked': checked,
                              'title': title,
                              'notes': notes,
                              'trashed': trashed,
                              'user': self.myConfig['MY_USER']}

            update_array.append(todo_task_dict)
            self.dbObject.insert_into_table(update_array)

        elif task == 'update':
            #: update task in DB
            todo_task_dict['time_last_changed'] = GetCurrentDatetime().get_compact_datetime()
            if checked and checked == '1':
                todo_task_dict['checked'] = str(1)
            elif checked and checked == '0':
                todo_task_dict['checked'] = str(0)
            todo_task_dict['title'] = title if title else todo_task_dict['title']
            todo_task_dict['notes'] = notes if notes else todo_task_dict['notes']
            if trashed and trashed == '1':
                todo_task_dict['trashed'] = str(1)
            elif trashed and trashed == '0':
                todo_task_dict['trashed'] = str(0)

            update_array.append(todo_task_dict)
            self.debug(f'Dict to update: {str(todo_task_dict)}')
            self.dbObject.update_lines_in_table(update_array)

        #: will reload tabs
        self.command_reload_tabs()

    #: ###########
    #: Gui parts #
    #: ###########

    def create_todo_frame(self, parent, todo_task_dict):
        #: object_todo_task < list of objects that represents to do task
        #: Frame
        object_todo_task = {'containing_frame': tk.Frame(parent, relief=tk.SUNKEN, borderwidth=1)}

        #: variable for check box "Done"
        var_done = tk.IntVar(value=1 if todo_task_dict['checked'] == '1' else 0)
        #: Check button
        object_todo_task['done_checkbutton'] = \
            tk.Checkbutton(object_todo_task['containing_frame'], text='Done', onvalue=1, offvalue=0, var=var_done,
                           command=lambda: [self.debug(f'pressing Checkbox at {todo_task_dict["time_last_changed"]}, ' +
                                                       f'checked status: {var_done.get()}'),
                                            self.command_save_todo(todo_task_dict,
                                                                   checked=str(var_done.get()),
                                                                   task='update')
                                            ])

        #: Label with Title of task
        title_label_width = 46
        object_todo_task['title_label'] = tk.Label(object_todo_task['containing_frame'],
                                                   anchor='w', width=title_label_width,
                                                   font=("Courier", 10),
                                                   text=self.change_to_shorter_string(todo_task_dict['title'], 42))
        #: Label with date of last change
        object_todo_task['time_label'] = tk.Label(object_todo_task['containing_frame'],
                                                  text=self.change_time_to_readable(todo_task_dict['time_last_changed'])
                                                  )
        #: edit button for to do task
        object_todo_task['edit_button'] = \
            tk.Button(object_todo_task['containing_frame'], text='EDIT', fg='black',
                      command=lambda: [self.debug(f'EDIT Button pressed in ToDo frame' +
                                                  f'text: {todo_task_dict["time_created"]}'),
                                       self.edit_popup(False, todo_task_dict['user'], todo_task_dict)
                                       ])
        #: packing to do task frame
        object_todo_task['containing_frame'].pack(side="top", fill="both", padx=5, pady=5)
        object_todo_task['done_checkbutton'].pack(side="left")
        object_todo_task['title_label'].pack(side="left", fill="both", padx=10, pady=5)
        object_todo_task['edit_button'].pack(side="right")
        object_todo_task['time_label'].pack(side="right", fill="both", padx=5, pady=5)

        return object_todo_task.copy()

    def create_tabs(self):
        self.tabs = {'tab_parent': ttk.Notebook(self.parent)}

        #: Active to do tab
        self.tabs['tab_active'] = ttk.Frame(self.tabs['tab_parent'], relief=tk.SUNKEN, borderwidth=1)
        self.tabs['tab_parent'].add(self.tabs['tab_active'], text="Active", state="normal")

        #: Done to do tab
        self.tabs['tab_done'] = ttk.Frame(self.tabs['tab_parent'], relief=tk.SUNKEN, borderwidth=1)
        self.tabs['tab_parent'].add(self.tabs['tab_done'], text="Done", state="normal")

        #: checks if Trash tab should be visible
        if self.myConfig['TRASH'] == 'True':
            self.tabs['tab_trash'] = ttk.Frame(self.tabs['tab_parent'], relief=tk.SUNKEN, borderwidth=1)
            self.tabs['tab_parent'].add(self.tabs['tab_trash'], text="Trash", state="normal")

        self.tabs['tab_parent'].pack(expand=1, fill="both")

        self.tabs['canvas_active'] = tk.Canvas(self.tabs['tab_active'])
        self.tabs['canvas_done'] = tk.Canvas(self.tabs['tab_done'])
        self.tabs['canvas_trash'] = tk.Canvas(self.tabs['tab_trash'])

        self.tabs['scrollbar_active'] = ttk.Scrollbar(self.tabs['tab_active'], orient="vertical",
                                                      command=self.tabs['canvas_active'].yview)
        self.tabs['scrollbar_done'] = ttk.Scrollbar(self.tabs['tab_done'], orient="vertical",
                                                    command=self.tabs['canvas_done'].yview)
        self.tabs['scrollbar_trash'] = ttk.Scrollbar(self.tabs['tab_trash'], orient="vertical",
                                                     command=self.tabs['canvas_trash'].yview)

        self.tabs['scrollable_frame_active'] = tk.Frame(self.tabs['canvas_active'])
        self.tabs['scrollable_frame_done'] = tk.Frame(self.tabs['canvas_done'])
        self.tabs['scrollable_frame_trash'] = tk.Frame(self.tabs['canvas_trash'])

        self.tabs['scrollable_frame_active'].pack(side="right", fill="both", expand=True)

        self.tabs['scrollable_frame_active'].bind(
            "<Configure>",
            lambda e: self.tabs['canvas_active'].configure(
                scrollregion=self.tabs['canvas_active'].bbox("all")
            )
        )

        self.tabs['scrollable_frame_done'].bind(
            "<Configure>",
            lambda e: self.tabs['canvas_done'].configure(
                scrollregion=self.tabs['canvas_done'].bbox("all")
            )
        )

        self.tabs['scrollable_frame_trash'].bind(
            "<Configure>",
            lambda e: self.tabs['canvas_trash'].configure(
                scrollregion=self.tabs['canvas_trash'].bbox("all")
            )
        )

        self.tabs['canvas_active'].create_window((0, 0), window=self.tabs['scrollable_frame_active'], anchor="nw",
                                                 width=680)
        self.tabs['canvas_done'].create_window((0, 0), window=self.tabs['scrollable_frame_done'], anchor="nw",
                                               width=680)
        self.tabs['canvas_trash'].create_window((0, 0), window=self.tabs['scrollable_frame_trash'], anchor="nw",
                                                width=680)

        self.tabs['canvas_active'].configure(yscrollcommand=self.tabs['scrollbar_active'].set)
        self.tabs['canvas_done'].configure(yscrollcommand=self.tabs['scrollbar_done'].set)
        self.tabs['canvas_trash'].configure(yscrollcommand=self.tabs['scrollbar_trash'].set)

        #: sorting rows from DB
        todo_active = []
        todo_done = []
        todo_trash = []
        if self.myConfig['TODO_SORTING_NEW_TO_OLD'].lower() == 'true':
            todo_tasks = sorted(self.dbObject.print_table(), key=lambda td: td['time_last_changed'], reverse=True)
        else:
            todo_tasks = sorted(self.dbObject.print_table(), key=lambda td: td['time_last_changed'])

        #: create frames for each to_do task based on lists: todo_active, todo_done, todo_trash
        for todos in todo_tasks:
            if todos['user'] == self.myConfig['MY_USER']:
                if todos['trashed'] == '1':
                    self.debug(f'trashed row: {todos}')
                    if self.myConfig['TRASH'] != 'False':
                        todo_trash.append(self.create_todo_frame(self.tabs['scrollable_frame_trash'], todos))
                    continue
                if todos['checked'] == '1':
                    self.debug(f'checked row: {todos}')
                    todo_done.append(self.create_todo_frame(self.tabs['scrollable_frame_done'], todos))
                    continue
                self.debug(f'active row: {todos}')
                todo_active.append(self.create_todo_frame(self.tabs['scrollable_frame_active'], todos))

        self.tabs['scrollbar_active'].pack(side="right", fill="y")
        self.tabs['scrollbar_done'].pack(side="right", fill="y")
        self.tabs['scrollbar_trash'].pack(side="right", fill="y")

        self.tabs['canvas_active'].pack(side="right", fill="both", expand=True)
        self.tabs['canvas_done'].pack(side="right", fill="both", expand=True)
        self.tabs['canvas_trash'].pack(side="right", fill="both", expand=True)

    #: ################
    #: POP-UP Windows #
    #: ################
    def warning_popup(self, text, my_parent):
        #: pop-up variables
        title_text = "Configuration"
        resize = False

        #: creating  pop up window
        self.debug(f'Config file: {self.myConfFileNameWithPath}')
        config_window = tk.Toplevel()
        config_window.wm_title(f'{title_text}')
        config_window.resizable(width=resize, height=resize)
        config_window.geometry(f'+{my_parent.winfo_x()+50}+{my_parent.winfo_y()+50}')

        #: Frames
        frame = tk.Frame(config_window, relief=tk.SUNKEN, borderwidth=2)
        label = tk.Label(frame, text=text)
        frame.pack(side="top", fill="both", padx=5, pady=5)
        label.pack(side="top", fill="both", padx=5, pady=5)

    def config_popup(self):
        #: pop-up variables
        title_text = 'Configuration'
        window_size = f'600x300+{self.parent.winfo_x()+50}+{self.parent.winfo_y()+50}'
        resize = False

        #: creating  pop up window
        self.debug(f'Config file: {self.myConfFileNameWithPath}')
        config_window = tk.Toplevel()
        config_window.wm_title(f'{title_text}')
        config_window.geometry(f'{window_size}')
        config_window.resizable(width=resize, height=resize)

        #: Frames
        frame_top = tk.Frame(config_window, relief=tk.SUNKEN, borderwidth=2)
        frame_bottom = tk.Frame(config_window)

        #: pack Frame
        frame_top.pack(side="top", fill="both", padx=5, pady=5)
        frame_bottom.pack(side="bottom", fill="x", padx=5, pady=5)

        #: text_box + scrollbar on frame_top
        frame_text = tk.Frame(config_window)
        frame_text.pack(side="top", fill="both", padx=5, pady=5)

        vbar = ttk.Scrollbar(frame_text, orient=tk.VERTICAL)
        vbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame_text, wrap=tk.WORD, undo=True, yscrollcommand=vbar.set)
        with open(self.myConfFileNameWithPath, 'r') as f:
            text_widget.insert(tk.INSERT, f.read())
        f.close()
        text_widget.pack(side="right")

        vbar.config(command=text_widget.yview)

        #: SAVE and CLOSE buttons on frame_bottom
        close_button = tk.Button(frame_bottom, text='CLOSE', fg='red',
                                 command=lambda: [self.debug(f'CLOSE Button pressed in {title_text} popup'),
                                                  config_window.destroy()
                                                  ])
        close_button.pack(side="right")
        save_button = tk.Button(frame_bottom, text='SAVE', fg='black',
                                command=lambda: [self.debug(f'SAVE Button pressed in {title_text} popup'),
                                                 self.command_save_config(text_widget.get("1.0", "end"), config_window)
                                                 ])
        save_button.pack(side="left")

    def edit_popup(self, new, my_user, todo_task_dict):
        #: pop-up variables
        if new:
            title_text = 'Add new ToDo task'
            task = 'insert'

            #: check_buttons variables
            var_done = tk.IntVar(value=0)
            var_trash = tk.IntVar(value=0)
        else:
            title_text = 'Edit ToDo task'
            task = 'update'

            #: check_buttons variables
            var_done = tk.IntVar(value=1 if todo_task_dict['checked'] == '1' else 0)
            var_trash = tk.IntVar(value=1 if todo_task_dict['trashed'] == '1' else 0)

        window_size = f'600x300+{self.parent.winfo_x() + 50}+{self.parent.winfo_y() + 50}'
        resize = False

        #: creating  pop up window
        self.debug(f'Config file: {self.myConfFileNameWithPath}')
        config_window = tk.Toplevel()
        config_window.wm_title(f'{title_text}')
        config_window.geometry(f'{window_size}')
        config_window.resizable(width=resize, height=resize)

        #: User
        user_label = tk.Label(config_window, text=f'USER: {my_user}')
        user_label.pack(side="top", fill="both", padx=2, pady=2)

        #: Frames
        frame_top = tk.Frame(config_window, relief=tk.SUNKEN, borderwidth=2)
        frame_bottom = tk.Frame(config_window)

        #: pack Frame
        frame_top.pack(side="top", expand=1, fill="both", padx=5, pady=5)
        frame_bottom.pack(side="bottom", fill="x", padx=5, pady=5)

        #: Label + entry (top)
        entry_frame = tk.Frame(frame_top)
        entry_frame.pack(side="top", fill="x", padx=5, pady=5)
        entry_label = tk.Label(entry_frame, text="Title: ")
        entry_label.pack(side="left")
        entry_box = tk.Entry(entry_frame, font=30)
        if task == 'update':
            entry_box.insert(0, todo_task_dict['title'])
        entry_box.pack(side="left", fill="x", expand=True)

        #: text_box + scrollbar on frame_text (middle)
        frame_text = tk.Frame(config_window)
        frame_text.pack(side="top", fill="both", padx=5, pady=5)

        vbar = ttk.Scrollbar(frame_text, orient=tk.VERTICAL)
        vbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame_text, wrap=tk.WORD, undo=True, yscrollcommand=vbar.set)
        if task == 'update':
            my_text = self.change_quotes_in_text('read', todo_task_dict['notes'])
            text_widget.insert(1.0, my_text)
        text_widget.pack(side="right")

        vbar.config(command=text_widget.yview)

        #: Edit + Close buttons (bottom)
        close_button = tk.Button(frame_bottom, text='CLOSE', fg='red',
                                 command=lambda: [self.debug(f'CLOSE Button pressed in {title_text} popup'),
                                                  config_window.destroy()
                                                  ])
        close_button.pack(side="right")

        save_button = tk.Button(frame_bottom, text='SAVE', fg='black',
                                command=lambda: [self.command_save_todo(todo_task_dict=todo_task_dict,
                                                                        title=entry_box.get(),
                                                                        notes=text_widget.get("1.0", "end"),
                                                                        checked=str(var_done.get()),
                                                                        trashed=str(var_trash.get()),
                                                                        task=task),
                                                 self.debug(f'SAVE Button pressed in {title_text} popup, TO DO: ' +
                                                            f'{str(todo_task_dict)} ')
                                                 ])
        save_button.pack(side="right", padx=10)

        #: check_buttons DONE
        done_checkbutton_popup = \
            tk.Checkbutton(frame_bottom, text='Done', onvalue=1, offvalue=0, var=var_done,
                           command=lambda: [self.debug(f'pressing DONE Checkbox at {task}, ' +
                                                       f'Checked? {var_done.get()}, Trashed? {var_trash.get()}')
                                            ])
        done_checkbutton_popup.pack(side="left")

        #: check_buttons TRASH
        trash_checkbutton_popup = \
            tk.Checkbutton(frame_bottom, text='Trash', onvalue=1, offvalue=0, var=var_trash,
                           command=lambda: [self.debug(f'pressing TRASH Checkbox at {task}, ' +
                                                       f'Checked? {var_done.get()}, Trashed? {var_trash.get()}')
                                            ])

        trash_checkbutton_popup.pack(side="left", padx=10)


#: #############
#: DEFINITIONS #
#: #############

#: ######
#: BODY #
#: ######


if __name__ == '__main__':
    myDebug = True

    #: default Values for Config
    myDefaultConfDict = {
        'DB_NAME': 'ToDo.db',
        'MY_USER': 'Default',
        'TRASH': 'True',
        'KEEP_TRASH': 'D30',
        'TABLE': 'main',
        'TODO_SORTING_NEW_TO_OLD': 'True'
    }

    #: load config
    myScriptPath = dirname(argv[0])
    myConfName = "ToDoConfig.cfg"
    myConf = myScriptPath + "/" + myConfName
    configObject = ConfigClass(myDefaultConfDict, my_conf=myConf)

    #: table name where things are stored
    tableName = "main"
    #: sql if there is need to create database
    sqlCreateMainTable = f""" CREATE TABLE IF NOT EXISTS {tableName} ( 
                                time_created integer PRIMARY KEY,
                                time_last_changed integer NOT NULL,
                                checked integer NOT NULL,
                                title text NOT NULL,
                                notes text,
                                trashed integer NOT NULL,
                                user text NOT NULL) """

    root = Tk()
    my_gui = MyGui(root, config_object=configObject, sql_create_main_table=sqlCreateMainTable, my_debug=myDebug)

    root.mainloop()
