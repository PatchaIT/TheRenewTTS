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
#   2022/11/27 av1.02 - Allows to force read lowercased or uppercased
#   2023/01/15 av1.03 - Added a pause method
#   2023/01/24 av1.04 -
#       Fixed a bug with TTS stuttering aliases with spaces
#       Added setting to keep or not keep queing on pause
#   2023/01/24 av1.05 -
#       Removed typo oddity into a comment
#       Exported utility functions into dedicated new library
#   2023/02/01 av1.06 -
#       Flag to disable using aliases even if any
#       Flag to preview textually in chat the reading text
#               if you use "append_and_play" method
#           or write textually in chat the third parameter
#               if you use "play" method and you set a second parameter
#       Possibility to choose a specific language for the TTS reader
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

from scripts_utils_101 import *

# Define Global Variables
global Parent, _defaults, _cases

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
    "keep": False,
    "case": "",
    "clean_rep_lett": True,
    "clean_rep_word": True,
    "max_rep_word": 3,
    "alias_on": True,
    "alias_list": "",
    "chars_swapping": "",
    "clean_urls": False,
    "replace_urls": "link removed",
    "replaces": "",
    "emote_name_upper": True,
    "emote_prefix": "",
    "cut_max_chars": True,
    "max_chars": 200,
    "preview": False,
    "params": "",
    "webservice": "",
    "audio_format" : "",
    # "_path": cannot have a default, must be explicit
    # "_cache": cannot have a default, must be explicit
}

_cases = ["", "Lower", "Upper"]


class MediaDownloader:
    def __init__(self, settings):
        global Parent

        Parent = get_parent()

        self._texts = []
        self._audios = []
        self._count = 0
        self._thread = None

        self.__settings = self.__settings_check(settings)
        self._keep = self.__settings["keep"]

        self.__start()


    # standard checks on settings voices
    # returns settings with checked voices
    def __settings_check(self, settings):
        settings = self.__check_defaults(settings)

        settings["lang"] = (
                                re.match(r"^.*\[(.+)\]", settings["lang"])
                                .groups()[0] if settings["lang"] else "en-US"
                            )

        settings["volume"] = float_check(settings["volume"], 1.0)
        settings["pitch"] = float_check(settings["pitch"], 1.0)
        settings["speed"] = float_check(settings["speed"], 1.0)
        settings["length"] = int(float_check(settings["length"], 30))
        settings["timeout"] = int(float_check(settings["timeout"], 30))

        settings["cut_max_chars"] = check_false(
                                        settings["cut_max_chars"])
        settings["max_chars"] = int(float_check(settings["max_chars"],
                                        200))
        if settings["max_chars"] > 200:
            settings["max_chars"] = 200

        settings["volume_on"] = check_false(settings["volume_on"])
        settings["pitch_on"] = check_false(settings["pitch_on"])
        settings["speed_on"] = check_false(settings["speed_on"])

        settings["case"] = check_in_list(settings["case"], _cases, 0)

        settings["clean_rep_lett"] = check_false(
                                        settings["clean_rep_lett"])
        settings["clean_rep_word"] = check_false(
                                        settings["clean_rep_word"])
        settings["max_rep_word"] = int(float_check(
                                        settings["max_rep_word"], 3))
        settings["alias_on"] = check_false(
                                        settings["alias_on"])
        settings["alias_list"] = parse_alias_list(
                                        settings["alias_list"])
        settings["chars_swapping"] = parse_alias_list(
                                        settings["chars_swapping"])
        settings["clean_urls"] = check_false(
                                        settings["clean_urls"])

        settings["preview"] = check_false(settings["preview"])

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
            self._paused = False
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
    def _download_async(self):
        try:
            while True:
                if self._close:
                    break

                if self._texts and not self._paused:
                    text_info = self._texts.pop(0)
                    text = text_info[0]
                    lang = text_info[1]

                    if len(text) <= self.get_max_chars():
                        params = [HttpUtility.UrlEncode(text)]
                        params.extend(self.__settings["params"])

                        if lang is not None:
                            params[1] = lang

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
                            file_path = process_media(file_path,
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
    #   or empty string if nothing was appended
    def append(self, text, lang = None):

        if not self._paused or self._keep:
            text = self.get_ref_text(text)
            self._texts.append([text, lang])
        else:
            return ""

        return text


    # External method to get the reference text from original text,
    #   same reference text which would be used on append method call
    def get_ref_text(self, text):
        return self.__ref_text(
                            text,
                            self.__settings["case"],
                            self.__settings["clean_urls"],
                            self.__settings["replace_urls"],
                            self.__settings["emote_prefix"],
                            self.__settings["emote_name_upper"],
                            self.__settings["clean_rep_word"],
                            self.__settings["max_rep_word"],
                            self.__settings["clean_rep_lett"],
                            self.__settings["replaces"],
                            self.__settings["alias_list"] \
                                if self.__settings["alias_on"] else {},
                            self.__settings["chars_swapping"],
                            self.__settings["cut_max_chars"],
                            self.get_max_chars()
                            )


    # Internal core method to get a reference text from original text,
    #   with max length and chars replacement
    def __ref_text(self, text, case,
                        clean_urls = False, replace_urls = "",
                        emote_prefix = "", emote_name_upper = True,
                        clean_rep_word = True, max_rep_word = 3,
                        clean_rep_lett = True, replaces = "",
                        alias_dict = {}, chars_swapping = {},
                        cut_max_chars = True, max_chars = 200):

        if text:
            if case:
                if case == "Lower":
                    text = text.lower()
                elif case == "Upper":
                    text = text.upper()

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
            text = re.sub(r"\s+", ' ', text)
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
                text = re.sub(r'\\(.)', r'\1', text)
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
            text = re.sub(r'\b'+prefix+'(['+first+']\w*)', r'\1', text)
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
    def get_main_lang_code(self):
        return self.__settings["lang"]


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
    def play(self, path, text = None, preview = None):
        if preview is not True and preview is not False:
            preview = self.__settings["preview"]

        while not parent_audio_player(path, 1.0):
            continue

        if text and preview:
            Parent.SendStreamMessage(text)

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
    def append_and_play(self, text, preview = None, lang = None):
        text = self.append(text, lang)

        if text:
            path = self.get_now(text)

            if path:
                self.play(path, text, preview)
                self.clean(path)

        return text
