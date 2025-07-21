# YTControlsMC
A small application I made allowing YouTube chatters to interact with a Minecraft Server World using RCON
*This uses @DougDougGithub's TwitchPlays code but for YouTube chat and controls a Minecraft server using RCON*
*This is only available for Java edition of Minecraft, NOT bedrock.*

# How to set up a Minecraft Java Server

*this is only for your local network, friends will not be allowed to play unless you portforward which will NOT be explained here, and as it risks exposing your IP address*

If you want a YouTube video version, here is a YouTube link to a tutorial by Kevin Stratvert https://www.youtube.com/watch?v=sz6kqZPVsfM

1. I recommend downloading a Minecraft server from papermc.io as the servers are better than vanilla servers and can support plugins.
https://papermc.io/downloads

After downloading the server jar file which might look like. `paper-1.21.8-4.jar`

*Numbers may vary depending on which version of paper you download, in this case, this is for Minecraft Java 1.21.8*

2. After downloading, going to your file explorer, create a new folder for your Minecraft server.

3. Simply put the server jar file into this newly created folder.

4. In the address bar above (where you see the directory C:\etc), replace it with `cmd` and hit enter.

5. This should open a command prompt, here, we will check if we have java installed.

6. To check if you have java, run `java -version` in the command prompt. If you get `'java' is not recognized as an internal or external command, operable program or batch file`, then we will need to install Java.

7. To install java, you will need to run `winget install Microsoft.OpenJDK.21` in commmand prompt. (this is Java for the most recent version)

8. After installing Java, you might need to close and re open the command prompt by using step 4, then here run the command `java -jar server.jar --nogui`

9. After running the command, a lot of text is going to appear, but or server hasn't started yet, we will need to agree to the server EULA file which we can see in our folder that we created with the server jar.

10. In the EULA file, change `eula=false` to `eula=true` then save (ctrl + s)

11. Then back in command prompt, run the `java -jar server.jar` command, to start up our server. A windows security message might appear, make sure to click `Allow`

12. Your Minecraft server is now almost finished! We are now going to create a new file so we don't have to open command prompt everytime we want to start our server.

13. Close the server and command prompt windows, then we will create a new text document (Make sure you have "show file extensions", to enable, go to "view > show > file name extensions")

14. replace the text file `New Text Document.txt` with `start.bat` then save, if you get a warning about the file might becoming unusable and if we are sure that we want to change it, press `Yes`

15. Next, right click and edit it within notepad. In here, paste the following code

`@ECHO OFF`

`java -Xms2G -Xmx8G -jar server.jar`

`Pause`

***MAKE SURE TO CHANGE `server.jar` TO THE NAME OF THE MINECRAFT SERVER FILE YOU DOWNLOADED, in this case, we would change it to `paper-1.21.8-4.jar`***

*this code will automatically run the server without us having to open command prompt every time which is neat!*

*in the second line, `-Xms2G -Xmx4G` is the amount of ram you want to dedicate to your server, in this case, it's 2 for the minimum and 8 for the max, change these to your likings but make sure you have enough ram!*

16. After pasting the code, make sure to save the file (ctrl + s) and close notepad.

After that, the server is done! if you want to change server settings, you can open the server.properties file (with notepad as well) and configure it to your liking. To run the server now, just simply run the `start.bat` file!

*to connect to your server locally, go to Minecraft and to the multiplayer tab, here add a server, and for the server address, make sure to make it as `localhost`*

# YouTube Livestream Chat Integration Into Minecraft Instructions

1. Open config.json and fill in your YouTube channel info (CHANNEL ID and STREAM URL) and RCON settings.

*To find your channel ID, go to your profile > settings > advanced settings > Channel ID*

*Your RCON settings must match your Minecraft server's RCON, I recommend using a local server*

*IF using a local server, no need to change the host and make sure the port and password matches with the server's server.properties file*

2. Change PLAYER_USERNAME to your Minecraft IGN (or @a for all player, although not tested)

3. Save the file using Ctrl + S

4. Double-click the .exe to launch the controller.

5. Viewers can now type chat commands like “give diamond 5” or “effect speed 30 3”

6. Simply close the command prompt whenever you want your chat to stop.

**PREDETERMINED COMMANDS**

This script has already commands built in that viewers can do

These built in commands feature "give", "summon", "spawn", and "effect"

All viewers simply need to do is type the keyword, then whatever they want to give you

ex: `give diamond 30`

in the example, we are giving 30 diamonds. 

If you do not receive the item, it is most likely how the item is formatted in minecraft. 

For example, if a viewer wants to give you an `eye of ender`, they would actually need to type `ender eye` as in minecraft, it is formatted as `minecraft:ender_eye`

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

# Source Code
You will need to install Python 3.9 or above
You will also need to install these libraries:

python -m pip install mcron

python -m pip install requests

After that, you can modify the configurations like you would with the app in the three json files

If you want to modify how the script works or improve on it, You can edit the **YTControlsWorld.py** script
