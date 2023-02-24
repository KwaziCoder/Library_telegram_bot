from telegram import Update
from telegram.ext import ContextTypes


# async def upload_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.callback_query
#     await query.delete_message()
#     context.bot.send_message(update.effective_chat.id, text="Хорошо. Загрузи документ и я сохраню его.")


async def upload_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive('./assets/files/books.xlsx')




