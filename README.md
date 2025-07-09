# YTControlsMC
A small application I made allowing YouTube chatters to interact with a Minecraft Server World using RCON
*This uses @DougDougGithub's TwitchPlays code but for YouTube chat and controls a Minecraft server using RCON*

# YouTube Livestream Chat Integration Into Minecraft Instructions

1. Open config.json and fill in your YouTube channel info (CHANNEL ID and STREAM URL) and RCON settings.
*To find your channel ID, go to your profile > settings > advanced settings > Channel ID*
*Your RCON settings must match your Minecraft server's RCON, I recommend using a local server*
*IF using a local server, no need to change the host and make sure the port and password matches with the server's server.properties file*
2. Change PLAYER_USERNAME to your Minecraft IGN (or @a for all player, although not tested)
3. Save the file using Ctrl + S
4. Double-click the .exe to launch the controller.
5. Viewers can now type chat commands like “give diamond 5” or “effect speed 30 3”
6. Simply close the command prompt when done

**IMPORTANT**: Do not rename or move the .json files, or the program may not work. No need to change the message rate, max queue length and max workers. 

Additonally, this config has limits for how many mobs can a viewer spawn on the player, how many items the viewer is allowed to give the player, and how long an effect can last and the amplifier.
These are caps, if the viewers try to go past this, it will just limit it to the set value.

**Note**: Amplifiers are added by one, so a viewer trying to give strength 2 (effect strength 30 **2**) would actually give strength 3.

# Commands Config File

Commands are commands you can set up that aren't available for the viewers by default (e.g. gamemode)
To add a command simply, 
1. Add a new line (make sure the previous line before that has a comma at the end)
2. In new "quotations", name it what you want viewers to refer to it as.
3. Add a colon : and add another "quotation" and have it refer to a Minecraft command (no need the /)
4. Save the file using Ctrl + S

**Note**: No need to add a give command as the app automatically handles this.

# Blacklists Config File 

Blacklists are things VIEWERS aren't allowed to do (e.g. give a certain effect, certain item, or summon a certain entity)

To add a new blacklisted term,

1. Add a comma inside the brackets of one of the blacklists (mobs, items, effects)
2. add new a "quotation" with the thing you want to block (for an item, it would simply be the item name, to check, turn on advanced tool tips in Minecraft Java [F3 + H])
*Note: no need to add the "minecraft:" part*
3. Save the file using Ctrl + S

# SOURCE CODE
You will need to install Python 3.9 or above
You will also need to install these libraries:

python -m pip install mcron
python -m pip install requests

After that, you can modify the configurations like you would with the app in the three json files

If you want to modify how the script works or improve on it, You can edit the **YTControlsWorld.py** script
