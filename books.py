import logging

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from excelParser import parse_excel

"""
    context.user_data:
        age: None -> str
        genre: None -> str
        subgenre: None -> str
"""


async def send_reply_keyboard(update: Update, answers, question) -> None:
    keyboard = [
        [KeyboardButton(answer)] for answer in answers
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        question,
        reply_markup=reply_markup)


async def start_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Started poll")

    if "data" not in context.bot_data:
        await parse_excel(update, context)

    context.user_data["age"] = None
    context.user_data["genre"] = None
    context.user_data["subgenre"] = None

    context.user_data["polling_in_progress"] = True

    ages = context.bot_data["data"].keys()

    await send_reply_keyboard(update, ages, 'Какое возрастное ограничение тебе подходит?')


async def finish_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(logging.info("Finished poll"))

    context.user_data["polling_in_progress"] = False

    await send_reply_keyboard(update, ["Подобрать книги"], 'Тебе спасибо! Ты всегда можешь обратиться ко мне через меню ниже.\n\nБуду ждать тебя снова!')


async def send_result(update: Update, context: ContextTypes.DEFAULT_TYPE, books) -> None:
    for book in books:
        await context.bot.send_photo(update.effective_chat.id, f"./assets/images/{book[3]}",
                                     f"Название книги: {book[0]}\nАвтор: {book[1]}\nОписание: {book[2]}")

    await context.bot.send_message(update.effective_chat.id,
                                   "Надеюсь, тебе понравились мои рекомендации.\n\nБыл рад стараться. Любую книгу из списка ты можешь взять в библиотеке-филиале №15 по адресу: Мурманск, проспект Ленина 94. Номер телефона для связи: 42-21-67.\n\nЕсли тебе все еще нужна моя помощь - нажми “Продолжить”")

    logging.info("Sent result of poll!")


async def book_find_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if "polling_in_progress" in context.user_data and context.user_data["polling_in_progress"]:
        logging.info("Poll in progress! Message goes to inner scope!")

        if update.message.text == "Продолжить":
            await start_poll(update, context)

        elif update.message.text == "Спасибо за помощь":
            await finish_poll(update, context)

        elif context.user_data["age"] is None:
            if update.message.text in context.bot_data["data"]:
                age = update.message.text
                context.user_data["age"] = age

                genres = context.bot_data["data"][age].keys()

                await send_reply_keyboard(update, genres, 'Давай теперь определимся с темой?')

            else:
                ages = context.bot_data["data"].keys()

                await send_reply_keyboard(update, ages, 'Какое возрастное ограничение тебе подходит?')

        elif context.user_data["genre"] is None:
            age = context.user_data["age"]

            if update.message.text in context.bot_data["data"][age]:
                genre = update.message.text
                context.user_data["genre"] = genre

                subgenres = context.bot_data["data"][age][genre].keys()

                await send_reply_keyboard(update, subgenres,  'Я тебя понял. Давай уточним?')

            else:
                genres = context.bot_data["data"][age].keys()

                await send_reply_keyboard(update, genres, 'Давай теперь определимся с темой?')

        elif context.user_data["subgenre"] is None:
            age = context.user_data["age"]
            genre = context.user_data["genre"]

            if update.message.text in context.bot_data["data"][age][genre]:
                finish_answers = ["Продолжить", "Спасибо за помощь"]

                await send_reply_keyboard(update, finish_answers, 'Смотри, я могу предложить посмотреть эти варианты...')
                
                subgenre = update.message.text
                context.user_data["subgenre"] = subgenre

                books = context.bot_data["data"][age][genre][subgenre]

                await send_result(update, context, books)

            else:
                subgenres = context.bot_data["data"][age][genre].keys()

                await send_reply_keyboard(update, subgenres, 'Я тебя понял. Давай уточним?')

    else:
        logging.info("Poll is finished! Message goes to outer scope!")

        if update.message.text == "Подобрать книги" or update.message.text == "Продолжить":
            await start_poll(update, context)

        elif update.message.text == "Спасибо за помощь":
            await finish_poll(update, context)
        else:
            await send_reply_keyboard(update, ["Подобрать книги"], "Прошу прощения, я потерял нить нашего разговора. Уточни, пожалуйста, как я могу тебе помочь.")