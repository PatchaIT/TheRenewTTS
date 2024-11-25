# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SHARED INFO:
#
# Original a subclass for TheNewTTS script for Streamlabs Chatbot
# Copyright (C) 2020 Luis Sanchez
# Extracted as library by Patcha (2022)
#
# Note:
#    if you wanna further customize this library, 
#        rename the file like "blacklist_<ScriptName>_<version>.py"
#        or you'll risk conflicts with namesake libraries
#        possibly used by other scripts.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CHANGELOG:
#
# Versions:
#   2022/11/20 v1.0 - Extracted from Luis Sanchez's TheNewTTS script
#                       (extraction by Patcha)
#   2023/01/24 v1.01 - Fixed a bug with lowercasing loaded data
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import clr
import json
import codecs


class Blacklist:
    def __init__(self, file_path):
        global Parent
        Parent = get_parent()

        self._path = file_path
        self._normalize()

        self._db = self._load()


    def add_user(self, user_name):
        user_name = Blacklist.strip_username(user_name)
        if self.is_user_blacklisted(user_name):
            return False

        self._db.append(user_name)
        self._save(self._db)

        return True


    def remove_user(self, user_name):
        user_name = Blacklist.strip_username(user_name)
        if not self.is_user_blacklisted(user_name):
            return False

        self._db.remove(user_name)
        self._save(self._db)

        return True


    def is_user_blacklisted(self, user_name):
        user_name = Blacklist.strip_username(user_name)
        return user_name in self._db


    def _load(self):
        if not os.path.isfile(self._path):
            return []
        with codecs.open(
                            self._path,
                            encoding="utf-8-sig",
                            mode='r'
                        ) as file:
            return json.load(file, encoding="utf-8-sig")


    def _save(self, modified_db):
        with codecs.open(
                            self._path,
                            encoding="utf-8-sig",
                            mode='w'
                        ) as file:
            file.write(json.dumps(modified_db, encoding="utf-8-sig"))
        return


    # lowercases the whole file content
    def _normalize(self):
        db = self._load()
        if db:
            new_db = [value.lower() for value in db]
            self._save(new_db)
        return


    @staticmethod
    def strip_username(user_name):
        user_name = user_name.lower()
        if "@" in user_name:
            user_name = user_name.replace("@","")
        return user_name


import System
clr.AddReference([
        asbly for asbly in System.AppDomain.CurrentDomain.GetAssemblies()
        if "AnkhBotR2" in str(asbly)
    ][0])


import AnkhBotR2
def get_parent():
    return AnkhBotR2.Managers.PythonManager()
