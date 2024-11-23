# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SHARED INFO:
#
# This library has the purpose to automatize the combined use of
#   tts_media_utils and play_media_utils library in a separate thread.
#   It prevents the Streamlabs Chatbot main thread to be stuck in case
#       such named library would make a timeout issue.
#
# Note:
#    if you wanna further customize this library, 
#        rename the file like "manage_media_<ScriptName>_<version>.py"
#        or you'll risk conflicts with namesake libraries
#        possibly used by other scripts.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CHANGELOG:
#
# Versions:
#   2022/11/20 v1.0 - First public release
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import clr
import time
import threading
from urlparse import urlparse

# Required to download the audio files
clr.AddReference("System.Web")
from System.Web import HttpUtility
from System.Net import WebClient

from tts_media_utils_101 import MediaDownloader, run_cmd
from play_media_utils_101 import MediaPlayer

# Define Global Variables
global Parent

_defaults = {
    # "script": cannot have a default, must be explicit
    "timeout": 30
    # "MEDIA_DWNL": cannot have a default, must be explicit instance of
    #                   Media_Downloader or its configuraton dict
    # "MEDIA_PLAY": cannot have a default, must be explicit instance of
    #                   Media_Player or its configuraton dict
}


class MediaManager:
    def __init__(self, settings):
        global Parent

        Parent = get_parent()

        self._texts = []
        self._audios = []
        self._valid = True
        self._thread = None

        self.__settings = self.__settings_check(settings)

        self.MEDIA_DWNL = None
        self.MEDIA_PLAY = None

        if self._valid:
            self.MEDIA_DWNL = self.__settings["MEDIA_DWNL"]
            self.MEDIA_PLAY = self.__settings["MEDIA_PLAY"]
            self.__start()


    # standard checks on settings voices
    # returns settings with checked voices
    def __settings_check(self, settings):
        settings = self.__check_defaults(settings)

        settings["timeout"] = int(self._float_check(settings["timeout"], 30))

        if "MEDIA_DWNL" not in settings or not settings["MEDIA_DWNL"]:
            self._valid = False
            Parent.Log(settings["script"],
                "ttsXplay init: MEDIA_DWNL is not valid")
        else:
            DWNL_SET = settings["MEDIA_DWNL"]
            if not isinstance(DWNL_SET, MediaDownloader):
                if not isinstance(DWNL_SET, dict):
                    Parent.Log(settings["script"],
                        "ttsXplay init: MEDIA_DWNL is not valid")
                else:
                    settings["MEDIA_DWNL"] = MediaDownloader(DWNL_SET)

        if "MEDIA_PLAY" not in settings or not settings["MEDIA_PLAY"]:
            self._valid = False
            Parent.Log(settings["script"],
                "ttsXplay init: MEDIA_PLAY is not valid")
        else:
            PLAY_SET = settings["MEDIA_PLAY"]
            if not isinstance(PLAY_SET, MediaPlayer):
                if not isinstance(PLAY_SET, dict):
                    Parent.Log(settings["script"],
                        "ttsXplay init: MEDIA_PLAY is not valid")
                else:
                    settings["MEDIA_PLAY"] = MediaPlayer(PLAY_SET)

        return settings


    # if a setting isn't found in setting, it will be added with a
    #   default value
    # returns settings with checked voices
    def __check_defaults(self, settings):
        for set in _defaults:
            if not set in settings:
                settings[set] = _defaults[set]
        return settings


    # check if the value could be a valid float, and return it casted
    #   to float
    # if not, returns the given default
    def _float_check(self, value, default):
        try:
            return float(value)
        except:
            return default


    # start thread
    def __start(self):
        if self._valid and (
                            not self._thread
                            or not isinstance(self._thread, threading.Thread)
                            or not self._thread.is_alive()
                            ):
            self._close = False
            self._thread = threading.Thread(
                target = self._download_and_play_async)
            self._thread.start()
        return


    # close thread
    def close(self):
        if self.MEDIA_DWNL:
            self.MEDIA_DWNL.close()

        if self.MEDIA_PLAY:
            self.MEDIA_PLAY.close()

        try:
            if not self._close:
                self._close = True

                if self._thread and self._thread.is_alive():
                    self._thread.join()

        except AttributeError as e:
            self._close = True

        timeout = self.__settings["timeout"]
        loop_start = time.time()

        while self._thread and self._thread.is_alive():
            if (time.time() - loop_start) > timeout:
                break
            self._close = True
            time.sleep(0.05)

        return


    # thread which will use tts_media_utils to generates TTS from text
    # and play_media_utils to play TTS from requests appended to queue
    def _download_and_play_async(self):
        try:
            while True:
                if self._close:
                    break

                if self._texts:
                    text = self._texts.pop(0)

                    try:
                        if self._close:
                            break

                        if text:
                            if self.MEDIA_DWNL:
                                text = self.MEDIA_DWNL.append(text)
                                path = self.MEDIA_DWNL.get_now(text)
                            else:
                                Parent.Log(settings["script"],
                                    "ttsXplay generate TTS: MEDIA_DWNL"\
                                    " is not valid")

                        if self._close:
                            self.MEDIA_DWNL.clean(path)
                            break

                    except Exception as e:
                        Parent.Log(self.__settings["script"],
                            "ttsXplay generate TTS: Error generating TTS"\
                            " file > " + str(e))

                    else:
                        try:
                            if self._close:
                                break

                            if path:
                                if self.MEDIA_PLAY:
                                    self.MEDIA_PLAY.append_play_clean(path,
                                                                    text)
                                else:
                                    Parent.Log(settings["script"],
                                        "ttsXplay play TTS: MEDIA_PLAY"\
                                        " is not valid")

                            if self._close:
                                break

                        except Exception as e:
                            Parent.Log(self.__settings["script"],
                                "ttsXplay play TTS: Error playing TTS file > "
                                + str(e))

                time.sleep(0.150)

        except Exception as e:
            Parent.Log(self.__settings["script"],
                "ttsXplay loop: Error gathering info for text > " + str(e))
        return


    # append text to generate and play TTS
    #   tts_media_utils usually cuts to 200 chars max and applies chars
    #   replacements by setup
    # returns a preview of the new reference text, eventually cut to
    #   usually 200 chars max and with replaced chars
    def append(self, text):

        if self._valid and self.MEDIA_PLAY and self.MEDIA_DWNL:
            self._texts.append(text)
            return self.MEDIA_DWNL.getRefText(text)

        # if ttsXplay_media_utils was invalid at initalization
        Parent.Log(self.__settings["script"],
            "ttsXplay append: This Media_Manager is not valid.")
        return "invalid for " + text


import System
clr.AddReference([
        asbly for asbly in System.AppDomain.CurrentDomain.GetAssemblies()
        if "AnkhBotR2" in str(asbly)
    ][0])


import AnkhBotR2
def get_parent():
    return AnkhBotR2.Managers.PythonManager()
