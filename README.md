# TheRenewTTS

[![development status | 1 - planning](https://img.shields.io/badge/development_status-1_--_planning-yellow)](https://pypi.org/classifiers/)
[![code style: pep-008](https://img.shields.io/badge/code_style-pep--0008-FFF8FF)](https://peps.python.org/pep-0008/)
[![license: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![release](https://img.shields.io/github/v/release/PatchaIT/TheRenewTTS)
[![next](https://img.shields.io/badge/next-v1.1.1-yellow)](https://github.com/PatchaIT/TheRenewTTS/tree/therenewtts_v1.1.1)

(On your Streamlabs Chatbot) Renewing the best Chat to Speech for Twitch and Youtube for Streamlabs Chatbot (in its creator's opinion).

## Table of Contents

* [About the Project](#about-the-project)
  * [Warning Notes](#warning-notes)
* [In Shorts](#in-shorts)
* [Changelog](#changelog)
  * [Versions by LuisSanchezDev (TheNewTTS)](#versions-by-luissanchezdev-thenewtts)
  * [Versions by Patcha (TheRenewTTS)](#versions-by-patcha-therenewtts)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Settings](#settings)
  * [General](#general)
  * [Command Configuration](#command-configuration)
  * [Command Messages](#command-messages)
  * [Moderator Commands](#moderator-commands)
  * [Moderator Commands Messages](#moderator-commands-messages)
  * [TTS Configuration](#tts-configuration)
  * [TTS Multi Languages](#tts-multi-languages)
  * [TTS Server](#tts-server)

## About The Project

Hi all,
  one day I wanted to reintroduce Text To Speach function in my scripts,
  so looking around I found [2020 Luis Sanchez's TheNewTTS script for
Streamlabs Chatbot](https://github.com/LuisSanchez-Dev/TheNewTTS).

But when I tried to implement such libraries into my scripts I noticed
  they wheren't suppose to work on multiple scripts without conflicts.

So I started reworking it, I splitted into different libraries, I made
  their threading systems compatible on multiple scripts and so on.
But then I thought the best and most complete way to put their features
  at work was on the same script where they came from. So that's how I
  ended up reworking the whole `TheNewTTS script` and creating this
  `TheRenewTTS script` version.

Enjoy.

### Warning Notes

Note:  
  If you're migrating from old TheNewTTS script, let's know that
    while most settings are the same, still settings files are no more
    compatible, because all variable names are changed.
  So it's better you note your current settings and then report them on
    the brand new TheRenewTTS script configuration GUI.
  Don't try to use same files from old TheNewTTS script!

Note:  
  If you're updating from a previous TheReNewTTS script version,
    you may have to delete old "lib" subdirectory before update,
    because all releases use new lib versions.

Note for Save Settings:  
  Sometimes Streamlabs Chatbot doesn't trigger `ReloadSettings` method on new
    settings save from Save Settings GUI button.

  If you can't hear TTS say the `Configuration updated successfully` sentence
    (by default `Configuration updated successfully`) probably new settings
    are saved, but you can't be sure if they're already reloaded and applied
    into current Chatbot session.

  In this case I'd suggest you to shut down and restart the Chatbot,
    or at least to refresh scripts from Scripts screen (the circle arrow icon
    on the top right).
  After that, make some checks to see if new settings are actually applied.

  Anyway, after every Chatbot start or reboot, I always suggest to refresh
    scripts at least once.

Note for Custom TTS:  
  Obviously you already need to have an existing custom TTS webservice.
  The script doesn't create a new one for you.
  It just allows you to use one you already own.
  Otherwise just keep using Google Translate's TTS as default.

## In Shorts

* Script: The ReNew TTS script
* Version: 1.1.1-SNAPSHOT
* Description: Text to speech with Google translate voice,
      or your own custom TTS webservice
* Change: Final fixing issue with sometimes custom settings
      not correctly loaded;
    Possibility to manually set channel/streamer name
* Services: Twitch, Youtube
* Overlays: None
* Made By: @Patcha_it
* Update Date: 2023/12/03

## Changelog

### Versions by LuisSanchezDev (TheNewTTS)

* 2019/11/12 v1.0.0
  * Initial release
* 2019/11/27 v1.0.1
  * Fixed sound not playing
* 2019/12/03 v1.1.0
  * Added max length in seconds
* 2019/12/08 v1.2.0
  * Added blacklist
* 2019/12/09 v1.2.1
  * Fixed Youtube/Mixer blacklist comparison against user ID instead of username
* 2020/08/29 v2.0.0
  * Added a say username before message option
  * Added a skip command
  * Fixed sometimes skipping messages
  * Fixed script stopped working suddenly
* 2020/10/05 v2.1.0
  * Added a clean repeated words/emotes option
  * Added a clean repeated letters option
  * Added a clean and replace links option
  * Added a ignore messages starting with a character option

### Versions by Patcha (TheRenewTTS)

* 2022/11/20 v1.0.0
  * Using reworked python custom libraries for TTS download & play,
      which can be shared with other scripts without conflicts
  * Possibility to set an own custom TTS webserver (if you have it)
  * `Clean repeated words/emotes` option will no longer remove
      punctuation from sentences
    * you can now set a maximum allowed amount of repetitions
    * it's no more case sensitive
  * `Clean repeated letters` option will now replace repetitions
      with a double letter
    * it's no more case sensitive
  * `Ignore messages starting with` option now can set multiple
      characters, which means it still checks first character,
      but compares with each one setted into a series
  * Option to replace each char in a series with spaces
      (if you don't want TTS to read them literally)
  * Option to replace some words/usernames with other words/aliases
  * Option to replace some chars sequence with another sequence,
      if you need to correct TTS pronunciation/spelling
      (invasive: could create oddities)
  * Option to set channel's emotes prefix, to be skipped and try
      to read only emotes names
      (case sensitive, but invasive: could create oddities
      if that prefix is a common chars sequence)
    * there's an option to filter only prefixes followed
      by uppercase letter (it helps prevent most oddities)
  * Option to set a max amount of chars lower than 200
    * option to cut and not skip messages too long
  * Option to disable/enable each command's message reply
    * new command messages to be able to customize
    * (also for moderator commands)
  * New skip options for moderators:
    * if they add an argument to standard skip command, it will
        skip all TTS with such text inside from current queue
    * a new command to skip `next` TTS, while the current one
        is still playing
    * a new command to skip the whole TTS queue and start a new
  * Commands are no more case sensitive
  * Usernames are no more case sensitive
  * Option to make moderators bannable from TTS
      (it means they won't use nor TTS nor moderator commands)
  * Options to disable volume, pitch and speed alterators
      (useful for custom TTS webserver)
  * Script files rearranged into subfolders
* 2023/01/05 v1.0.1
  * Fixed bug skipping first word on Read ALL
  * Allows to force read lowercased or uppercased
* 2023/01/07 v1.0.2
  * Fixed a bug with message Cost set to 0
* 2023/01/15 v1.0.3
  * Added a customizable !pause command
* 2023/01/24 v1.0.4
  * Fixed a bug with Blacklist file loading
  * Fixed a bug with TTS stuttering aliases with spaces
  * Added permission level VIP (includes subscribers and moderators)
  * Added setting to keep or not keep queing on pause
* 2023/01/27 v1.0.5
  * Removed typo oddity into a comment
  * Exported utility functions into dedicated new library
* 2023/07/30 v1.0.6
  * Flag to preview textually in chat the reading text
  * Channel owner doesn't need to pay anymore to use TTS
  * Possibility to allow choosing TTS language into chat command
* 2023/12/03 v1.1.0
  * Fixed issue with sometimes custom settings not correctly loaded
  * Thanks Chidinma for testing!
* 2025/xx/xx v1.1.1 * SNAPSHOT
  * Final fixing issue with sometimes custom settings not correctly loaded
  * Possibility to manually set channel/streamer name
  * If dll audio source is busy, it will retry until a timeout

## Getting Started

### Prerequisites

Have an installation of Streamlabs Chatbot, already logged in to your accounts.

* [Download Streamlabs Chatbot](https://streamlabs.com/desktop-chatbot)

Follow this tutorial to prepare your Streamlabs Chatbot installation to accept scripts.

* [[Streamlabs Chatbot] Scripts Explained by Castorr91](https://www.youtube.com/watch?v=l3FBpY-0880)

### Installation

1. Download the latest version of the script.
2. If you haven't already, open your Streamlabs Chatbot and log in to your
  Streamer and Bot accounts.
3. On the left side, wait for the `Scripts` tab to pop up and click it.
4. On the top right corner of the window, next to the reload button is an
  import script button (Arrow pointing right to a box) and select the script
  downloaded before.
5. You will receive a message box confirming the import, accept it.
6. The window will update and show the `The Renew TTS` script.
7. Click on the `The Renew TTS` name to see the configuration pane.

## Settings

Don't be scared about so many options, most of them are not mandatory to be
  customized. For the most, default options are enough ok.

For each option I'll note if and what changes there are, compared to the
  original TheNewTTS script settings from Luis Sanchez.

Note:  
  From version 1.06, I'll no long note in square brackets
    what changed compared to original TheNewTTS script settings
    from Luis Sanchez.  
  If you're very curious about that, you'll have to find the readMe of
    an older version.  
  Sorry, but I found this facilitates readability.

### General

> #### Read ALL chat

Check this to read all chat disregarding the command.

IF YOU ARE USING THIS FEATURE MAKE SURE TO SET A FAST SPEED
  SO THE CHATBOT CAN KEEP UP!

Also note that this feature may prevent the use of some other options.

> #### Force lower or upper case

Set this if you want TTS to read lowercase (could avoid acronyms
  reading on uppercase words) or uppercase (could read words as acronym).

> #### Clean repeated letters

Prevent repeated letters to be spoken and only speak them twice.

Example: noooooooo -> noo .

> #### Clean repeated words/emotes

Prevent repeated words/emotes to be spoken and only speak them as max
  as setted in the option `Max words/emotes repeat allowed`.

Example: :Kappa: :Kappa: :Kappa: :Kappa: :Kappa: :Kappa: -> :Kappa:

> #### Max words/emotes repeat allowed

How many times you allow to repeat a word/emote, if `Clean repeated
  words/emotes` option is enabled.

> #### Clean links

Prevent links to be spoken and say the replacement text instead.

> #### Replace links with

If `Clean links` is checked, links will be replaced with this text.

> #### Say username before message

Check this to say the username before the message.

> #### Say this after the username

Append this text to the username so the TTS makes more sense.

This option works only if `Say username before message` is enabled, too.

> #### Ignore messages starting with

Ignore messages starting with any of these characters to prevent
  commands being spoken.

> #### Replace these with spaces

For each character in here, replaces each occurrence of it with a
  white space, so TTS will not read them literally.

> #### Emote prefix, don't read this

If you want to read your own channel emotes name as words and skip prefix,
  specify it here.

Be sure it is not a common char sequence used in your TTS, otherwise
  it would became mute at any occurrence, also outside emotes' name.  
It is case sensitive.  
Setting the option `First emotes' name letter is uppercase, after prefix`
  could help.

Left empty if you don't want to use this option.

> #### First emotes' name letter is uppercase, after prefix

Check this if the first letter of your emotes' name (the first letter
  after your channel prefix) is uppercased.
Checking this flag could help `Emote prefix, don't read this` option
  to not be too invasive and to create less oddities.

> #### Alias to apply to words or nicknames

You can set aliases for words or nicknames (only full words, no partials),
  if you want them to be spelled differently.  
Expressed with 'Word:Alias' or 'Name:Alias' couples separated by semicolon.

Note1: It also applies on 'Say username' option.  
Note2: Blacklist checks will be made on original nicknames.

> #### Character series to swap

Swaps series of characters with another series, if you want them to be
  spelled differently.  
Expressed with 'Chars:Swaps' couples separated by semicolon.

Note: at the contrary of aliases, as for the option above, this option
  is case sensitive but swaps also partial words, so it could be invasive
  and create oddities.  
Be sure to use the most rich series of characters possible.

> #### Cut automatically to Max chars allowed

Check this to let the script automatically cut text to max characters
  allowed, to be able to play TTS anyway.

Otherwise the text will not be read if too long (silently ignored).

> #### Max chars allowed

Max characters allowed to submit to TTS.

> #### Write in chat the text to be read

If enabled, the bot will textually write in chat the text TTS will read.

### Command Configuration

> #### Command

Command for users to write in chat to say something with TTS.  
Aka: the chat command which activate this TTS script.

> #### Permission level

Set the permission level necessary to be enabled to use the command.

> #### Global cooldown (seconds)

Cooldown applied globally to everybody after the command is used.

> #### User cooldown (seconds)

Cooldown applied for each user after he/she used the command.

> #### Cost

Command cost for users.

Note:  
  From version 1.06 this applies no more to the channel owner itself.  
  But due to a bug, some version of the Chatbot need a refresh on the
    scripts section (the icon with a circled arrow on top right) after
    bot's startup, otherwise it will not be able to recognize channel name.

### Command Messages

> #### Missing text

Check this to shown a message when someone tries to issue the command
  without a text to be read.

> #### Missing text message

Message shown when someone tries to issue the command without a text
  to be read.

> #### Permissions

Check this to shown a message when someone tries to issue the command
  without enough permissions.

> #### Permissions message

Message shown when someone tries to issue the command without enough
  permissions.

> #### Cooldown

Check this to shown a message when someone tries to issue the command but
  it is still on cooldown.

> #### Cooldown message

Message shown when someone tries to issue the command but it is still on
  cooldown.

> #### User Cooldown

Check this to shown a message when someone tries to issue the command
  while they are on cooldown.

> #### User Cooldown message

Message shown when someone tries to issue the command while they are on
  cooldown.

> #### Cost (show error message)

Check this to shown a message when someone tries to issue the command
  without enough points.

> #### Cost message

Message shown when someone tries to issue the command without enough points.

> #### Too long

Check this to shown a message when someone tries to issue the command with
  a message too long.

> #### Too long message

Message shown when someone tries to issue the command with a message too long.

{0} is where user's nickname will go.

> #### Blacklisted

Check this to shown a message when someone banned tries to issue a command.

> #### Blacklisted message

Message shown when someone banned tries to issue a command.

{0} is where user's nickname will go.

### Moderator Commands

> #### Skip currently playing text command

Use this command to skip the currently playing text to speech,
  like in case of a troll.

You can even skip all texts in queue containing a reference word,
  if any word is specified after the command.

> #### Skip next text command in queue, without need the current one ends up

Use this command to skip the next text to speech in queue, like in case
  of a troll, without need to wait the current one to ends up.

> #### Skip the whole text command queue, and start a new one

Use this command to skip the whole text to speech queue, for any reason,
  like going to close the session.

> #### Pauses\Unpauses the script

Use this command to pause or unpause the script.

Note: if the TTS is already reading, it will still finish the current reading.

> #### Keep queuing on pause

Check this to keep queuing new TTS messages even if you paused the script.

All queued messages will be read sequentially after unpaused, you can still
  skip them with skip commands.

Note: if the TTS is already reading, it will still finish the current reading.

> #### Keep\Unkeep queuing on pause

Switches and reswitches settings for "Keep queuing on pause" flag,
  only for the current session.

Next session will start as for setting on flag "Keep queuing on pause".

> #### Add user to blacklist command

Use this command to add an user to the blacklist

> #### Remove user from blacklist command

Use this command to remove an user from the blacklist

> #### Moderator permission

Allow these users to blacklist/unblacklist people

> #### Allow bannable moderators

Check this to make any moderator bannable from using Moderator commands.

### Moderator Commands Messages

> #### Missing target

Check this to shown when moderator forget to specify the target user.

> #### Missing target message

Message shown when moderator forget to specify the target user.

{0} is where the command name will go.

> #### TTS paused

Check this to shown a message when TTS is paused with pause command.

> #### TTS paused message

Message shown when moderator paused TTS with pause command.

> #### TTS unpaused

Check this to shown a message when TTS is unpaused with pause command.

> #### TTS unpaused message

Message shown when moderator unpaused TTS with pause command.

> #### TTS keeps queuing on pause

Check this to shown a message when TTS keeps queuing on pause
  after keep command.

> #### TTS keeps queuing on pause message

Message shown when moderator set TTS to keeping queuing on pause
  after keep command.

> #### TTS stops queuing on pause

Check this to shown a message when TTS keeps stops queuing on pause
  after keep command.

> #### TTS stops queuing on pause message

Message shown when moderator set TTS to stop queuing on pause
  after keep command.

> #### Successfully blacklisted

Check this to shown when moderator succeed to ban an user.

> #### Successfully blacklisted message

Message shown when moderator succeed to ban an user.

{0} is where user's nickname will go.

> #### Unsuccessfully blacklisted

Check this to shown when moderator tries to ban an already banned user.

> #### Unsuccessfully blacklisted message

Message shown when moderator tries to ban an already banned user.

{0} is where user's nickname will go.

> #### Successfully unbanned

Check this to shown when moderator succeed to unban an user.

> #### Successfully unbanned message

Message shown when moderator succeed to unban an user.

{0} is where user's nickname will go.

> #### Unsuccessfully unbanned

Check this to shown when moderator tries to ban a not banned user.

> #### Unsuccessfully unbanned message

Message shown when moderator tries to unban a not banned user.

{0} is where user's nickname will go.

### TTS Configuration

> #### TTS Language

Change Text To Speach Language.

> #### Alter volume?

Alter volume of Text To Speach generated file?

You could want to disable this expecially if volume changes generate
  oddities with custom TTS webservices.

> #### TTS Volume

Change Text To Speach volume.

> #### Alter pitch?

Alter pitch of Text To Speach generated file?

You could want to disable this expecially if pitch changes generate
  oddities with custom TTS webservices.

Note: Pitch will still influece speed final effect,
  if alter speed is enabled.

> #### TTS % Pitch

Change Text To Speach default pitch of voice.

> #### Alter speed?

Alter speed of TTS generated file?

You could want to disable this expecially if speed changes generate
  oddities with custom TTS webservices.

Note: Pitch value will also be involted, even if alter pitch is disabled.

> #### TTS % Speed

Change Text To Speach default speed of voice.

> #### Max length (seconds)

Limit the duration the Text To Speach will be speaking.

> #### Settings update confirmation

Text To Speach will say this sentence to confirm settings are
  updated successfully.

### TTS Multi Languages

> #### Allows multi languages?

It enables codes (from `Set all custom languages available`) to allow users
  to request TTS for different languages.

> #### Set all custom languages available

Set all custom languages available, with their "in chat" codes.

I.e.: `Language: code; Language2: code2;`  
Like: `English (UK): en-GB; English (US): en-US; Italian: it-IT;`

Note:  
  Those codes have to actually be codes used by your TTS webservice
    to define the TTS language to read... not just fantasy codes.  
  The Language name, instead, it's up to your fantasy, but just try to not
    make the text too long, I have no idea about Chatbots limits on length.

Those codes are not mandatory to be used.

In case an user doesn't use any of those codes, the main language setted
  for this script will be used by default, as always.

If used, the code have to follow the TTS Command itself (if `Read ALL chat`
  option is not active), as first parameter before the text to be read.  
I.e.: > `!tts it-IT It's a me: Mario!`  
This will make Italian language bot read `It's a me: Mario!`...  
  if `it-IT` code is actually configured in your settings, and `!tts` is still
  the script's main `Command` setted into `Command configuration` section.  
Otherwise obviously the `Command` have to be the one you setted and so
  for multilanguage codes: this was just an example with default options.

In case `Read ALL chat` option is active, the code will have to be first
  thing wrote into the message, still before the text to be read.  
I.e.: > `it-IT It's a me: Mario!`  
Unfunny note: the result will not remember Super Mario so much, sorry.

Note:  
  For now, the `Say this after the username` option in General
    section is ignored when a custom multilanguage is used.  
  While the option `Say username before message` still works.

Pro-Tip:  
Seeing the above note, you can put a code also for the same
  main language you already setted into TTS Configuration section.

By doing so and using the language code, the TTS will read the message
  without the `Say this after the username` word, and the whole TTS will
  sound as the describing of an action made by the user.

Let's make this example:

* The main language setted is `English US`.  
  `Say username before message` is active.  
  `Say this after the username` is `says`.  
  `Command` option is `!tts`.  
  Also Multilanguage option is enabled and between the others, there's also
    a code setted for the main language itself: `English (US): en-US;`.
* An user named `ThisIsMyNick` tries to use the Command:
  * if he writes > `!tts is going crazy with this awesome TTS script`
    the TTS will read:  
      `ThisIsMyNick says is going crazy with this awesome TTS script`
  * if he writes > `!tts en-US is going crazy with this awesome TTS script`
    the TTS will read:
      `ThisIsMyNick is going crazy with this awesome TTS script`

As you can see, the second example seems like TTS is describing
  an user's action.

> #### Codes are case sensitive?

If enabled, languages' code uppercases and lowercases have to be respected.
Otherwise codes will be case unsensitive (it-it or it-IT would both work).

> #### Show available languages?

If enabled, the following command `Show available languages command`
  will be activated for chatters.

> #### Show languages command

Litellary writes in chat your custom languages setting,
  to let chatters know possible languages.

> #### Show languages cooldown (secs)

Cooldown applied to `Show available languages command`.

### TTS Server

> #### Custom parameters

These parameters will fill the webservice call, replacing in order {2}, {3}
  and so on.  
They have to be enclosed in quotation marks.

{0} and {1} are not included because they'll be `{0} = text to read`
  and `{1} = language`.

If your webservice language format is different than default
  (i.e not: 'en-GB', 'it-IT', 'fil-PH') you can set it as custom parameter.

> #### Webservice

The webservice to be called for TTS services.

{0}, {1} and so on will be replaced by parameters, as explained for
  previous field.

> #### Audio format

Audio file extention generated by Text To Speach service.

Note: I'm not sure on how many audio formats are supported.  
If it seems not to work, try to set your TTS webservice to generate a
  different audio format.  
For now I just tested .mp3 and .wav .
