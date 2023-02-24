import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from admin import upload_doc
from books import book_find_process
from excelParser import parse_excel


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if "data" not in context.bot_data:
        await parse_excel(update, context)

    context.user_data["age"] = None
    context.user_data["genre"] = None
    context.user_data["subgenre"] = None

    context.user_data["polling_in_progress"] = True

    keyboard = [
        [
            KeyboardButton("Давай!"),
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    await update.message.reply_text('Привет! Меня зовут Федя. Я кибер-сотрудник библиотеки-филиал №15. Не знаешь что бы почитать? Давай я задам тебе пару наводящих вопросов?', reply_markup=reply_markup)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application = ApplicationBuilder().token('TOKEN').build()

    start_handler = CommandHandler('start', start)
    books_handler = MessageHandler(filters.Regex(r"\w+"), book_find_process)

    upload_doc_handler = MessageHandler(filters.Document.ALL, upload_doc)
    parse_excel_handler = CommandHandler('parsing', parse_excel)

    application.add_handler(start_handler)

    application.add_handler(books_handler)

    application.add_handler(upload_doc_handler)
    application.add_handler(parse_excel_handler)

    application.run_polling()