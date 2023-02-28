from telegram import Update
from telegram.ext import ContextTypes

from excelParser import parse_excel

ADMINS = [763665227]


async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id in ADMINS:
        print("Admin")
        context.user_data["is_admin"] = True
    else:
        print("Not admin")
        context.user_data["is_admin"] = False


async def upload_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Document")
    if update.message.from_user.id in ADMINS:
        file = await context.bot.get_file(update.message.document)
        await file.download_to_drive('./assets/files/books.xlsx')
        await parse_excel(update, context)
    else:
        await context.bot.send_message(update.effective_chat.id, "Отказано в доступе! Авторизируйтесь как администратор!")


async def upload_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Image")
    if update.message.from_user.id in ADMINS:
        file = await context.bot.get_file(update.message.document.file_id)
        await file.download_to_drive(f'./assets/images/{update.message.document.file_name}')
    else:
        await context.bot.send_message(update.effective_chat.id, "Отказано в доступе! Авторизируйтесь как администратор!")




