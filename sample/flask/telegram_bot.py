#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import time
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from flask import Flask, request
app = Flask(__name__)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

chat_ids = set()
stop_notification = False
started_notification = False
bot = None

def start(update, context):
    chat_id = update.message.chat_id
    chat_ids.add(chat_id)
    print(chat_ids)
    update.message.reply_text('Du wirst benachrichtigt, wenn ich Hilfe benötige. Danke 😊')

def stop(update, context):
    chat_ids.remove(update.message.chat_id)
    print(chat_ids)
    update.message.reply_text('Du wirst nicht mehr benachrichtigt. Danke für deine Hilfe. 😊')

def button_callback(update, context):
    global stop_notification
    stop_notification = True
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Danke für deine Hilfe. 😊".format(query.data))

def start_notification(update, context):
    global stop_notification
    stop_notification = False
    x = threading.Thread(target=start_notification_thread)
    x.start()

def start_notification_thread():
    print("start_notification")
    global stop_notification
    while True:
        if stop_notification:
            print("stop notification")
            break
        for chat_id in chat_ids:
            print("send message to " + str(chat_id))
            send_notification(chat_id)
            time.sleep(2)


def send_notification(chat_id):
    keyboard = [[InlineKeyboardButton("Stoppe Benachrichtigungen", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id,'🚨 Ich brauche deine Hilfe! 🚨', reply_markup=reply_markup)

def echo(update, context):
    if update.message.chat_id in chat_ids:
        update.message.reply_text('Schön, dass du mir hilfst 😊')
    else:
        update.message.reply_text('Bitte schicke mir /start damit ich dich benachrichtigen kann, wenn ich Hilfe benötige. Danke 😊')

def start_telegram_bot():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1295851454:AAGv8OlnnFDQHwLlbMAMPtKhnpyAJGE9m1c", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("sn", start_notification))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_callback))
    # Start the Bot
    updater.start_polling()
    global bot
    bot = updater.bot

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    # updater.idle()