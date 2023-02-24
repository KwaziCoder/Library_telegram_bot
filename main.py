import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from admin import upload_doc
from books import book_find_process
from excelParser import parse_excel


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["step"] = 0

    keyboard = [
        [
            InlineKeyboardButton("Получить книжную рекомендацию", callback_data='books')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Чем могу помочь?', reply_markup=reply_markup)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application = ApplicationBuilder().token('TOKEN').build()

    start_handler = CommandHandler('start', start)
    books_handler = CallbackQueryHandler(book_find_process, "books")


    # upload_query_handler = CallbackQueryHandler(upload_query, "upload")
    upload_doc_handler = MessageHandler(filters.Document.ALL, upload_doc)
    parse_excel_handler = CommandHandler('parsing', parse_excel)

    application.add_handler(start_handler)

    application.add_handler(books_handler)

    # application.add_handler(upload_query_handler)
    application.add_handler(upload_doc_handler)
    application.add_handler(parse_excel_handler)

    application.run_polling()