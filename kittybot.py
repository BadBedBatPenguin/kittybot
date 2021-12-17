import logging
import os

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dotenv import load_dotenv 

load_dotenv()

secret_token = os.getenv('TOKEN')

CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'
ERROR_MESSAGE = 'Ошибка при запросе к основному API: '


def get_new_pictre(category):
    categories = {
        'cat': [CAT_URL, DOG_URL],
        'dog': [DOG_URL, CAT_URL],
    }
    try:
        response = requests.get(categories[category][0])
    except Exception as error:
        logging.error(ERROR_MESSAGE + error)
        response = requests.get(categories[category][1])
    response = response.json()
    return response[0].get('url')


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_pictre('cat'))


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_pictre('dog'))


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat', '/newdog']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри какого котика я тебе нашел'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_pictre('cat'))


def answer(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Мау?')


def main():
    updater = Updater(token=secret_token)
    commands = [
        ['start', wake_up],
        ['newcat', new_cat],
        ['newdog', new_dog],
    ]
    for command, func in commands:
        updater.dispatcher.add_handler(CommandHandler(command, func))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, answer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()