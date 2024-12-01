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
#   2023/01/27 v1.0 - Initial release, includes:
#       parse_alias_list (by Patcha)
#       strip_username (by LuisSanchezDev)
#       download_tts (by LuisSanchezDev)
#       process_media (by LuisSanchezDev)
#       run_cmd (by LuisSanchezDev)
#       get_parent (by LuisSanchezDev)
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import os
import clr
import System

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


# parse a list of corresponding element,
#   formatted this way "Element:Correspondence",
#   aka: "Word:Alias".
# returns a dictionary where Elements (or Words) are keys,
#   and Correspondences (or Aliases) are values.
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


# remove the @ character before an username
def strip_username(user_name):
    user_name = user_name.lower()
    if "@" in user_name:
        user_name = user_name.replace("@","")
    return user_name


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


Parent = get_parent()
