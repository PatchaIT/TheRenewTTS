# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SHARED INFO:
#
# Original library for TheNewTTS script for Streamlabs Chatbot
# Copyright (C) 2020 Luis Sanchez
# Reworked for export to use TTS in other scripts, by Patcha (2022)
#
# Note:
#    if you wanna further customize this library, 
#        rename the file like "tts_media_<ScriptName>_<version>.py"
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
# tts_media_utils_xxx.py
#   2022/10/15 av1.0 - Reengineered to support multiple scripts adopting
#                       this same library at the same time (by Patcha)
#                      ["a"lternative "v"ersion; no internal player
#                       + no "skip"]
#   2022/11/20 av1.01 - First public release, not backwards compatible
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import clr
import time
import threading
import re

# Required to download the audio files
clr.AddReference("System.Web")
from System.Web import HttpUtility
from System.Net import WebClient
from urlparse import urlparse

# Required to run cmd commands without a window and wait for the result
from System.Diagnostics import Process, ProcessStartInfo, ProcessWindowStyle

# Define Global Variables
global Parent

_defaults = {
    # "script": cannot have a default, must be explicit
    "lang": "English (US) [en-US]",
    "volume_on": True,
    "pitch_on": True,
    "speed_on": True,
    "volume": 100,
    "pitch": 100,
    "speed": 100,
    "length": 30,
    "timeout": 30,
    "clean_rep_lett": True,
    "clean_rep_word": True,
    "max_rep_word": 3,
    "alias_list": "",
    "chars_swapping": "",
    "clean_urls": False,
    "replace_urls": "link removed",
    "replaces": "",
    "emote_name_upper": True,
    "emote_prefix": "",
    "cut_max_chars": True,
    "max_chars": 200,
    "params": "",
    "webservice": "",
    "audio_format" : ""
    # "_path": cannot have a default, must be explicit
    # "_cache": cannot have a default, must be explicit
}


class MediaDownloader:
    def __init__(self, settings):
        global Parent

        Parent = get_parent()

        self._texts = []
        self._audios = []
        self._count = 0
        self._thread = None

        self.__settings = self.__settings_check(settings)
        self.__start()


    # standard checks on settings voices
    # returns settings with checked voices
    def __settings_check(self, settings):
        settings = self.__check_defaults(settings)

        settings["lang"] = (
                                re.match(r"^.*\[(.+)\]", settings["lang"])
                                .groups()[0] if settings["lang"] else "en-US"
                            )

        settings["volume"] = self._float_check(settings["volume"], 1.0)
        settings["pitch"] = self._float_check(settings["pitch"], 1.0)
        settings["speed"] = self._float_check(settings["speed"], 1.0)
        settings["length"] = int(self._float_check(settings["length"], 30))
        settings["timeout"] = int(self._float_check(settings["timeout"], 30))

        settings["cut_max_chars"] = self._check_false(
                                        settings["cut_max_chars"])
        settings["max_chars"] = int(self._float_check(settings["max_chars"],
                                        200))
        if settings["max_chars"] > 200:
            settings["max_chars"] = 200

        settings["volume_on"] = self._check_false(settings["volume_on"])
        settings["pitch_on"] = self._check_false(settings["pitch_on"])
        settings["speed_on"] = self._check_false(settings["speed_on"])

        settings["clean_rep_lett"] = self._check_false(
                                        settings["clean_rep_lett"])
        settings["clean_rep_word"] = self._check_false(
                                        settings["clean_rep_word"])
        settings["max_rep_word"] = int(self._float_check(
                                        settings["max_rep_word"], 3))
        settings["alias_list"] = MediaDownloader.parse_alias_list(
                                        settings["alias_list"])
        settings["chars_swapping"] = MediaDownloader.parse_alias_list(
                                        settings["chars_swapping"])
        settings["clean_urls"] = self._check_false(settings["clean_urls"])

        if settings["webservice"]:
            settings["webservice"] = settings["webservice"].strip(" ")
        else:
            settings["webservice"] = (
                "https://translate.google.com/translate_tts?ie=UTF-8&tl={1}" \
                "&client=tw-ob&q={0}"
            )

        settings["audio_format"] = re.sub("\s+", "",
                                    settings["audio_format"]).lower() \
                                        if settings["audio_format"] \
                                        else ".mp3"
        if not settings["audio_format"].startswith("."):
            settings["audio_format"] = "." + settings["audio_format"]

        settings["params"] = self.__params_parser(settings)

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


    # check if the value is trying to be a False boolean, and returns
    #   a real boolean
    # returns True if True or "True"; otherwise False
    def _check_false(self, value):
        return (value == True or
                (isinstance(value, str) and value.lower() == "true")
                )


    # creates a list of parameters starting from lang setting and
    #   extending with extracted custom params
    def __params_parser(self, settings):
        paramsList = [settings["lang"]]
        paramsList.extend(settings["params"].replace("{", "")\
            .replace("}", "").strip("\"").split("\"\""))
        return paramsList


    # start thread
    def __start(self):
        if (
                not self._thread
                or not isinstance(self._thread, threading.Thread)
                or not self._thread.is_alive()
            ):
            self._close = False
            self._thread = threading.Thread(target=self._download_async)
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


    # thread which generates TTS from text appended to queue
    def _download_async(self):
        try:
            while True:
                if self._close:
                    break

                if self._texts:
                    text = self._texts.pop(0)

                    if len(text) <= self.get_max_chars():
                        params = [HttpUtility.UrlEncode(text)]
                        params.extend(self.__settings["params"])

                        file_path = os.path.join(
                                self.__settings["_cache"],
                                self.__settings["script"]
                                    + str(self._count)
                                    + self.__settings["audio_format"]
                            )

                        try:
                            if self._close:
                                break
                            download_tts(file_path,
                                        self.__settings["webservice"],
                                        params)

                            if self._close:
                                break
                            file_path = process_tts(file_path,
                                                    self.__settings)

                            self._audios.append([file_path, text])
                            self._count += 1

                        except Exception as e:
                            Parent.Log(self.__settings["script"],
                                "Error generating TTS file > " + str(e))

                time.sleep(0.150)

        except Exception as e:
            Parent.Log(self.__settings["script"],
                "Error gathering info for TTS file > " + str(e))
        return


    # append text to generate TTS
    #   it usually cuts to 200 chars max and apply chars replacements
    #   by setup
    # returns the new reference text, eventually with cuts and replaces
    def append(self, text):

        text = self.get_ref_text(text)
        self._texts.append(text)

        return text


    # External method to get the reference text from original text,
    #   same reference text which would be used on append method call
    def get_ref_text(self, text):
        return self.__ref_text(
                                text,
                                self.__settings["clean_urls"],
                                self.__settings["replace_urls"],
                                self.__settings["emote_prefix"],
                                self.__settings["emote_name_upper"],
                                self.__settings["clean_rep_word"],
                                self.__settings["max_rep_word"],
                                self.__settings["clean_rep_lett"],
                                self.__settings["replaces"],
                                self.__settings["alias_list"],
                                self.__settings["chars_swapping"],
                                self.__settings["cut_max_chars"],
                                self.get_max_chars()
                                )


    # Internal core method to get a reference text from original text,
    #   with max length and chars replacement
    def __ref_text(self, text, clean_urls = False, replace_urls = "",
                        emote_prefix = "", emote_name_upper = True,
                        clean_rep_word = True, max_rep_word = 3,
                        clean_rep_lett = True, replaces = "",
                        alias_dict = {}, chars_swapping = {},
                        cut_max_chars = True, max_chars = 200):
        if text:
            if clean_urls:
                text = self.__clean_urls(text, replace_urls)

            text = self.__clean_emotes_prefix(text, emote_prefix,
                                                emote_name_upper)

            if clean_rep_lett:
                text = self.__clean_repeated_letters(text)

            if clean_rep_word:
                text = self.__clean_repeated_words(text, max_rep_word)

            text = self.__replace_words_with_aliases(text, alias_dict)

            text = self.__replace_chars_with_swaps(text, chars_swapping)

            text = self.__replace_each_char_with_space(text, replaces)

            if cut_max_chars:
                text = text[:max_chars]

        return text


    # Replaces urls with a given text
    def __clean_urls(self, text, replace):
        if text:
            pattern = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'\
            '([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
            text = re.sub('https?', "",
                            re.sub(pattern, replace, text),
                            flags=re.IGNORECASE)
        return text


    # Clean letters repeated more than 2 times, letting them be repeated only 2 times
    def __clean_repeated_letters(self, text):
        if text:
            text = re.sub(r'(.)\1{2,}', r'\1\1', text, flags=re.IGNORECASE)
        return text


    # Clean words repeated more than "max" times,
    #   letting them be repeated only "max" times
    def __clean_repeated_words(self, text, max):
        if text:
            text = re.sub(r"\s+", ' ', text.replace(":", " "))
            max = 3 if not max else int(max)

            pattern = '(\s\w+)\\1{' + str(max) + ',}'
            replace = '\\1' * max

            text = re.sub(pattern, replace, text, flags=re.IGNORECASE)

        return text


    # Into given text, replaces all occurence of alias_list keys
    #   as whole word with their relative value. Not case sensitive.
    def __replace_words_with_aliases(self, text, alias_dict):
        if text:
            for word in alias_dict:
                text = re.sub(
                            r"\b%s\b" % re.escape(word),
                            re.escape(alias_dict[word]),
                            text,
                            flags=re.IGNORECASE
                            )
        return text


    # Into given text, replaces all occurence of chars_swapping keys
    #   partial chars with their relative value. Case sensitive.
    def __replace_chars_with_swaps(self, text, chars_swap):
        if text:
            for chars in chars_swap:
                text = re.sub(
                            r"%s" % re.escape(chars),
                            re.escape(chars_swap[chars]),
                            text
                            )
        return text


    # Replaces any occurrence in text of each single character from
    #   chars with a space
    def __replace_each_char_with_space(self, text, chars):
        if text and chars:
            chars = re.escape(chars)
            text = re.sub(
                        r"\s+", ' ',
                        re.sub(
                            r'['+chars+']',
                            ' ',
                            text,
                            flags=re.IGNORECASE
                            )
                        )
        return text


    # clean all occurrente of prefix, when maches with the inital part
    #   of a word plus a first letter of something else
    def __clean_emotes_prefix(self, text, prefix, nameUp):
        if text and prefix:
            first = "A-Z"
            if not nameUp:
                first += "a-z"
            text = re.sub(r'\b'+prefix+'(['+first+']\w*)', r'\1', text) \
                    .lower()
        return text


    # Returns the alias of a single word,
    #   if exists as key in alias_list's dict
    def get_alias(self, word):
        if word:
            alias_dict = self.__settings["alias_list"]
            if word in alias_dict:
                word = alias_dict[word]
        return word


    # Returns the swap chars sequence of a given chars sequence,
    #   if exists as key in chars_swapping's dict
    def get_swap(self, chars):
        if chars:
            chars_swap = self.__settings["chars_swapping"]
            if chars in chars_swap:
                chars = chars_swap[word]
        return chars


    # External method to get current max chars setting
    def get_max_chars(self):
        return self.__settings["max_chars"]


    # Checks if a TTS is generate for such script
    #   optionally: it can check original text, too
    def check(self, text = None):

        for audio in self._audios:
            if not text or text == audio[1]:
                return True

        return False


    # Get the first TTS generated for such script
    #   (and remove it from queue)
    # otherwise: returns None if not found
    #   (could just still be not ready)
    # optionally: it can check original text, too
    def get(self, text = None):

        for audio in self._audios[:]:
            if not text or text == audio[1]:
                path = audio[0]
                self._audios.remove(audio)
                return path

        return None


    # After using "append" method, you can use this method
    #   to directly wait until TTS file is generated
    # Optionally: it can check original text, too
    # Notes:
    #   Be sure you appended a file with such parameters first,
    #   or your script will have to wait until timeout without success
    def get_now(self, text = None):
        timeout = self.__settings["timeout"]
        loop_start = time.time()

        while not self.check(text):
            if (time.time() - loop_start) > timeout:
                return None
            continue

        return self.get(text)


    # Given the path is a sound file, it launches
    #   Parent.PlaySound(path, volume) for you.
    # It waits until Parent.PlaySound(path, volume) actually
    #   played the sound.
    # [No timeout is applied: we trust Parent.PlaySound(path, volume)]
    # For TTS audio generated by this library,
    #   the volume is already set internally, so this method keeps it
    #   untouched by always playing at volume 1.0
    def play(self, path):
        if path:
            while not Parent.PlaySound(path, 1.0):
                continue
        return True


    # Remove the file on such path, and all elements with that path
    #   in TTS generated queue, if any.
    # It's best practice to clean cache, after playing file with
    #   any player library
    def clean(self, path):
        run_cmd('del "{0}"'.format(path))

        for audio in self._audios[:]:
            if audio[0] == path:
                self._audios.remove(audio)

        return


    # Appends a new text into the queue, to transform into TTS;
    # waits for TTS to be generated for such script and text;
    # get its path, play it and delete it.
    # Notes:
    #   If queue is already long, it holds your script until that TTS
    #       is generated and played.
    #   It is also an example on how to use the other methods of this
    #      library.
    #   After playing file with Chatbot's function
    #      Parent.PlaySound(path, volume) it cleans that file from
    #      the cache, as it's best practice to do.
    #   Your script could be forced to wait until timeout,
    #      if something goes wrong.
    # Returns the new reference text, eventually cut to max chars and
    #   with chars replacements.
    def append_and_play(self, text):
        text = self.append(text)
        path = self.get_now(text)

        if path:
            self.play(path)
            self.clean(path)

        return text


    # parse a list of corresponding element,
    #   formatted this way "Element:Correspondence",
    #   aka: "Word:Alias".
    # returns a dictionary where Elements (or Words) are keys,
    #   and Correspondences (or Aliases) are values.
    @staticmethod
    def parse_alias_list(alias_list):
        # split all word:alias couples by semicolon
        alias_list = alias_list.split(";")
        # split word and alias by colon
        alias_list = [x.split(":") for x in alias_list]

        new_alias_dict = {}
        for s in alias_list:
            if s and s[0]:  # no empty keys are allowed
                if len(s) < 2:
                    s.append("")
                new_alias_dict[s[0].strip()] = s[1]

        return new_alias_dict


# Download from chosen voice generator webservice using defined
#   TTS settings
def download_tts(file_path, webservice, params):
    with WebClient() as wc:
        try:
            url = webservice.format(*params)
            parse = urlparse(url)
            wc.Headers["Referer"] = (
                                        parse.scheme + "://"
                                        + parse.netloc + "/"
                                    )
            wc.Headers["User-Agent"] = "Chrome/104.0 (Linux; Android 10)"
            wc.DownloadFile(url, file_path)

        except Exception as e:
            Parent.Log("download_tts",
                "Error reaching TTS webservice > " + str(e))
    return


# Changes the pitch, speed and volume of downloaded audio file
def process_tts(file_path, settings):
    try:
        temp_mp3 = os.path.join(os.path.dirname(file_path), "processing.mp3")

        af = []
        if settings["pitch_on"]:
            af.append("asetrate=24000*{0}".format(settings["pitch"]))
        if settings["speed_on"]:
            af.append("atempo={0}/{1}".format(
                                            settings["speed"],
                                            settings["pitch"])
                                            )
        if settings["volume_on"]:
            af.append("volume={0}".format(settings["volume"]))
        af = "" if not af else "-af " + ",".join(af)

        commands = [
            'cd "{0}"'.format(settings["_path"]),
            'ffmpeg.exe -t {0} -i "{1}" {2} "{3}" -y'.format(
                settings["length"],
                file_path,
                af,
                temp_mp3
            ),
            'del "{0}"'.format(file_path),
        ]
        run_cmd(" & ".join(commands))

        if not file_path.endswith(".mp3"):
            os.path.splitext(file_path)[0] + ".mp3"
        run_cmd('move "{0}" "{1}"'.format(temp_mp3, file_path))

    except Exception as e:
        Parent.Log("process_tts", "Error processing TTS file > " + str(e))
    return file_path


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
