from os.path import isfile
import sqlite3
from sqlite3 import Error

#: Methods: insert_into_table([{},{}]), remove_lines_in_table([str(), str()]), update_lines_in_table([{},{}])
#: Methods: print_table(str('where column="string"/int')) or print_table()


class AllAboutDatabase:
    def __init__(self, db_name, sql_create_table, table_name="main", my_debug=False):
        self.myDebug = my_debug
        self.clsDict = {'dbName': db_name, 'tableName': table_name, 'createTableSQL': sql_create_table}
        self.conn = None

        if not self.check_db_file_exist():
            self.create_table()
        else:
            self.create_table()

    def debug(self, text='Undefined text'):
        if self.myDebug:
            print(f'DEBUG INFO: {text}')

    def check_db_file_exist(self):
        if isfile(self.clsDict['dbName']):
            self.debug(f'{self.clsDict["dbName"]}: if file')
            return True
        else:
            self.debug(f'{self.clsDict["dbName"]}: doesnt exist')
            return False

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.clsDict['dbName'])
            self.debug(f'{self.clsDict["dbName"]}: connection opened')
        except Error as e:
            self.debug(f'ERROR: {e}; ')

    def close_connection(self):
        self.conn.close()
        self.debug(f'{self.clsDict["dbName"]}: connection closed')

    def create_table(self, sql_create_table=""):
        if not sql_create_table:
            sql_create_table = self.clsDict['createTableSQL']

        self.debug(f'Using {sql_create_table}: to create Table')

        try:
            self.open_connection()
            c = self.conn.cursor()
            c.execute(sql_create_table)
            self.close_connection()
            return True
        except Error as e:
            self.debug(f'ERROR: {e}; ')
            return False

    def get_table_name(self):
        return self.clsDict['tableName']

    def get_db_name(self):
        return self.clsDict['dbName']

    def table_to_listdict(self, my_input):
        my_list_out = []
        tmp_dict = {}

        for my_list in my_input:
            tmp_dict.clear()

            tmp_dict['time_created'] = str(my_list[0])
            tmp_dict['time_last_changed'] = str(my_list[1])
            tmp_dict['checked'] = str(my_list[2])
            tmp_dict['title'] = my_list[3].strip("'")
            tmp_dict['notes'] = str(my_list[4]).strip("'")
            tmp_dict['trashed'] = str(my_list[5])
            tmp_dict['user'] = my_list[6].strip("'")

            self.debug(f'Tuple: {my_list}')
            self.debug(f'Dictionary: {tmp_dict}')

            my_list_out.append(tmp_dict.copy())

        return my_list_out

    def print_table(self, where=''):
        self.debug(f'using table {self.clsDict["tableName"]} {where}')

        self.open_connection()
        c = self.conn.cursor()
        c.execute(f'SELECT * from {self.clsDict["tableName"]} {where}')
        table = c.fetchall()
        self.debug(f'output from DB: {table}')
        self.close_connection()

        my_output = self.table_to_listdict(table)

        return my_output

    def insert_into_table(self, my_input_data=()):
        self.open_connection()
        c = self.conn.cursor()

        for item in my_input_data:
            my_row = f'{item["time_created"]},{item["time_last_changed"]},{item["checked"]},"{item["title"]}",' + \
                     f'"{item["notes"]}",{item["trashed"]},"{item["user"]}"'
            insert_into = f'INSERT INTO {self.clsDict["tableName"]} VALUES({my_row})'

            self.debug(f'inserting line: {insert_into}')

            try:
                self.debug(f'inserting line: {my_row}')
                c.execute(insert_into)
                self.conn.commit()
            except sqlite3.IntegrityError as e:
                self.debug(f'ERROR: {e}; ')
                return str(e)
            except sqlite3.OperationalError as e:
                self.debug(f'ERROR: {e}; ' +
                           f'HINT: see, if table exist, or create DB from scratch')
                return str(e)

        self.close_connection()
        return "OK"

    def remove_lines_in_table(self, my_ids=()):
        self.open_connection()
        c = self.conn.cursor()

        for my_id in my_ids:
            try:
                c.execute(f'DELETE FROM {self.clsDict["tableName"]} WHERE time_created = {my_id}')
                self.debug(f'Removing from TABLE: {self.clsDict["tableName"]}, by ID: {my_id}')
                self.conn.commit()
            except sqlite3.IntegrityError as e:
                self.debug(f'ERROR: {e}; ')

        self.close_connection()

    def update_lines_in_table(self, my_input_data=()):
        self.open_connection()
        c = self.conn.cursor()

        for line in my_input_data:
            my_id = line['time_created']
            update = f'time_last_changed={line["time_last_changed"]}, checked={line["checked"]}, ' + \
                     f'title="{line["title"]}", notes="{line["notes"]}", trashed={line["trashed"]}, ' + \
                     f'user="{line["user"]}"'

            update_into = f'UPDATE {self.clsDict["tableName"]} SET  {update} WHERE time_created = {my_id} '

            self.debug(f'inserting line: {update_into}')

            try:
                c.execute(update_into)
                self.debug(f'updating TABLE: {self.clsDict["tableName"]}, by ID: {my_id}, DATA: {update}')
                self.conn.commit()
            except sqlite3.IntegrityError as e:
                self.debug(f'ERROR: {e}; ')

        self.close_connection()
