from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from data import data

steps = [
    {"question": 'Возраст?', "answers": ["Возраст 1", "Возраст 2"]},
    {"question": 'Жанр?', "answers": ["Жанр 1", "Жанр 2"]},
    {"question": 'Поджанр?', "answers": ["Поджанр 1", "Поджанр 2"]}
]

user_data_keys_by_steps = {
    1: "age",
    2: "genre",
    3: "subgenre"
}

"""
    context.user_data:
        age: None -> str
        genre: None -> str
        subgenre: None -> str
        step: 0 -> number
"""

async def book_find_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.delete_message()

    current_step = context.user_data["step"]

    if (current_step > 0):
        context.user_data[user_data_keys_by_steps[current_step]] = query.message.reply_markup.inline_keyboard[0][0].text


    if (context.user_data["step"] <= 2):
        keyboard = [
            list(map(lambda answer: InlineKeyboardButton(answer, callback_data="books" ), steps[current_step]["answers"]))
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(steps[current_step]["question"], reply_markup=reply_markup)

        context.user_data["step"] += 1
    else:
        age = context.user_data["age"]
        genre = context.user_data["genre"]
        subgenre = context.user_data["subgenre"]

        books = data[age][genre][subgenre]

        for book in books:
            await context.bot.send_photo(update.effective_chat.id, "./assets/images/book1.png",
                                         f"Название книги: {book['title']}\nАвтор: {book['author']}\nОписание: {book['desc']}")

        context.user_data["step"] = 0
