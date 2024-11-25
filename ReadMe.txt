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
 Sometimes Streamlabs Chatbot doesn't trigger ReloadSettings method on new
  settings save from Save Settings GUI button.
 If you can't hear TTS say the "Configuration updated successfully" sentence
  (by default "Configuration updated successfully") probably new settings are
  saved, but you can't be sure if they're already loaded / applied into
  current Chatbot session.
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

- Script: The ReNew TTS script
- Version: 1.0.4
- Description: Text to speech with Google translate voice,
   or your own custom TTS webservice
- Change: Fixed a bug with Blacklist file loading;
   Fixed a bug with TTS stuttering aliases with spaces;
   Added permission level VIP (includes subscribers and moderators);
   Added setting to keep or not keep queing on pause
- Services: Twitch, Youtube
- Overlays: None
- Made By: @Patcha_it
- Update Date: 2023/01/24

## Changelog

### Versions by LuisSanchezDev (TheNewTTS)
- 2019/11/12 v1.0.0
  - Initial release
- 2019/11/27 v1.0.1
  - Fixed sound not playing
- 2019/12/03 v1.1.0
  - Added max length in seconds
- 2019/12/08 v1.2.0
  - Added blacklist
- 2019/12/09 v1.2.1
  - Fixed Youtube/Mixer blacklist comparison against user ID instead of username
- 2020/08/29 v2.0.0
  - Added a say username before message option
  - Added a skip command
  - Fixed sometimes skipping messages
  - Fixed script stopped working suddenly
- 2020/10/05 v2.1.0 -
  - Added a clean repeated words/emotes option
  - Added a clean repeated letters option
  - Added a clean and replace links option
  - Added a ignore messages starting with a character option

### Versions by Patcha (TheRenewTTS)
- 2022/11/20 v1.0.0
  - Using reworked python custom libraries for TTS download & play,
     which can be shared with other scripts without conflicts
  - Possibility to set an own custom TTS webserver (if you have it)
  - `Clean repeated words/emotes` option will no longer remove
     punctuation from sentences
     + you can now set a maximum allowed amount of repetitions
     + it's no more case sensitive
  - `Clean repeated letters` option will now replace repetitions
     with a double letter
     + it's no more case sensitive
  - `Ignore messages starting with` option now can set multiple
     characters, which means it still checks first character,
     but compares with each one setted into a series
  - Option to replace each char in a series with spaces
     (if you don't want TTS to read them literally)
  - Option to replace some words/usernames with other words/aliases
  - Option to replace some chars sequence with another sequence,
     if you need to correct TTS pronunciation/spelling
     (invasive: could create oddities)
  - Option to set channel's emotes prefix, to be skipped and try
     to read only emotes names
     (case sensitive, but invasive: could create oddities
      if that prefix is a common chars sequence)
     + there's an option to filter only prefixes followed
      by uppercase letter (it helps prevent most oddities)
  - Option to set a max amount of chars lower than 200
     + option to cut and not skip messages too long
  - Option to disable/enable each command's message reply
     + new command messages to be able to customize
     + (also for moderator commands)
  - New skip options for moderators:
     - if they add an argument to standard skip command, it will
       skip all TTS with such text inside from current queue
     - a new command to skip `next` TTS, while the current one
       is still playing
     - a new command to skip the whole TTS queue and start a new
  - Commands are no more case sensitive
  - Usernames are no more case sensitive
  - Option to make moderators bannable from TTS
     (it means they won't use nor TTS nor moderator commands)
  - Options to disable volume, pitch and speed alterators
     (useful for custom TTS webserver)
  - Script files rearranged into subfolders
- 2023/01/05 v1.0.1
  - Fixed bug skipping first word on Read ALL
  - Allows to force read lowercased or uppercased
- 2023/01/07 v1.0.2
  - Fixed a bug with message Cost set to 0
- 2023/01/15 v1.0.3
  - Added a customizable !pause command
- 2023/01/24 v1.0.4
  - Fixed a bug with Blacklist file loading
  - Fixed a bug with TTS stuttering aliases with spaces
  - Added permission level VIP (includes subscribers and moderators)
  - Added setting to keep or not keep queing on pause

## Getting Started

### Prerequisites

Have an installation of Streamlabs Chatbot, already logged in to your accounts.
* [Download Streamlabs Chatbot](https://streamlabs.com/desktop-chatbot)

Follow this tutorial to prepare your Streamlabs Chatbot installation to accept scripts.
* [[Streamlabs Chatbot] Scripts Explained by Castorr91](https://www.youtube.com/watch?v=l3FBpY-0880)

### Installation

1. Download the latest version of the script.
2. If you haven't already, open your Streamlabs Chatbot and log in to your Streamer and Bot accounts.
3. On the left side, wait for the `Scripts` tab to pop up and click it.
4. On the top right corner of the window, next to the reload button is an import script button (Arrow pointing right to a box) and select the script downloaded before.
5. You will receive a message box confirming the import, accept it.
6. The window will update and show the `The Renew TTS` script.
7. Click on the `The Renew TTS` name to see the configuration pane.

## Settings

Don't be scared about so many options, most of them are not mandatory to be
 customized. For the most, default options are enough ok.

For each option I'll note if and what changes there are, compared to the
 original TheNewTTS script settings from Luis Sanchez.

### General

> #### Read ALL chat
Check this to read all chat disregarding the command.

IF YOU ARE USING THIS FEATURE MAKE SURE TO SET A FAST SPEED
 SO THE CHATBOT CAN KEEP UP!

Also note that this feature may prevent the use of some other options.

[Unchanged]

> #### Force lower or upper case
Set this if you want TTS to read lowercase (could avoid acronyms
 reading on uppercase words) or uppercase (could read words as acronym).

[Brand new]

> #### Clean repeated letters
Prevent repeated letters to be spoken and only speak them twice.

Example: noooooooo -> noo .

[Before it used to speak them once, i.e.: noooo -> no .]

> #### Clean repeated words/emotes
Prevent repeated words/emotes to be spoken and only speak them as max
 as setted in the option `Max words/emotes repeat allowed`.

Example: :Kappa: :Kappa: :Kappa: :Kappa: :Kappa: :Kappa: -> :Kappa:

[Before it used to remove all punctuation, now punctuation is preserved.  
Before it used to speak them only once, now you can set the a custom amount
 with option below.]

> #### Max words/emotes repeat allowed
How many times you allow to repeat a word/emote, if `Clean repeated
 words/emotes` option is enabled.

[Brand new]

> #### Clean links
Prevent links to be spoken and say the replacement text instead.

[Unchanged]

> #### Replace links with
If `Clean links` is checked, links will be replaced with this text.

[Unchanged]

> #### Say username before message
Check this to say the username before the message.

[Unchanged]

> #### Say this after the username
Append this text to the username so the TTS makes more sense.

This option works only if `Say username before message` is enabled, too.

[Unchanged]

> #### Ignore messages starting with
Ignore messages starting with any of these characters to prevent
 commands being spoken.

[Before it accepted a single character, now it accept multiple chars
 and it will check each of them.]

> #### Replace these with spaces
For each character in here, replaces each occurrence of it with a
 white space, so TTS will not read them literally.

[Brand new]

> #### First emotes' name letter is uppercase, after prefix
Check this if the first letter of your emotes' name (the first letter
 after your channel prefix) is uppercased.
Checking this flag could help `Emote prefix, don't read this` option
 to not be too invasive and to create less oddities.

[Brand new]

> #### Emote prefix, don't read this
If you want to read your own channel emotes name as words and skip prefix,
 specify it here.

Be sure it is not a common char sequence used in your TTS, otherwise
 it would became mute at any occurrence, also outside emotes' name.  
It is case sensitive.  
Setting the option `First emotes' name letter is uppercase` could help.

Left empty if you don't want to use this option.

[Brand new]

> #### Alias to apply to words or nicknames
You can set aliases for words or nicknames (only full words, no partials),
 if you want them to be spelled differently.  
Expressed with 'Word:Alias' or 'Name:Alias' couples separated by semicolon.

Note1: It also applies on 'Say username' option.  
Note2: Blacklist checks will be made on original nicknames.

[Brand new]

> #### Character series to swap
Swaps series of characters with another series, if you want them to be
 spelled differently.  
Expressed with 'Chars:Swaps' couples separated by semicolon.

Note: at the contrary of aliases, as for the option above, this option
 is case sensitive but swaps also partial words, so it could be invasive
 and create oddities.  
Be sure to use the most rich series of characters possible.

[Brand new]

> #### Cut automatically to Max chars allowed
Check this to let the script automatically cut text to max characters
 allowed, to be able to play TTS anyway.

Otherwise the text will not be read if too long (silently ignored).

[Brand new: before it always discarded longer texts.]

> #### Max chars allowed
Max characters allowed to submit to TTS.

[Brand new: before it was always 200.]

### Command Configuration

> #### Command
Command for users to write in chat to say something with TTS.  
Aka: the chat command which activate this TTS script.

[Unchanged]

> #### Permission level
Set the permission level necessary to be enabled to use the command.

[Unchanged]

> #### Global cooldown (seconds)
Cooldown applied globally to everybody after the command is used.

[Unchanged]

> #### User cooldown (seconds)
Cooldown applied for each user after he/she used the command.

[Unchanged]

> #### Cost
Command cost.

[Unchanged]

### Command Messages

> #### Missing text
Check this to shown a message when someone tries to issue the command
 without a text to be read.

[Brand new, was always on before.]

> #### Missing text message
Message shown when someone tries to issue the command without a text
 to be read.

[Brand new, could not be customized before.]

> #### Permissions
Check this to shown a message when someone tries to issue the command
 without enough permissions.

[Brand new, was always on before.]

> #### Permissions message
Message shown when someone tries to issue the command without enough
 permissions.

[Unchanged]

> #### Cooldown
Check this to shown a message when someone tries to issue the command but
 it is still on cooldown.

[Brand new, was always on before.]

> #### Cooldown message
Message shown when someone tries to issue the command but it is still on
 cooldown.

[Unchanged]

> #### User Cooldown
Check this to shown a message when someone tries to issue the command
 while they are on cooldown.

[Brand new, was always on before.]

> #### User Cooldown message
Message shown when someone tries to issue the command while they are on
 cooldown.

[Unchanged]

> #### Cost
Check this to shown a message when someone tries to issue the command
 without enough points.

[Brand new, was always on before.]

> #### Cost message
Message shown when someone tries to issue the command without enough points.

[Unchanged]

> #### Too long
Check this to shown a message when someone tries to issue the command with
 a message too long.

[Brand new, was always on before.]

> #### Too long message
Message shown when someone tries to issue the command with a message too long.

{0} is where user's nickname will go.

[Brand new, could not be customized before.]

> #### Blacklisted
Check this to shown a message when someone banned tries to issue a command.

[Brand new, was always on before.]

> #### Blacklisted message
Message shown when someone banned tries to issue a command.

{0} is where user's nickname will go.

[Brand new, could not be customized before.]

### Moderator Commands

> #### Skip currently playing text command
Use this command to skip the currently playing text to speech,
 like in case of a troll.

You can even skip all texts in queue containing a reference word,
 if any word is specified after the command.

[Before it couldn't use an argument to skip all text containing a reference word.]

> #### Skip next text command in queue, without need the current one ends up.
Use this command to skip the next text to speech in queue, like in case
 of a troll, without need to wait the current one to ends up.

[Brand new]

> #### Skip the whole text command queue, and start a new one.
Use this command to skip the whole text to speech queue, for any reason,
 like going to close the session.

[Brand new]

> #### Pauses\Unpauses the script
Use this command to pause or unpause the script.

Note: if the TTS is already reading, it will still finish the current reading.

[Brand new]

> #### Keep queuing on pause
Check this to keep queuing new TTS messages even if you paused the script.

All queued messages will be read sequentially after unpaused, you can still
 skip them with skip commands.

Note: if the TTS is already reading, it will still finish the current reading.

[Brand new]

> #### Keep\Unkeep queuing on pause
Switches and reswitches settings for "Keep queuing on pause" flag,
 only for the current session.

Next session will start as for setting on flag "Keep queuing on pause".

[Brand new]

> #### Add user to blacklist command
Use this command to add an user to the blacklist

[No more case sensitive]

> #### Remove user from blacklist command
Use this command to remove an user from the blacklist

[No more case sensitive]

> #### Moderator permission
Allow these users to blacklist/unblacklist people

[Unchanged]

> #### Allow bannable moderators
Check this to make any moderator bannable from using Moderator commands.

[Brand new]

### Moderator Commands Messages

> #### Missing target
Check this to shown when moderator forget to specify the target user.

[Brand new, was always on before.]

> #### Missing target message
Message shown when moderator forget to specify the target user.

{0} is where the command name will go.

[Brand new, could not be customized before.]

> #### TTS paused
Check this to shown a message when TTS is paused with pause command.

[Brand new]

> #### TTS paused message
Message shown when moderator paused TTS with pause command.

[Brand new]

> #### TTS unpaused
Check this to shown a message when TTS is unpaused with pause command.

[Brand new]

> #### TTS unpaused message
Message shown when moderator unpaused TTS with pause command.

[Brand new]

> #### TTS keeps queuing on pause
  Check this to shown a message when TTS keeps queuing on pause
    after keep command.

[Brand new]

> #### TTS keeps queuing on pause message
  Message shown when moderator set TTS to keeping queuing on pause
    after keep command.

[Brand new]

> #### TTS stops queuing on pause
  Check this to shown a message when TTS keeps stops queuing on pause
    after keep command.

[Brand new]

> #### TTS stops queuing on pause message
  Message shown when moderator set TTS to stop queuing on pause
    after keep command.

[Brand new]

> #### Successfully blacklisted
Check this to shown when moderator succeed to ban an user.

[Brand new, was always on before.]

> #### Successfully blacklisted message
Message shown when moderator succeed to ban an user.

{0} is where user's nickname will go.

[Brand new, could not be customized before.]

> #### Unsuccessfully blacklisted
Check this to shown when moderator tries to ban an already banned user.

[Brand new, was always on before.]

> #### Unsuccessfully blacklisted message
Message shown when moderator tries to ban an already banned user.

{0} is where user's nickname will go.

[Brand new, could not be customized before.]

> #### Successfully unbanned
Check this to shown when moderator succeed to unban an user.

[Brand new, was always on before.]

> #### Successfully unbanned message
Message shown when moderator succeed to unban an user.

{0} is where user's nickname will go.

[Brand new, could not be customized before.]

> #### Unsuccessfully unbanned
Check this to shown when moderator tries to ban a not banned user.

[Brand new, was always on before.]

> #### Unsuccessfully unbanned message
Message shown when moderator tries to unban a not banned user.

{0} is where user's nickname will go.

[Brand new, could not be customized before.]

### TTS Configuration

> #### TTS Language
Change Text To Speach Language.

[Unchanged]

> #### Alter volume?
Alter volume of Text To Speach generated file?

You could want to disable this expecially if volume changes generate
 oddities with custom TTS webservices.

[Brand new, was always on before.]

> #### TTS Volume
Change Text To Speach volume.

[Now it allows to change one point at time, before it was 5 at time.  
Before it was from 15 to 200, not the range is from 1 to 100.]

> #### Alter pitch?
Alter pitch of Text To Speach generated file?

You could want to disable this expecially if pitch changes generate
 oddities with custom TTS webservices.

Note: Pitch will still influece speed final effect,
 if alter speed is enabled.

[Brand new, was always on before.]

> #### TTS % Pitch
Change Text To Speach default pitch of voice.

[Now it allows to change one point at time, before it was 5 at time]

> #### Alter speed?
Alter speed of TTS generated file?

You could want to disable this expecially if speed changes generate
 oddities with custom TTS webservices.

Note: Pitch value will also be involted, even if alter pitch is disabled.

[Brand new, was always on before.]

> #### TTS % Speed
Change Text To Speach default speed of voice.

[Now it allows to change one point at time, before it was 5 at time]

> #### Max length (seconds)
Limit the duration the Text To Speach will be speaking.

[Unchanged]

> #### Settings update confirmation
Text To Speach will say this sentence to confirm settings are
 updated successfully.

[Brand new, could not be customized before.]

### TTS Server
[This section is totally brand new.]

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
