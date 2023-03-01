from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from excelParser import parse_excel

"""
    context.user_data:
        age: None -> str
        genre: None -> str
        subgenre: None -> str
"""


async def book_find_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if "polling_in_progress" in context.user_data and context.user_data["polling_in_progress"]:
        print("Наш случай!")

        if update.message.text == "Продолжить":
            if "data" not in context.bot_data:
                await parse_excel(update, context)

            context.user_data["age"] = None
            context.user_data["genre"] = None
            context.user_data["subgenre"] = None

            ages = context.bot_data["data"].keys()

            keyboard = [
                [KeyboardButton(age)] for age in ages
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            await update.message.reply_text(
                'Какое возрастное ограничение тебе подходит?',
                reply_markup=reply_markup)

        elif update.message.text == "Спасибо за помощь":
            keyboard = [[KeyboardButton("Подобрать книги")]]
            reply_markup = ReplyKeyboardMarkup(keyboard,  resize_keyboard=True)
            await update.message.reply_text(
                'Тебе спасибо! Ты всегда можешь обратиться ко мне через меню ниже.\n\n Буду ждать тебя снова!',
                reply_markup=reply_markup)

            context.user_data["polling_in_progress"] = False

        elif context.user_data["age"] is None:
            if update.message.text in context.bot_data["data"]:
                age = update.message.text
                context.user_data["age"] = age

                genres = context.bot_data["data"][age].keys()

                keyboard = [
                    [KeyboardButton(genre)] for genre in genres
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

                await update.message.reply_text(
                    'Давай теперь определимся с темой?',
                    reply_markup=reply_markup)

            else:
                ages = context.bot_data["data"].keys()

                keyboard = [
                    [KeyboardButton(age)] for age in ages
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

                await update.message.reply_text(
                    'Какое возрастное ограничение тебе подходит?',
                    reply_markup=reply_markup)

        elif context.user_data["genre"] is None:
            age = context.user_data["age"]

            if update.message.text in context.bot_data["data"][age]:
                genre = update.message.text
                context.user_data["genre"] = genre

                subgenres = context.bot_data["data"][age][genre].keys()

                keyboard = [
                    [KeyboardButton(subgenre)] for subgenre in subgenres
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

                await update.message.reply_text(
                    'Я тебя понял. Давай уточним?',
                    reply_markup=reply_markup)

            else:
                genres = context.bot_data["data"][age].keys()

                keyboard = [
                    [KeyboardButton(genre)] for genre in genres
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

                await update.message.reply_text(
                     'Давай теперь определимся с темой?',
                    reply_markup=reply_markup)

        elif context.user_data["subgenre"] is None:
            age = context.user_data["age"]
            genre = context.user_data["genre"]

            if update.message.text in context.bot_data["data"][age][genre]:
                subgenre = update.message.text
                context.user_data["subgenre"] = subgenre

                books = context.bot_data["data"][age][genre][subgenre]

                await context.bot.send_message(update.effective_chat.id, "Смотри, я могу предложить посмотреть эти варианты")

                for book in books:
                    await context.bot.send_photo(update.effective_chat.id, f"./assets/images/{book[3]}",
                            f"Название книги: {book[0]}\nАвтор: {book[1]}\nОписание: {book[2]}")

                await context.bot.send_message(update.effective_chat.id, "Надеюсь, тебе понравились мои рекомендации.\n\nБыл рад стараться. Любую книгу из списка ты можешь взять в библиотеке-филиале №15 по адресу: Мурманск, проспект Ленина 94. Номер телефона для связи: 42-21-67.")

                keyboard = [
                    [KeyboardButton("Продолжить")],
                    [KeyboardButton("Спасибо за помощь")]
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

                await update.message.reply_text(
                    'Если тебе все еще нужна моя помощь - нажми “Продолжить”',
                    reply_markup=reply_markup)

            else:
                subgenres = context.bot_data["data"][age][genre].keys()

                keyboard = [
                    [KeyboardButton(subgenre)] for subgenre in subgenres
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

                await update.message.reply_text(
                    'Я тебя понял. Давай уточним?',
                    reply_markup=reply_markup)

    else:
        print("Не наш случай!")

        if update.message.text == "Подобрать книги":
            if "data" not in context.bot_data:
                await parse_excel(update, context)

            context.user_data["age"] = None
            context.user_data["genre"] = None
            context.user_data["subgenre"] = None

            context.user_data["polling_in_progress"] = True

            ages = context.bot_data["data"].keys()

            keyboard = [
                [KeyboardButton(age)] for age in ages
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            await update.message.reply_text(
                'Какое возрастное ограничение тебе подходит?',
                reply_markup=reply_markup)
