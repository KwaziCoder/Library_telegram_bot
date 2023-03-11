import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from admin import upload_doc, auth, upload_image, define_sticker, info, get_data, upload_photo, upload_zip
from books import book_find_process
from excelParser import parse_excel
from logger import set_logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Command 'start' was entered!")

    if "data" not in context.bot_data:
        logging.info("No data!")
        await parse_excel(update, context)

    context.user_data["age"] = None
    context.user_data["genre"] = None
    context.user_data["subgenre"] = None

    context.user_data["polling_in_progress"] = True

    await context.bot.send_sticker(update.effective_chat.id, "CAACAgUAAxkBAAIEhGP_myRO81SMdRKquFUQdvRu7zs6AAKCAwAC6QrIA4xZA7HpW8S3LgQ")
    await context.bot.send_message(update.effective_chat.id, "Привет! Меня зовут Федя. Я кибер-сотрудник библиотеки-филиал №15. Не знаешь что бы почитать? Давай я задам тебе пару наводящих вопросов?")

    ages = context.bot_data["data"].keys()

    keyboard = [
        [KeyboardButton(age)] for age in ages
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Какое возрастное ограничение тебе подходит?',
        reply_markup=reply_markup)

    logging.info("Started poll!")

if __name__ == '__main__':
    set_logger()

    try:
        application = ApplicationBuilder().token('TOKEN').build()

        logging.info("App has been successfully built!")

        start_handler = CommandHandler('start', start)
        info_handler = CommandHandler('info', info)
        data_handler = CommandHandler('data', get_data)

        books_handler = MessageHandler(filters.Regex(r"\w+"), book_find_process)

        stickers_handler = MessageHandler(filters.Sticker.ALL, define_sticker)

        upload_doc_handler = MessageHandler(filters.Document.FileExtension("xlsx"), upload_doc)
        upload_zip_handler = MessageHandler(filters.Document.ZIP, upload_zip)
        upload_image_handler = MessageHandler(filters.Document.IMAGE, upload_image)
        upload_photo_handler = MessageHandler(filters.PHOTO, upload_photo)

        application.add_handler(start_handler)
        application.add_handler(info_handler)
        application.add_handler(data_handler)

        application.add_handler(books_handler)

        application.add_handler(stickers_handler)

        application.add_handler(upload_doc_handler)
        application.add_handler(upload_zip_handler)
        application.add_handler(upload_image_handler)
        application.add_handler(upload_photo_handler)

        logging.info("All handlers are added!")
        logging.info("App start running...")

        application.run_polling()
    except Exception as e:
        logging.error(e, exc_info=True)