from os.path import dirname
from sys import argv


#: class for handling Config File
class ConfigClass:
    def __init__(self, my_default_conf_dict, my_conf=dirname(argv[0]) + "/config.cfg", my_debug=False):
        self.myDebug = my_debug
        self.clsDict = {'ConfigName': my_conf, 'loadedConfig': {}, 'defaultConfig': my_default_conf_dict}

        #: load Config file into "self.myConfDict" dictionary
        self.clsDict['loadedConfig'] = self.load_my_config(self.clsDict['ConfigName'], self.clsDict['defaultConfig'])

    def debug(self, text='Undefined text'):
        if self.myDebug:
            print(f'DEBUG INFO: {text}')

    def get_my_conf_dict(self):
        return self.clsDict['loadedConfig']

    def get_my_default_conf_dict(self):
        return self.clsDict['defaultConfig']

    def get_my_conf_file_name(self):
        return self.clsDict['ConfigName']

    def force_set_my_conf_dict(self, my_conf_dict):
        self.clsDict['loadedConfig'] = my_conf_dict
        return self.clsDict['loadedConfig']

    def save_my_conf_dict(self, config_name='', my_dict_input=''):
        try:
            if not config_name:
                config_name = self.clsDict['ConfigName']
                self.debug(f'save_my_conf_dict, set "config_name": {config_name}')
            if not my_dict_input:
                my_dict_input = self.clsDict['loadedConfig']
                self.debug(f'save_my_conf_dict, set "my_dict_input": {my_dict_input}')

            my_conf_file = open(config_name, "w")
            for my_key in my_dict_input.keys():
                my_conf_file.write(my_key + "=" + my_dict_input[my_key] + "\n")
            my_conf_file.close()

        except IOError as e:
            self.debug(f'IOError raised in "save_my_conf_dict" method of "ConfigClass" class; ' +
                       f'\n  ERROR: {e}; ' +
                       f'\n  HINT: see if Path you provided exist')
        except TypeError as e:
            self.debug(f'TypeError: raised in "save_my_conf_dict" method of "ConfigClass" class; ' +
                       f'\n  ERROR: {e}; ' +
                       f'\n  HINT: check if what you provided as "my_dict_input" is Dictionary')
        except AttributeError as e:
            self.debug(f'AttributeError: raised in "save_my_conf_dict" method of "ConfigClass" class; ' +
                       f'\n  ERROR: {e}; ' +
                       f'\n  HINT: check if what you provided as "my_dict_input" is Dictionary')

    def load_my_config(self, config_name, default_config_dict):
        try:
            my_conf_file = open(config_name, "r")
            my_conf_dict = {}
            for line in my_conf_file:
                #: continue in next iteration if line is blank
                if line == "":
                    continue
                #: continue if there is only whitespace characters in line
                if line.isspace():
                    continue

                #: get myKey and myValue from line and add it into "myConfDict"
                my_key, my_value = line.rstrip().split("=", 1)
                my_conf_dict[my_key] = my_value
                self.debug(f'key:{my_key}, value:{my_conf_dict[my_key]}')

            #: close file after parsing through file
            my_conf_file.close()

            #: if by chance some keys=value are missing, load them from default
            for my_default_key in default_config_dict.keys():
                self.debug(f'default = key:{my_default_key}, value:{default_config_dict[my_default_key]}')

                if my_default_key not in my_conf_dict.keys():
                    self.clsDict['loadedConfig'][my_default_key] = default_config_dict[my_default_key]
                    self.debug(f'changed to = key:{my_default_key}, value:{my_conf_dict[my_default_key]}')

            return my_conf_dict

        except IOError as e:
            self.debug(f'IOError raised in "load_my_config" method of "ConfigClass" class; ' +
                       f'\n  ERROR: {e}; ' +
                       f'\n  HINT: see if Path you provided exist')
            my_conf_file = open(self.clsDict['ConfigName'], "a")
            for item in default_config_dict.keys():
                my_conf_file.write(item + "=" + default_config_dict[item] + "\n")
            my_conf_file.close()

            #: load default if config do not exist
            return default_config_dict


if __name__ == '__main__':
    myDebug = True

    myDefaultConfDict = {
        'DB_NAME': 'ToDo.db',
        'MY_USER': 'Default',
        'TRASH': 'True'
    }
    path = '/home/wollwo/Projects/Python3/Pycharm/ToDoApp'
    config = path + '/config.cfg'

    confObject = ConfigClass(myDefaultConfDict, config, myDebug)
