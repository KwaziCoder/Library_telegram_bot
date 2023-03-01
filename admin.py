from telegram import Update
from telegram.ext import ContextTypes

from excelParser import parse_excel

ADMINS = [763665227]


async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.message.from_user.id in ADMINS:
        return True
    else:
        await context.bot.send_message(update.effective_chat.id,
                                       "Отказано в доступе! У вас нет прав закачивание файлов!")
        return False


async def upload_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Document")

    if await auth(update, context):
        excel = update.message.document
        if excel.file_name == "books.xlsx":
            file = await context.bot.get_file(excel)
            await file.download_to_drive('./assets/files/books.xlsx')
            await parse_excel(update, context)
            await context.bot.send_message(update.effective_chat.id, "Файл 'books.xlsx' загружен!")


async def upload_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Image")

    if await auth(update, context):
        image = update.message.document
        file = await context.bot.get_file(image.file_id)
        await file.download_to_drive(f'./assets/images/{image.file_name}')
        await context.bot.send_message(update.effective_chat.id, f"Файл '{image.file_name}' успешно загружен!")


async def define_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.sticker.file_id)


