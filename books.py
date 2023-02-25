from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


"""
    context.user_data:
        age: None -> str
        genre: None -> str
        subgenre: None -> str
"""


async def book_find_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if "polling_in_progress" in context.user_data and context.user_data["polling_in_progress"]:
        print("Наш случай!")

        if context.user_data["age"] is None:
            if update.message.text in context.bot_data["data"]:
                age = update.message.text
                context.user_data["age"] = age

                genres = context.bot_data["data"][age].keys()

                keyboard = [
                    [KeyboardButton(genre)] for genre in genres
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    'Давай теперь определимся с темой?',
                    reply_markup=reply_markup)

            else:
                ages = context.bot_data["data"].keys()

                keyboard = [
                    [KeyboardButton(age)] for age in ages
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard)

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

                reply_markup = ReplyKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    'Я тебя понял. Давай уточним?',
                    reply_markup=reply_markup)

            else:
                genres = context.bot_data["data"][age].keys()

                keyboard = [
                    [KeyboardButton(genre)] for genre in genres
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard)

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

                for book in books:
                    await context.bot.send_photo(update.effective_chat.id, f"./assets/images/{book[3]}",
                            f"Название книги: {book[0]}\nАвтор: {book[1]}\nОписание: {book[2]}")

                context.user_data["age"] = None
                context.user_data["genre"] = None
                context.user_data["subgenre"] = None

                context.user_data["polling_in_progress"] = False

            else:
                subgenres = context.bot_data["data"][age].keys()

                keyboard = [
                    [KeyboardButton(subgenre)] for subgenre in subgenres
                ]

                reply_markup = ReplyKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    'Я тебя понял. Давай уточним?',
                    reply_markup=reply_markup)

    else:
        print("Не наш случай!")
    # await query.answer()

    #
    # if (current_step > 0):
    #     context.user_data[user_data_keys_by_steps[current_step]] = query.message.reply_markup.inline_keyboard[0][0].text
    #
    #
    # if (context.user_data["step"] <= 2):
    #     keyboard = [
    #         list(map(lambda answer: InlineKeyboardButton(answer, callback_data="books" ), steps[current_step]["answers"]))
    #     ]
    #
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #
    #     await update.callback_query.message.reply_text(steps[current_step]["question"], reply_markup=reply_markup)
    #
    #     context.user_data["step"] += 1
    # else:
    #     age = context.user_data["age"]
    #     genre = context.user_data["genre"]
    #     subgenre = context.user_data["subgenre"]
    #
    #     books = data[age][genre][subgenre]
    #
    #     for book in books:
    #         await context.bot.send_photo(update.effective_chat.id, "./assets/images/book1.jpg",
    #                                      f"Название книги: {book['title']}\nАвтор: {book['author']}\nОписание: {book['desc']}")
    #
    #     context.user_data["step"] = 0
