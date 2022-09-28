# discord-bot-csgo
This is a Discord bot to help skin investors in the CS:GO game written with Discord.py. It shows the price history of an inputted item.

## Technology Choices

I chose Discord.py rather than Discordjs as an exercise to learn about applications of Python and API calls.

## Command List and Example Outputs

### Price Command - "$price <"skin name"> \<currency>" <br />
![Price Message](https://raw.githubusercontent.com/RyanRepositories/discord-bot-csgo/main/pictures/price_command.PNG)

### Help Command - "$help \<Command>" <br />
![Help Message](https://raw.githubusercontent.com/RyanRepositories/discord-bot-csgo/main/pictures/help.PNG)

### Sample Help Command - "$help price or $price" <br />
![Price-Help Message](https://raw.githubusercontent.com/RyanRepositories/discord-bot-csgo/main/pictures/price_help.PNG)

### If anything but those commands above are used, it shows this error message: <br />
![Error Message](https://raw.githubusercontent.com/RyanRepositories/discord-bot-csgo/main/pictures/error.PNG)

## How to Install and Use
1. Install discord.py through `pip install -U discord.py`.
2. Create an API key on Discord and configure it to be a bot. Tutorial by WriteBots here: https://www.writebots.com/discord-bot-token/.
3. Input your new API key into the script file.
4. Run the script file.

### NOTE: You have to replace "token" at the bottom of the main.py file with your own Discord API token, as that is what communicates with the Discord API and what makes the Discord bot work. To get your own Discord API token, here is a tutorial by WriteBots: https://www.writebots.com/discord-bot-token/. Never share this token with anyone.
