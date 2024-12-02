# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SHARED INFO:
#
# Reworked for use in different scripts, by Patcha (2022)
#
# Just took ispiration from an old script I use as base from 2017
# Did some rework to ensure it works with every script, somehow
#
# Note:
#    if you wanna further customize this library, 
#        rename the file like "settings_<ScriptName>_<version>.py"
#        or you'll risk conflicts with namesake libraries
#        possibly used in other scripts' folder.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CHANGELOG:
#
# Versions:
#   2022/10/15 v1.0 - Initial release as separate library
#   2022/11/20 v1.01 - First public release, not backwards compatible
#   2023/01/27 v1.02 - Exported utility functions into
#                       dedicated new library
#   2023/02/03 v1.03 - Scripts utils library version 1.01
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import codecs
import json

from scripts_utils_101 import get_parent

# Define Global Variables
global Parent


class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    # settingsFile is a json file path, defaults is a dictionary
    def __init__(self, settingsFile = None, defaults = None):
        global Parent

        Parent = get_parent()
        self._defaults = None

        # set variables from settings file
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(
                                settingsFile,
                                encoding='utf-8-sig',
                                mode='r'
                            ) as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 

        # initialize missing variables to defaults,
        #   if no settings file or incomplete data
        self.defaults(defaults)


    # if a setting isn't found in __dict__,
    #   it will be added with a default value
    def defaults(self, defaults = None):
        # if defaul is set, store as his own
        if defaults:
            self._defaults = defaults
        # otherwise, try to use his own if any
        else:
            defaults = _defaults

        # could still be no defaults set, but if any,
        #   will be used to complete settings
        if defaults:
            for setting in defaults:
                if not setting in self.__dict__:
                    self.__dict__[setting] = defaults[setting]

        return


    # Reload settings on save through UI
    def ReloadSettings(self, data, defaults = None):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

        # if incomplete data, set missing variables to defaults if any
        self.defaults(defaults)

        return


    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):

        with codecs.open(
                            settingsFile,
                            encoding='utf-8-sig',
                            mode='w+'
                        ) as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')

        with codecs.open(
                            settingsFile.replace("json", "js"),
                            encoding='utf-8-sig',
                            mode='w+'
                        ) as f:
            f.write("var settings = {0};".format(
                                                json.dumps(
                                                    self.__dict__,
                                                    encoding='utf-8-sig')
                                                )
                    )

        return
