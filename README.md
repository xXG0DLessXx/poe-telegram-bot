# README - Poe.com Telegram Bot

This is a Telegram bot that allows you to interact with AI models from the website poe.com. The bot is built using Python, the Telegram Bot API, and the poe library.

## Features
- Select and use different AI models from poe.com
- Start, reset, and clear conversations with the selected model
- Send messages to the selected model and receive responses
- Help command to show available commands
- Works in both private chats and group chats
- Knows your Telegram nickname and @username

## Setup
1. Clone this repository to your local machine.
2. Install Python 3.6 or higher.
3. Create a `.env` file in the root directory of the project and add the following environment variables:
   - `BOT_TOKEN` - Your Telegram bot token obtained from BotFather.
   - `POE_COOKIE` - Your poe.com "p-b" cookie obtained from your browser's developer tools.
   - `DEFAULT_MODEL` - (OPTIONAL) Allows setting a default model to be used when starting the bot. Default if not set, is "capybara" also known as Sage.
   - `POE_HEADERS` - (OPTIONAL) Sets the headers used for the browser agent (Lowers chance of getting banned if you use the headers of your own browser). You can get them [here](https://headers.uniqueostrich18.repl.co/).
   - `ALLOWED_USERS` - (OPTIONAL) Comma-separated list of allowed Telegram user IDs. If specified, only these users will be allowed to use the bot. If not specified, all users will be allowed.
   - `ALLOWED_CHATS` - (OPTIONAL) Comma-separated list of allowed Telegram chat IDs. If specified, the bot can be used by anyone in these chats. If not specified, the bot can be used by anyone in any chat.
### Example .env
```
BOT_TOKEN=<YOUR TELEGRAM TOKEN>
POE_COOKIE=<YOUR POE.COM p-b COOKIE>
DEFAULT_MODEL=<MODEL IDENTIFIER e.g one of these: {'capybara': 'Sage', 'beaver': 'GPT-4', 'a2_2': 'Claude+', 'a2': 'Claude', 'chinchilla': 'ChatGPT', 'nutria': 'Dragonfly'}>
POE_HEADERS=<(OPTIONAL LEAVE EMPTY IF NOT DESIRED) YOUR BROWSER HEADERS (Example: "{
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "en-US,en;q=0.5",
  "Te": "trailers",
  "Upgrade-Insecure-Requests": "1"
}")>
ALLOWED_USERS=<COMMA-SEPARATED LIST OF ALLOWED USER IDS (Exampe ID's:1234567890,9876543210)>
ALLOWED_CHATS=<COMMA-SEPARATED LIST OF ALLOWED CHAT IDS (Example ID's:-1001234567890,-1009876543210)>
```

7. Run the bot using `python3 start.py`. (It should install all needed dependencies automatically in a virtual environment).

## Usage
- `/start` - Start the bot and receive a welcome message.
- `/purge` - Purge the entire conversation with the selected bot/model.
- `/reset` - Clear/Reset the context with the selected bot/model.
- `/select` - Select a bot/model to use for the conversation.
- `/help` - Show the available commands.
- Send any text message to the bot and receive a response from the selected bot/model. In group chats, the bot will only respond to messages that mention the bot or are replies to its messages.

### Group Chat
- In group chats, the bot will only respond to messages that mention the bot or are replies to its messages. To use the bot in a group chat:

1. Mention the bot in your message by using the @ symbol followed by the bot's username (e.g. @YourBotUsername Hello!).
2. The bot will receive a mention notification and process your message, sending a response to the group chat.
3. Alternatively, reply to one of the bot's messages in the group chat. 
- Note that if the bot is not responding to your messages in a group chat, make sure that you have mentioned the bot correctly or replied to one of its messages.

## Credits
- The poe library used in this project is a reverse-engineered Python API wrapper for Quora's Poe, created by [ading2210](https://github.com/ading2210) and licensed under the GNU GPL v3. It can be found [here](https://github.com/ading2210/poe-api).
- The python-telegram-bot library is used to interact with the Telegram Bot API.
- The rest of the code in this project has been written by me with the help of ChatGPT, since this is my first Python project.

## Contributions
Contributions are welcome! If you find a bug or want to add a new feature, feel free to create an issue or submit a pull request. Just be aware that this is just a fun side project for me, so issues/features may or may not be fixed/added.

## License
This program is licensed under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.txt).

### Copyright Notice:
```
A basic Poe.com Telegram bot.
Copyright (C) 2023 G0DLess

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```