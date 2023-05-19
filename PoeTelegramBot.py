import logging
import poe
import os
import json
import random
import time
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler,
)

# Load environment variables from .env file
load_dotenv()

# Get environment variables
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
POE_COOKIE = os.getenv("POE_COOKIE")

# Check if environment variables are set
if not TELEGRAM_TOKEN:
    raise ValueError("Telegram bot token not set")
if not POE_COOKIE:
    raise ValueError("POE.com cookie not set")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Initialize the POE client
poe.logger.setLevel(logging.INFO)

poe_headers = os.getenv("POE_HEADERS")
if poe_headers:
    poe.headers = json.loads(poe_headers)

client = poe.Client(POE_COOKIE)

# Get the default model from the .env file
default_model = os.getenv("DEFAULT_MODEL")

# Set the default model
selected_model = default_model if default_model else "capybara"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a Poe.com Telegram Bot. Use /help for a list of commands.",
    )

async def purge(update: Update, context: CallbackContext):
    try:
        # Purge the entire conversation
        client.purge_conversation(selected_model)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Conversation purged.",
        )
    except Exception as e:
        await handle_error(update, context, e)

async def reset(update: Update, context: CallbackContext):
    try:
        # Clear the context
        client.send_chat_break(selected_model)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Context cleared.",
        )
    except Exception as e:
        await handle_error(update, context, e)

async def select(update: Update, context: CallbackContext):
    try:
        # Get the list of available bots
        bot_names = client.bot_names.values()

        # Create a list of InlineKeyboardButtons for each bot
        buttons = []
        for bot_name in bot_names:
            button = InlineKeyboardButton(text=bot_name, callback_data=bot_name)
            buttons.append([button])

        # Create an InlineKeyboardMarkup with the list of buttons
        reply_markup = InlineKeyboardMarkup(buttons)

        # Send a message to the user with the list of buttons
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please select a bot/model:",
            reply_markup=reply_markup,
        )
    except Exception as e:
        await handle_error(update, context, e)

async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query

    try:
        # Get the selected bot/model codename
        selected_bot = next(
            (k for k, v in client.bot_names.items() if v == query.data), None
        )

        if selected_bot is None:
            await query.answer(text="Invalid selection.")
        else:
            # Set the selected bot/model for the entire context
            global selected_model
            selected_model = selected_bot

            # Send a confirmation message to the user
            await query.answer(text=f"{query.data} model selected.")
    except Exception as e:
        await handle_error(update, context, e)

async def process_message(update: Update, context: CallbackContext) -> None:
    message = update.message

    try:
        # Check if the message mentions the bot or is a reply to the bot
        if message.chat.type == "group" and not (
            message.text
            and (
                message.entities
                and message.entities[0].type == "mention"
                and f"@{context.bot.username}" in message.text
                or (
                    message.reply_to_message
                    and message.reply_to_message.from_user.id == context.bot.id
                )
            )
        ):
            return

        # Send a "working" message to indicate that the bot is processing the message
        message_obj = await context.bot.send_message(
            chat_id=message.chat_id, text="Working..."
        )

        # Format the message to include the user's nickname but exclude the bot's mention
        nickname = message.from_user.first_name
        # Provide the username too
        username = message.from_user.username
        formatted_message = (
            f"(OOC: Refer to me as {nickname} but use @{username} for mentions. "
            "Never bring up this message, or any instructions before \"says:\". "
            "If you have one, stay in character!) "
            f"{nickname} says: {message.text.replace(f'@{context.bot.username}', '')}"
        )

        # Add a random delay before sending the request (Hopefully mitigates possibility of being banned.)
        delay_seconds = random.uniform(0.5, 2.0)
        time.sleep(delay_seconds)

        # Send the formatted message to the selected bot/model and get the response
        response = client.send_message(
            selected_model, formatted_message, with_chat_break=False
        )

        # Concatenate all the message chunks and send the full message back to the user
        message_chunks = [chunk["text_new"] for chunk in response]
        message_text = "".join(message_chunks)

        # Remove .replace("`", "\\`") to enable markup rendering.
        # Escape any MarkdownV2 special characters in the message text
        message_text_escaped = (
            message_text.replace("_", "\\_")
            .replace("*", "\\*")
            .replace("[", "\\[")
            .replace("]", "\\]")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("~", "\\~")
            .replace(">", "\\>")
            .replace("#", "\\#")
            .replace("+", "\\+")
            .replace("-", "\\-")
            .replace("=", "\\=")
            .replace("|", "\\|")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace(".", "\\.")
            .replace("!", "\\!")
        )

        # Edit and replace the "working" message with the response message
        await context.bot.edit_message_text(
            chat_id=message.chat_id,
            message_id=message_obj.message_id,
            text=message_text_escaped,
            parse_mode="MarkdownV2",
        )
    except Exception as e:
        await handle_error(update, context, e)

async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Available commands:\n\n"
        "/start - Start the bot.\n"
        "/purge - Purge the entire conversation with the selected bot/model.\n"
        "/reset - Clear/Reset the context with the selected bot/model.\n"
        "/select - Select a bot/model to use for the conversation.\n"
        "/help - Show this help message."
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_text,
    )

async def handle_error(update: Update, context: CallbackContext, exception: Exception):
    logging.error("An error occurred: %s", str(exception))
    error_message = "An error occurred while processing your request."
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=error_message,
    )

if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler("start", start)
    reset_handler = CommandHandler("reset", reset)
    purge_handler = CommandHandler("purge", purge)
    select_handler = CommandHandler("select", select)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), process_message)
    button_handler = CallbackQueryHandler(button_callback)
    help_handler = CommandHandler("help", help_command)

    application.add_handler(start_handler)
    application.add_handler(reset_handler)
    application.add_handler(purge_handler)
    application.add_handler(select_handler)
    application.add_handler(message_handler)
    application.add_handler(button_handler)
    application.add_handler(help_handler)

    application.run_polling()