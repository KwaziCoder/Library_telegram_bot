import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from admin import define_sticker, info, get_data, upload_zip, update_data, cancel_update_data
from books import book_find_process, start_poll
from logger import set_logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Command 'start' was entered!")

    await context.bot.send_sticker(update.effective_chat.id, "CAACAgUAAxkBAAIEhGP_myRO81SMdRKquFUQdvRu7zs6AAKCAwAC6QrIA4xZA7HpW8S3LgQ")
    await context.bot.send_message(update.effective_chat.id, "Привет! Меня зовут Федя. Я кибер-сотрудник библиотеки-филиала №15. Не знаешь что бы почитать? Давай я задам тебе пару наводящих вопросов?")

    await start_poll(update, context)


if __name__ == '__main__':
    set_logger()

    try:
        application = ApplicationBuilder().token('TOKEN').build()

        logging.info("App has been successfully built!")

        start_handler = CommandHandler('start', start)
        info_handler = CommandHandler('info', info)
        data_handler = CommandHandler('data', get_data)
        update_data_handler = CommandHandler('update', update_data)
        cancel_update_data_handler = CommandHandler('cancel', cancel_update_data)

        books_handler = MessageHandler(filters.Regex(r"\w+"), book_find_process)

        stickers_handler = MessageHandler(filters.Sticker.ALL, define_sticker)

        upload_zip_handler = MessageHandler(filters.Document.ZIP, upload_zip)

        application.add_handler(start_handler)
        application.add_handler(info_handler)
        application.add_handler(data_handler)
        application.add_handler(update_data_handler)
        application.add_handler(cancel_update_data_handler)

        application.add_handler(books_handler)

        application.add_handler(stickers_handler)

        application.add_handler(upload_zip_handler)

        logging.info("All handlers are added!")
        logging.info("App start running...")

        application.run_polling()
    except Exception as e:
        logging.error(e, exc_info=True)