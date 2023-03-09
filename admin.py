import logging

from telegram import Update
from telegram.ext import ContextTypes

from excelParser import parse_excel

ADMINS = [763665227, 879325220]


async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.message.from_user.id in ADMINS:
        logging.info("User is admin! Access granted!")
        return True
    else:
        await context.bot.send_message(update.effective_chat.id,
                                       "Отказано в доступе! У вас нет прав на загрузку файлов!")
        logging.info("User is not admin! Access denied!")
        return False


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await auth(update, context):
        await context.bot.send_message(update.effective_chat.id,
                                       "Понял тебя! Сейчас я объясню, как обновить у меня данные и создать тем самым новый контент для наших посетителей библиотеки!")
        await context.bot.send_message(update.effective_chat.id,
                                       "Шаг 1. Пришли мне обновленный excel-файл с данными для опроса пользователей. Помни! В excel-файле должна быть определенная структура полей! Нет образца для создания правильного документа? Не беда! Напиши команду /data и я пришлю файл, на который ориентируюсь сейчас, когда общаюсь с пользователями.")
        await context.bot.send_message(update.effective_chat.id,
                                       "Шаг 2. Пришли мне все картинки, которые были указаны тобой в excel-файле! Помни! Название и расширение (.jpg, .jpeg, .png и т.д.) каждой картинки должны В ТОЧНОСТИ соответствовать тем наименованиям, которые записаны в excel-файле.")
        await context.bot.send_message(update.effective_chat.id,
                                       "Шаг 3. Когда все файлы загружены, отправь мне команду /start и проверь мою работу на новых данных.")
        await context.bot.send_message(update.effective_chat.id,
                                       "Вот и всё! Дело не хитрое! Удачи тебе, коллега!")

async def upload_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Try of adding a new excel file was detected!")

    if await auth(update, context):
        excel = update.message.document
        file = await context.bot.get_file(excel)
        await file.download_to_drive('./assets/files/books.xlsx')
        await parse_excel(update, context)
        await context.bot.send_message(update.effective_chat.id, "Данные обновлены!")


async def upload_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Try of adding an image was detected!")

    if await auth(update, context):
        image = update.message.document
        file = await context.bot.get_file(image.file_id)
        await file.download_to_drive(f'./assets/images/{image.file_name}')
        await context.bot.send_message(update.effective_chat.id, f"Файл '{image.file_name}' успешно загружен!")


async def define_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.sticker.file_id)


