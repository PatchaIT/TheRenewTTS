# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SHARED INFO:
#
# Original library for TheNewTTS script for Streamlabs Chatbot
# Copyright (C) 2020 Luis Sanchez
# Extracted the audio player side only, by Patcha (2022)
#
# Note:
#    if you wanna further customize this library, 
#        rename the file like "play_media_<ScriptName>_<version>.py"
#        or you'll risk conflicts with namesake libraries
#        possibly used by other scripts.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CHANGELOG:
#
# Versions:
# tts_media.py
#   2019/11/12 v1.0 - Initial release (by LuisSanchezDev)
#   2019/11/27 v1.0.1 - Fixed sound not playing (by LuisSanchezDev)
#   2019/03/12 v1.1.0 - Added max length in seconds (by LuisSanchezDev)
#   2020/08/29 v2.0 - Added a skip command (by LuisSanchezDev)
# play_media_utils_xxx.py
#   2022/10/15 av1.0 - Extracted and reengineered the audio player side
#                       (extraction by Patcha)
#                      ["a"lternative "v"ersion; only the audio player]
#   2022/11/20 av1.01 - First public release, not backwards compatible
#   2023/01/15 av1.02 - Added a pause method
#   2023/01/24 av1.03 - Added setting to keep or not keep queing on pause
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import clr
import time
import threading

# Required to play audio files
clr.AddReference("NAudio")
import NAudio
from NAudio.Wave import AudioFileReader, WaveOutEvent, PlaybackState

# Required to run cmd commands without a window and wait for the result
from System.Diagnostics import Process, ProcessStartInfo, ProcessWindowStyle

# Define Global Variables
global Parent

_defaults = {
    # "script": cannot have a default, must be explicit
    "length": 30,
    "timeout": 30
}


class MediaPlayer:
    def __init__(self, settings):
        global Parent

        Parent = get_parent()

        self._audios = []
        self._thread = None
        self._file_path = ""

        self.__settings = self.__settings_check(settings)
        self.__skip = set()
        self.__to_clean = set()
        self._keep = self.__settings["keep"]

        self.__start()


    # standard checks on settings voices
    # returns settings with checked voices
    def __settings_check(self, settings):
        settings = self.__check_defaults(settings)
        settings["length"] = int(self._float_check(settings["length"], 30))
        settings["timeout"] = int(self._float_check(settings["timeout"], 30))
        return settings


    # if a setting isn't found in setting, it will be added with a
    #   default value
    # returns settings with checked voices
    def __check_defaults(self, settings):
        for set in _defaults:
            if not set in settings:
                self.settings[set] = defaults[set]
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
        if (
                not self._thread
                or not isinstance(self._thread, threading.Thread)
                or not self._thread.is_alive()
            ):
            self._close = False
            self._paused = False
            self._thread = threading.Thread(target=self._play_loop)
            self._thread.start()
        return


    # close thread
    def close(self):
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
        return self._keep


    # get the keep queuing setting on pause
    def is_keep_queuing(self):
        return self._keep


    # thread which generates TTS from text appended to queue
    def _play_loop(self):
        try:
            while True:
                if self._close:
                    break

                if self._audios and not self._paused:
                    audio = self._audios.pop(0)
                    self._file_path = audio[0]
                    text = audio[1]

                    try:
                        started_playing = time.time()
                        with AudioFileReader(self._file_path) as reader:
                            with WaveOutEvent() as device:
                                device.Init(reader)
                                device.Play()

                                while device.PlaybackState ==\
                                                    PlaybackState.Playing:
                                    if self._close:
                                        break

                                    if self.__skip:
                                        skip_clone = self.__skip.copy()
                                        if (
                                            "" in skip_clone
                                            or text in skip_clone
                                            or self._file_path in skip_clone
                                            ):
                                            self.__skip.discard("")
                                            self.__skip.discard(text)
                                            break

                                    elapsed = time.time() - started_playing
                                    if elapsed >= self.__settings["length"]:
                                        break

                                    time.sleep(0.1)

                    except Exception as e:
                        Parent.Log(self.__settings["script"],
                            "Error processing audio file > " + str(e))

                    self._file_path = ""

                    # soon after playing audio, or skipping or error:
                    # if there's still any "skip current"
                    #   (__skip with empty text) remove it,
                    #   to not risk to skip next audio instead
                    # anyway if there's a "skip next"
                    #   (__skip with "$$" value in text) will use a
                    #   "skip current" for next audio to be skipped
                    if self.__skip:
                        skip_clone = self.__skip.copy()
                        if "$$" in skip_clone:
                            self.__skip.add("")
                        else:
                            self.__skip.discard("")

                    # after playing an audio, check file paths
                    #   to remove requests queue (__to_clean)
                    #   and execute for files no more in queue and/or
                    #   no more playing
                    self.__clean_queue_executor()

                # if there is no audio left to play:
                #   let's clean __skip list
                #       to not risk to skip future audios
                #   and let's clean __to_clean list too
                else:
                    if self.__skip:
                        self.__skip.clear()
                    if self.__to_clean:
                        self.__to_clean.clear()

                time.sleep(0.150)

        except Exception as e:
            Parent.Log(self.__settings["script"],
                "Error processing audio queue > " + str(e))
        return


    # append audio file with info, to play it as soon as possible
    # returns True if succeeded to append
    #   or False if nothing was appended
    def append(self, file_path, text = None):

        if not self._paused or self._keep:
            self._audios.append([file_path, text if text else None])
            return True

        else:
            return False


    # append audio file with info, to play it as soon as possible
    def append_play_clean(self, file_path, text = None):

        if self.append(file_path, text):
            self.clean(file_path)

        return


    # check if file_path file is queued to be played
    def check(self, file_path):

        for audio in self._audios:
            if audio[0] == file_path:
                return True

        return False


    # return the file_path of the current playing sound
    def current(self):
        return self._file_path


    # return True if current playing sound has given file_path
    def is_current(self, file_path):
        return self.current() == file_path


    # Allows to skip the audio identified by text
    #   text can also be the file path
    # If optional text is empty, it means skip current playing audio
    def skip(self, text = ""):
        self.__skip.add(text)
        return


    # Allows to skip the next audio in queue,
    #   if audio queue is empty, it will skip nothing
    # Be sure the audio before it's not finished already or there'll be
    #   probability it will skip the audio soon after the next, instead
    def skip_next(self):
        self.skip("$$")
        return


    # Allows to skip all queued audio files containing the word into
    #   parameter, comparing with the refernce text passed when
    #   appended
    #   it doesn't apply to audio appended without a reference text
    #   it doesn't apply to audio already playing and no more in queue
    #   if audio queue is empty, it will skip nothing
    def skip_containing(self, filter):

        for audio in self._audios[:]:
            text = audio[1]
            if text and filter and (filter.lower() in text.lower()):
                self._audios.remove(audio)

        return


    # Allows to skip the whole current queue,
    #   included current audio
    def skip_all(self):

        for audio in self._audios[:]:
            self.skip(audio[0])
        self.skip()

        return


    # If file on such path is queued to be played or is playing, this
    #   method will also queue it to be removed (after being played).
    # If such file is not queued to be played or not playing,
    #   does nothing.
    def clean(self, file_path):
        self.__to_clean.add(file_path)
        return


    # This is the actual file remover method,
    #   but have to be called by thread loop
    def __clean_os_file(self, file_path):
        run_cmd('del "{0}"'.format(file_path))
        return


    # This checks and cleans a single file,
    #   not playing and not to be played
    # The list (or tuple) of file to be played is optional,
    #   you can get it with __get_audio_paths
    def __clean_file(self, file_path, audio_paths = tuple()):
        if file_path != self._file_path and file_path not in audio_paths:
            if os.path.isfile(file_path):
                self.__clean_os_file(file_path)
            self.__to_clean.remove(file_path)
        return


    # This is the core code to manage the queue of file_path to be
    #   removed after being played it will be called by thread loop
    # Method created to keep more readable the code itself.
    def __clean_queue_executor(self):
        if self.__to_clean:
            audio_paths = self.__get_audio_paths()
            for file_path in self.__to_clean.copy():
                self.__clean_file(file_path, audio_paths)
        return


    # Returns a tuple with all file paths for files in _audios queue,
    #   if any. Otherwise, an empty tuple.
    def __get_audio_paths(self):
        if self._audios:
            return tuple(zip(*self._audios))[0]
        return tuple()


def run_cmd(command):
    pinfo = ProcessStartInfo()
    pinfo.FileName = "cmd.exe"
    pinfo.WindowStyle = ProcessWindowStyle.Hidden;
    pinfo.Arguments = "/C" + command
    cmd = Process.Start(pinfo)
    cmd.WaitForExit()
    return


import System
clr.AddReference([
        asbly for asbly in System.AppDomain.CurrentDomain.GetAssemblies()
        if "AnkhBotR2" in str(asbly)
    ][0])


import AnkhBotR2
def get_parent():
    return AnkhBotR2.Managers.PythonManager()
