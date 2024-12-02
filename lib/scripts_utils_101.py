# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SHARED INFO:
#
# Some code are originally made by Patcha
# Some other codess are originally extracted from "TheNewTTS script
#   for Streamlabs Chatbot" libraries
#   Copyright (C) 2020 Luis Sanchez
#   Reworked and exported by Patcha (2023)
#
# Note:
#    if you wanna further customize this library, 
#        rename the file like "script_utils_<ScriptName>_<version>.py"
#        or you'll risk conflicts with namesake libraries
#        possibly used by other scripts.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CHANGELOG:
#
# Versions:
# tts_media.py
#   2023/01/27 v1.0 - Initial ReNewTTS release, includes:
#       parse_alias_list (by Patcha)
#       strip_username (by LuisSanchezDev)
#       download_tts (by LuisSanchezDev)
#       process_media (by LuisSanchezDev)
#       run_cmd (by LuisSanchezDev)
#       get_parent (by LuisSanchezDev)
#   2023/02/03 v1.01 - Greetings & PokemonCommunityGameSounder release
#       - includes:
#       parse_alias_list now can lowercase dict's keys
#       from_zero_to_one_dot_zero (by Patcha)
#       check_float (by Patcha)
#       check_false (by Patcha)
#       check_in_list (by Patcha)
#       is_existing_file_path (by Patcha)
#       is_existing_file_path_list (by Patcha)
#       parent_audio_player (by Patcha)
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import os
import clr
import System

# Define Global Variables
DIRECTORY = os.path.dirname(__file__)

# Required to import Parent from AnkhBotR2 (aka: Streamlabs Chatbot)
clr.AddReference([
        asbly for asbly in System.AppDomain.CurrentDomain.GetAssemblies()
        if "AnkhBotR2" in str(asbly)
    ][0])
import AnkhBotR2

# Required to download files
clr.AddReference("System.Web")
from System.Web import HttpUtility
from System.Net import WebClient
from urlparse import urlparse

# Required to run cmd commands without a window and wait for the result
from System.Diagnostics import Process, ProcessStartInfo, ProcessWindowStyle


# Check if the value could be a valid float, and return it casted
#   to float
# if not, returns the given default
def float_check(value, default):
    try:
        return float(value)
    except:
        return default


# Check if the value is trying to be a False boolean, and returns
#   a real boolean
# returns True if True or "True"; otherwise False
def check_false(value):
    return (value == True or
            (isinstance(value, str) and value.lower() == "true")
            )


# Check if the value is included into given list
# returns value if in list, otherwise the element on index
def check_in_list(value, list, index):
    if value and list and value not in list:
        value = list[index]

    return value


# Parse a list of corresponding element,
#   formatted this way "Element:Correspondence",
#   aka: "Word:Alias".
# returns a dictionary where Elements (or Words) are keys,
#   and Correspondences (or Aliases) are values.
def parse_alias_list(alias_list, lowerkeys=False):
    # split all word:alias couples by semicolon
    alias_list = alias_list.split(";")
    # split word and alias by colon
    alias_list = [x.split(":") for x in alias_list]

    new_alias_dict = {}
    for s in alias_list:
        if s and s[0]:  # no empty keys are allowed
            if len(s) < 2:
                s.append("")
            key = s[0].strip()
            if lowerkeys:
                key = key.lower()
            new_alias_dict[key] = s[1]

    return new_alias_dict


# Transform from 0 to "divisor" range value
#   into from 0.0 to 1.0 range
def from_zero_to_one_dot_zero(value, divisor):
    try:
        one_dot_zero = float(value)
        one_dot_zero = one_dot_zero / divisor \
                        if one_dot_zero > 0.0 else one_dot_zero
    # if value is not a number
    except ValueError:
        one_dot_zero = 1.0

    return one_dot_zero


# Remove the @ character before an username
def strip_username(user_name):
    user_name = user_name.lower()
    if "@" in user_name:
        user_name = user_name.replace("@","")
    return user_name


# Checks if a given (relative) path esists starting
#   from given argument "folder"
#   or from given current folder, should use: os.path.dirname(__file__)
#   (this library's folder if parameter is empty)
def is_existing_file_path(path, folder = "", local = DIRECTORY):
    if not os.path.isfile(path):
        sub = os.path.join(folder, path)
        local = os.path.join(local, path)

        if folder and os.path.isfile(sub):
            return sub
        elif os.path.isfile(local):
            return local
        else:
            return None

    return path


# Uses is_existing_file_path method for each path in list
def is_existing_file_path_list(list, folder = "", local = DIRECTORY):
    if list:
        for i, s in enumerate(list):
            list[i] = is_existing_file_path(s, folder, local)
    return list


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


# Changes the pitch, speed and volume of file_path audio file
def process_media(file_path, settings):
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
        Parent.Log("process_media", "Error processing TTS file > " + str(e))
    return file_path


# Run cmd commands without a window and wait for the result
def run_cmd(command):
    pinfo = ProcessStartInfo()
    pinfo.FileName = "cmd.exe"
    pinfo.WindowStyle = ProcessWindowStyle.Hidden;
    pinfo.Arguments = "/C" + command
    cmd = Process.Start(pinfo)
    cmd.WaitForExit()
    return


# Import Parent from AnkhBotR2
#   it is suggested to be used with a global variable Parent, this way:
#   Parent = get_parent()
def get_parent():
    return AnkhBotR2.Managers.PythonManager()


# Global Parent variable to contact Chatbot's Parent object
Parent = get_parent()


# Use Parent's audio player to play an audio file
def parent_audio_player(path, vol):
    if path and vol:
        return Parent.PlaySound(path, vol)
    return True
