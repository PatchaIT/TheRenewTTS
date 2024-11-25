# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SHARED INFO:
#
# Script: The ReNew TTS script
#           formely was:
#               TheNewTTS script for Streamlabs Chatbot
#               Copyright (C) 2020 Luis Sanchez
# Version: 1.04
# Description: Text to speech with Google translate voice,
#               or your own custom TTS webservice
# Change: Fixed a bug with Blacklist file loading
#       Fixed a bug with TTS stuttering aliases with spaces
#       Added permission level VIP (includes subscribers and moderators)
#       Added setting to keep or not keep queing on pause
# Services: Twitch, Youtube
# Overlays: None
# Update Date: 2023/01/24
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CHANGELOG:
#
# Versions by LuisSanchezDev (TheNewTTS):
#   2019/11/12 v1.0 - Initial release
#   2019/11/27 v1.0.1 - Fixed sound not playing
#   2019/12/03 v1.1 - Added max length in seconds
#   2019/12/08 v1.2 - Added blacklist
#   2019/12/09 v1.2.1 - Fixed Youtube/Mixer blacklist comparison
#                       against user ID instead of username
#   2020/08/29 v2.0 -
#       Added a say username before message option
#       Added a skip command
#       Fixed sometimes skipping messages
#       Fixed script stopped working suddenly
#   2020/10/05 v2.1 -
#       Added a clean repeated words/emotes option
#       Added a clean repeated letters option
#       Added a clean and replace links option
#       Added a ignore messages starting with a character option
#
# Versions by Patcha (TheRenewTTS):
#   2022/11/20 av1.0 -
#       Using reworked python custom libraries for TTS download & play,
#           which can be shared with other scripts without conflicts
#       Possibility to set an own custom TTS webserver (if you have it)
#       "Clean repeated words/emotes" option will no longer remove
#           punctuation from sentences
#           + you can now set a maximum allowed amount of repetitions
#           + it's no more case sensitive
#       "Clean repeated letters" option will now replace repetitions
#           with a double letter
#           + it's no more case sensitive
#       "Ignore messages starting with" option now can set multiple
#           characters, which means it still checks first character,
#           but compares with each one setted into a series
#       Option to replace each char in a series with spaces
#           (if you don't want TTS to read them literally)
#       Option to replace some words/usernames with other words/aliases
#       Option to replace some chars sequence with another sequence,
#           if you need to correct TTS pronunciation/spelling
#           (invasive: could create oddities)
#       Option to set channel's emotes prefix, to be skipped and try
#           to read only emotes names
#           (case sensitive, but invasive: could create oddities
#               if that prefix is a common chars sequence)
#           + there's an option to filter only prefixes followed
#               by uppercase letter (it helps prevent most oddities)
#       Option to set a max amount of chars lower than 200
#           + option to cut and not skip messages too long
#       Option to disable/enable each command's message reply
#           + new command messages to be able to customize
#           + (also for moderator commands)
#       New skip options for moderators:
#           - if they add an argument to standard skip command, it will
#               skip all TTS with such text inside from current queue
#           - a new command to skip "next" TTS, while the current one
#               is still playing
#           - a new command to skip the whole TTS queue and start a new
#       Commands are no more case sensitive
#       Usernames are no more case sensitive
#       Option to make moderators bannable from TTS
#           (it means they won't use nor TTS nor moderator commands)
#       Options to disable volume, pitch and speed alterators
#           (useful for custom TTS webserver)
#       Script files rearranged into subfolders
#   2023/01/05 av1.01 -
#       Fixed bug skipping first word on Read ALL
#       Allows to force read lowercased or uppercased
#   2023/01/07 av1.02 - Fixed a bug with message Cost set to 0
#   2023/01/15 av1.03 - Added a customizable !pause command
#   2023/01/24 av1.04 -
#       Fixed a bug with Blacklist file loading
#       Fixed a bug with TTS stuttering aliases with spaces
#       Added permission level VIP (includes subscribers and moderators)
#       Added setting to keep or not keep queing on pause
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Import Libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import clr
import os
import sys
import time
import re
import json
import codecs

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# Add script's folder to path to be able to find the other modules
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from manage_media_utils_103 import MediaManager, run_cmd
from settings_utils_101 import Settings
from blacklist_utils_101 import Blacklist


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   [Required] Script Information
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Description = "Text to speech with Google translate voice, or your own"\
                " custom TTS webservice."
ScriptName = "The Renew TTS"
Creator = "Patcha (from LuisSanchezDev)"
Version = "1.04"
Website = "https://www.patcha.it"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Define Global Variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SCRIPT_NAME = ScriptName.replace(" ", "")
DIRECTORY = os.path.dirname(__file__)
DB_PATH = os.path.join(DIRECTORY, "db")
SETTINGS_PATH = os.path.join(DIRECTORY, "Settings")
SETTINGS_FILE = os.path.join(SETTINGS_PATH, "settings.json")
DEFAULTS = {}
CHUNK = 1024

# TTS vars
global BOT_ON, LIB_PATH, DWNL_SET
BOT_ON = True
LIB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
DWNL_SET = {}

# PLAY and MEDIA_MAN vars
global PLAY_SET, MAN_SET, MEDIA_MAN
PLAY_SET = {}
MAN_SET = {}
MEDIA_MAN = None

# Blacklist
global BLACKLIST_FILE, BLACKLIST
BLACKLIST_FILE = os.path.join(DB_PATH, "blacklist.db")
BLACKLIST = None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   [Required] Initialize Data (Only called on load)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Init():
    global SETTINGS, DIRECTORY
    global DEFAULTS, TIMEOUT
    global BOT_ON, DWNL_SET, LIB_PATH
    global PLAY_SET, MAN_SET, MEDIA_MAN
    global BLACKLIST_FILE, BLACKLIST
    global THE_COMMAND, PAUSED, KEEP

    # Create Settings Directory
    if not os.path.exists(SETTINGS_PATH):
        os.makedirs(SETTINGS_PATH)

    TIMEOUT = 30
    DEFAULTS = {
        "script": SCRIPT_NAME,
        "read_all_text": False,
        "say_username": True,
        "say_after_username": "says",
        "ignore_starting_with": "!",
        "command": "!tts",
        "permission": "Everyone",
        "cooldown": 0,
        "user_cooldown": 0,
        "cost": 0,
        "do_msg_missing_text": True,
        "do_msg_permission": True,
        "do_msg_cooldown": True,
        "do_msg_user_cooldown": True,
        "do_msg_cost": True,
        "do_msg_too_long": True,
        "do_msg_blacklisted": True,
        "msg_missing_text": "You need to specify a message.",
        "msg_permission": "You don't have enough permissions to use this"\
                            " command.",
        "msg_cooldown": "This command is still on cooldown!",
        "msg_user_cooldown": "You need to wait before using this command"\
                                " again.",
        "msg_cost": "You don't have enough money!",
        "msg_too_long": "{0}'s message was too long!",
        "msg_blacklisted": "{0} is Blacklisted!",
        "cmd_ban": "!ttsban",
        "cmd_unban": "!ttsunban",
        "cmd_skip": "!ttskip",
        "cmd_skipnext": "!ttskipnext",
        "cmd_skipall": "!ttskipall",
        "cmd_pause": "!ttspause",
        "do_keep": False,
        "cmd_keep": "!ttskeep",
        "moderator_permission": "Caster",
        "mod_bannable": False,
        "do_msg_missing_target": True,
        "do_msg_paused": True,
        "do_msg_unpaused": True,
        "do_msg_keep": True,
        "do_msg_unkeep": True,
        "do_msg_blacklisted_success": True,
        "do_msg_blacklisted_unsuccess": True,
        "do_msg_unbanned_success": True,
        "do_msg_unbanned_unsuccess": True,
        "msg_missing_target": "Usage: {0} <username>",
        "msg_paused": "TTS paused.",
        "msg_unpaused": "TTS unpaused.",
        "msg_keep": "TTS keeps queuing on pause.",
        "msg_unkeep": "TTS stops queuing on pause.",
        "msg_blacklisted_success": "{0} successfully blacklisted!",
        "msg_blacklisted_unsuccess": "{0} already blacklisted!",
        "msg_unbanned_success": "{0} removed from blacklist!",
        "msg_unbanned_unsuccess": "{0} was not blacklisted!",
        "tts_bot_on": True,
        "tts_lang": "English (US) [en-US]",
        "tts_volume_on": True,
        "tts_volume": 90,
        "tts_pitch_on": True,
        "tts_pitch": 100,
        "tts_speed_on": True,
        "tts_speed": 100,
        "tts_length": 26,
        "tts_case": "",
        "tts_clean_repeated_letters": True,
        "tts_clean_repeated_words": True,
        "tts_replacement_urls": "link removed",
        "tts_max_repeated_words": 3,
        "tts_alias_list": "",
        "tts_chars_swapping": "@:a ,",
        "tts_clean_urls": True,
        "tts_confirm": "Configuration updated successfully",
        "tts_replaces": "_",
        "tts_emote_name_first_is_upper": True,
        "tts_emote_prefix": "",
        "tts_cut_max_chars": True,
        "tts_max_chars": 200,
        "tts_params": "",
        "tts_webservice": "https://translate.google.com/translate_tts?ie="\
                            "UTF-8&tl={1}&client=tw-ob&q={0}",
        "tts_audio_format" : ".mp3"
    }

    SETTINGS = Settings(SETTINGS_FILE, DEFAULTS)
    THE_COMMAND = SETTINGS.command.lower()
    PAUSED = False
    KEEP = SETTINGS.do_keep

    if SETTINGS.permission == "VIP":
        SETTINGS.permission = "VIP+"

    cache_folder = os.path.join(LIB_PATH, "cache")
    loop_start = time.time()
    while True:
        try:
            if (time.time() - loop_start) > TIMEOUT:
                break
            if os.path.isdir(cache_folder):
                run_cmd('RMDIR /Q/S "{0}"'.format(cache_folder))
            os.mkdir(cache_folder)
            break
        except:
            continue


    # TTS settings: length and timeout are in seconds
    DWNL_SET = {
        "script": SCRIPT_NAME,
        "lang": SETTINGS.tts_lang,
        "volume_on": SETTINGS.tts_volume_on,
        "pitch_on": SETTINGS.tts_pitch_on,
        "speed_on": SETTINGS.tts_speed_on,
        "volume": SETTINGS.tts_volume / 100.0,
        "pitch": SETTINGS.tts_pitch / 100.0,
        "speed": SETTINGS.tts_speed / 100.0,
        "length": SETTINGS.tts_length,
        "timeout": TIMEOUT,
        "keep": SETTINGS.do_keep,
        "case": SETTINGS.tts_case,
        "clean_rep_lett": SETTINGS.tts_clean_repeated_letters,
        "clean_rep_word": SETTINGS.tts_clean_repeated_words,
        "max_rep_word": SETTINGS.tts_max_repeated_words,
        "alias_list": SETTINGS.tts_alias_list,
        "chars_swapping": SETTINGS.tts_chars_swapping,
        "clean_urls": SETTINGS.tts_clean_urls,
        "replace_urls": SETTINGS.tts_replacement_urls,
        "replaces": SETTINGS.tts_replaces,
        "emote_name_upper": SETTINGS.tts_emote_name_first_is_upper,
        "emote_prefix": SETTINGS.tts_emote_prefix,
        "cut_max_chars": SETTINGS.tts_cut_max_chars,
        "max_chars": SETTINGS.tts_max_chars,
        "params": SETTINGS.tts_params,
        "webservice": SETTINGS.tts_webservice,
        "audio_format" : SETTINGS.tts_audio_format,
        "_path": LIB_PATH,
        "_cache": cache_folder,
    }

    # PLAY settings: length and timeout are in seconds
    PLAY_SET = {
        "script": SCRIPT_NAME,
        "length": SETTINGS.tts_length,
        "timeout": TIMEOUT,
        "keep": SETTINGS.do_keep,
    }

    # Save on TTS bot resources and threads, if bot is not enabled
    BOT_ON = SETTINGS.tts_bot_on
    if BOT_ON:
        MAN_SET = {
            "script": SCRIPT_NAME,
            "timeout": TIMEOUT,
            "keep": SETTINGS.do_keep,
            "MEDIA_DWNL": DWNL_SET,
            "MEDIA_PLAY": PLAY_SET,
        }
        MEDIA_MAN = MediaManager(MAN_SET)

    BLACKLIST = Blacklist(BLACKLIST_FILE)

    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   [Required] Execute Data / Process messages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Execute(data):
    global PAUSED, KEEP

    # Check if message is valid, and not making this script work from Discord
    if data.IsChatMessage() and not data.IsFromDiscord():

        # Check command, username and alias
        command = data.GetParam(0).lower()
        user_name = data.UserName.lower()
        alias_name = MEDIA_MAN.MEDIA_DWNL.get_alias(user_name)

        # Moderator commands
        if Parent.HasPermission(data.User, SETTINGS.moderator_permission, ""):
            target = data.GetParam(1).lower()

            # check if banned mod
            if (SETTINGS.mod_bannable and
                    BLACKLIST.is_user_blacklisted(user_name)):
                if SETTINGS.do_msg_blacklisted:
                    Parent.SendStreamMessage(
                        SETTINGS.msg_blacklisted.format(alias_name))
                return

            # skip (current) or skip target
            if command == SETTINGS.cmd_skip.lower():
                if target:
                    MEDIA_MAN.MEDIA_PLAY.skip_containing(target)
                else:
                    MEDIA_MAN.MEDIA_PLAY.skip()
                return

            # skip next
            elif command == SETTINGS.cmd_skipnext.lower():
                MEDIA_MAN.MEDIA_PLAY.skip_next()
                return

            # skip all
            elif command == SETTINGS.cmd_skipall.lower():
                MEDIA_MAN.MEDIA_PLAY.skip_all()
                return

            # pause
            elif command == SETTINGS.cmd_pause.lower():
                PAUSED = MEDIA_MAN.pause()
                if PAUSED and SETTINGS.do_msg_paused:
                    Parent.SendStreamMessage(SETTINGS.msg_paused)
                elif not PAUSED and SETTINGS.do_msg_unpaused:
                    Parent.SendStreamMessage(SETTINGS.msg_unpaused)
                return

            # keep queuing on pause
            elif command == SETTINGS.cmd_keep.lower():
                KEEP = MEDIA_MAN.keep()
                if KEEP and SETTINGS.do_msg_keep:
                    Parent.SendStreamMessage(SETTINGS.msg_keep)
                elif not KEEP and SETTINGS.do_msg_unkeep:
                    Parent.SendStreamMessage(SETTINGS.msg_unkeep)
                return

            # ban
            elif command == SETTINGS.cmd_ban.lower():
                if data.GetParamCount() != 2:
                    if SETTINGS.do_msg_missing_target:
                        Parent.SendStreamMessage(
                            SETTINGS.msg_missing_target.format(
                                SETTINGS.cmd_ban))
                    return

                # update blacklist
                if BLACKLIST.add_user(target):
                    if SETTINGS.do_msg_blacklisted_success:
                        Parent.SendStreamMessage(
                            SETTINGS.msg_blacklisted_success.format(
                                MEDIA_MAN.MEDIA_DWNL.get_alias(target)))
                else:
                    if SETTINGS.do_msg_blacklisted_unsuccess:
                       Parent.SendStreamMessage(
                        SETTINGS.msg_blacklisted_unsuccess.format(
                            MEDIA_MAN.MEDIA_DWNL.get_alias(target)))
                return

            # unban
            elif command == SETTINGS.cmd_unban.lower():
                if data.GetParamCount() != 2:
                    if SETTINGS.do_msg_missing_target:
                        Parent.SendStreamMessage(
                            SETTINGS.msg_missing_target.format(
                                SETTINGS.cmd_unban))
                    return

                # update blacklist
                if BLACKLIST.remove_user(target):
                    if SETTINGS.do_msg_unbanned_success:
                        Parent.SendStreamMessage(
                            SETTINGS.msg_unbanned_success.format(
                                MEDIA_MAN.MEDIA_DWNL.get_alias(target)))
                else:
                    if SETTINGS.do_msg_unbanned_unsuccess:
                        Parent.SendStreamMessage(
                            SETTINGS.msg_unbanned_unsuccess.format(
                                MEDIA_MAN.MEDIA_DWNL.get_alias(target)))
                return

        # Check text to speak
        if SETTINGS.read_all_text or command == THE_COMMAND:
            if not PAUSED or KEEP:
                text = data.Message
                start = text[0]
                text = re.sub(r'^'+THE_COMMAND+' ', '', text, flags=re.IGNORECASE)
                text = MEDIA_MAN.MEDIA_DWNL.get_ref_text(text)

                # Read the whole chat
                if SETTINGS.read_all_text:

                    # check if banned
                    if BLACKLIST.is_user_blacklisted(user_name):
                        return

                    # check if starts with characters to ignore
                    if start in SETTINGS.ignore_starting_with:
                        return

                    # check length, speak error only if not paused (no queing)
                    if len(text) > MEDIA_MAN.MEDIA_DWNL.get_max_chars():
                        if SETTINGS.do_msg_too_long and not MEDIA_MAN.is_paused():
                            MEDIA_MAN.append(
                                SETTINGS.msg_too_long.format(alias_name))

                    # play message
                    else:
                        MEDIA_MAN.append(alias_name + " "
                            + SETTINGS.say_after_username + ": "
                            + text if SETTINGS.say_username else text)

                # Read on command
                elif command == THE_COMMAND:
                    if not Parent.HasPermission(
                            data.User, SETTINGS.permission, ""):
                        if SETTINGS.do_msg_permission:
                            Parent.SendStreamMessage(SETTINGS.msg_permission)
                        return

                    # check if banned
                    if BLACKLIST.is_user_blacklisted(user_name):
                        if (SETTINGS.do_msg_blacklisted):
                            Parent.SendStreamMessage(
                                SETTINGS.msg_blacklisted.format(alias_name))
                        return

                    # check user's cooldown
                    if (SETTINGS.user_cooldown and
                            Parent.GetUserCooldownDuration(
                                ScriptName, SETTINGS.command, data.User)):
                        if SETTINGS.do_msg_user_cooldown:
                            Parent.SendStreamMessage(SETTINGS.msg_user_cooldown)
                        return

                    # check command's cooldown
                    if (SETTINGS.cooldown and
                            Parent.GetCooldownDuration(
                                ScriptName, SETTINGS.command)):
                        if SETTINGS.do_msg_cooldown:
                            Parent.SendStreamMessage(SETTINGS.msg_cooldown)
                        return

                    # check if enough coins
                    if SETTINGS.cost > 0:
                        if not Parent.RemovePoints(
                                data.User, data.UserName, SETTINGS.cost):
                            if SETTINGS.do_msg_cost:
                                Parent.SendStreamMessage(SETTINGS.msg_cost)
                            return

                    # check message
                    if not data.GetParam(1):
                        if SETTINGS.do_msg_missing_text:
                            Parent.SendStreamMessage(SETTINGS.msg_missing_text)
                        return

                    # if message too long
                    if len(text) > MEDIA_MAN.MEDIA_DWNL.get_max_chars():
                        if SETTINGS.cost > 0:
                            Parent.AddPoints(data.User, data.UserName, SETTINGS.cost)
                        if SETTINGS.do_msg_too_long:
                            Parent.SendStreamMessage(
                                SETTINGS.msg_too_long.format(alias_name))
                        return

                    # play message
                    else:
                        media = MEDIA_MAN.append(alias_name + " "
                            + SETTINGS.say_after_username + ": "
                            + text if SETTINGS.say_username else text)

                    # apply cooldowns
                    Parent.AddCooldown(ScriptName,
                        SETTINGS.command, SETTINGS.cooldown)
                    Parent.AddUserCooldown(ScriptName,
                        SETTINGS.command, data.User, SETTINGS.user_cooldown)

    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   [Required] Tick method (Gets called during every iteration even
#               when there is no incoming data)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Tick():
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   [Optional] Reload Settings (Called when a user clicks the
#               Save Settings button in the Chatbot UI)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ReloadSettings(jsonData):
    global MEDIA_MAN
    Unload()
    Init()
    if BOT_ON and MEDIA_MAN and SETTINGS.tts_confirm:
        MEDIA_MAN.append(SETTINGS.tts_confirm)
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   [Optional] Unload (Called when a user reloads their scripts or
#               closes the bot / cleanup stuff)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Unload():
    global MEDIA_MAN

    if MEDIA_MAN:
        MEDIA_MAN.close()
        del MEDIA_MAN

    return
