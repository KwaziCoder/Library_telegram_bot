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

        if context.user_data["age"] is None and update.message.text == "Давай!":

            keyboard = [
                [
                    KeyboardButton("1"),
                ],
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard)

            await update.message.reply_text(
                'Какое возрастное ограничение тебе подходит?',
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
