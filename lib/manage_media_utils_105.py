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
#   2022/11/27 v1.01 - Allows to force read lowercased or uppercased
#   2023/01/15 v1.02 - Added a pause method (in tts library)
#   2023/01/24 av1.03 - Added setting to keep or not queing on pause
#   2023/01/27 av1.04 - Adopts scripts utils library
#   2023/02/01 av1.05 -
#       Flag to preview textually in chat the reading text
#               if you use "append" method
#       Possibility to choose a specific language for the TTS reader
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

from tts_media_utils_106 import MediaDownloader
from play_media_utils_105 import MediaPlayer
from scripts_utils_101 import *


# Define Global Variables
global Parent

_defaults = {
    # "script": cannot have a default, must be explicit
    "timeout": 30,
    "preview": False,
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
        self._keep = self.__settings["keep"]

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

        settings["timeout"] = int(float_check(settings["timeout"], 30))
        settings["preview"] = check_false(settings["preview"])

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


    # start thread
    def __start(self):
        if self._valid and (
                            not self._thread
                            or not isinstance(self._thread, threading.Thread)
                            or not self._thread.is_alive()
                            ):
            self._close = False
            self._paused = False
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


    # pause\unpause queue querying
    def pause(self):
        self.set_paused(not self._paused)
        return self._paused


    # set paused or unpaused queue querying
    def set_paused(self, paused):
        self._paused = paused

        if self.MEDIA_DWNL:
            self.MEDIA_DWNL.set_paused(paused)

        if self.MEDIA_PLAY:
            self.MEDIA_PLAY.set_paused(paused)

        return self._paused


    # get the pause status of queue querying
    def is_paused(self):
        return self._paused


    # keep\unkeep queuing on pause
    def keep(self):
        self.set_keep_queuing(not self._keep)
        return self._keep


    # set keep or unkeep queuing on pause
    def set_keep_queuing(self, keep):
        self._keep = keep

        if self.MEDIA_DWNL:
            self.MEDIA_DWNL.set_keep_queuing(keep)

        if self.MEDIA_PLAY:
            self.MEDIA_PLAY.set_keep_queuing(keep)

        return self._keep


    # get the keep queuing setting on pause
    def is_keep_queuing(self):
        return self._keep


    # thread which will use tts_media_utils to generates TTS from text
    # and play_media_utils to play TTS from requests appended to queue
    def _download_and_play_async(self):
        try:
            while True:
                if self._close:
                    break

                if self._texts and not self._paused:
                    text_info = self._texts.pop(0)
                    text = text_info[0]
                    preview = text_info[1]
                    lang = text_info[2]

                    if preview is not True and preview is not False:
                        preview = self.__settings["preview"]

                    try:
                        if self._close:
                            break

                        if text:
                            if self.MEDIA_DWNL:
                                text = self.MEDIA_DWNL.append(text, lang = lang)
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
                                    self.MEDIA_PLAY.append_play_clean(
                                                                        path,
                                                                        text,
                                                                        preview
                                                                    )
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
    #   or empty string if nothing was appended
    def append(self, text, preview = None, lang = None):

        if self._valid and self.MEDIA_PLAY and self.MEDIA_DWNL:
            if not self._paused or self._keep:
                self._texts.append([text, preview, lang])
                return self.MEDIA_DWNL.get_ref_text(text)

            else:
                return ""

        # if ttsXplay_media_utils was invalid at initalization
        Parent.Log(self.__settings["script"],
            "ttsXplay append: This Media_Manager is not valid.")
        return "invalid for " + text
