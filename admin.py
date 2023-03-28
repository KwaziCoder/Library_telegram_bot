import logging
import time
from zipfile import ZipFile

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
    logging.info("Command 'info' was entered!")

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


async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Command 'data' was entered!")

    if await auth(update, context):
        await context.bot.send_document(update.effective_chat.id, './assets/files/books.xlsx')


async def upload_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Try of adding a new excel file was detected!")

    if await auth(update, context):
        context.user_data["test_mode"] = True

        excel = update.message.document
        file = await context.bot.get_file(excel)
        await file.download_to_drive('./assets/test_files/books.xlsx')
        await parse_excel(update, context)
        await context.bot.send_message(update.effective_chat.id, "Данные загружены! ВНИМАНИЕ! Включен ТЕСТОВЫЙ режим!\n\nОтправь мне команду /start и проверь, нормально ли работает опрос на новых данных.\n\nЕсли все хорошо, то отправь мне команду /update, чтобы обновить данные для всех пользователей.\n\nЧтобы вернуться к старым данным и выйти из тестового режима, отправь мне команду /cancel")


async def update_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await auth(update, context):
        logging.info("Process of updating data is launched!")

        context.bot_data["data"] = context.user_data["data"]
        context.bot_data["update_date"] = time.time()

        context.user_data["test_mode"] = False

        await context.bot.send_message(update.effective_chat.id,
                                       "Данные обновлены и стали доступны всем пользователям! Тестовый режим отключен!")

        logging.info("Process of updating data is finished successfully!")


async def cancel_update_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await auth(update, context):
        context.user_data["data"] = context.bot_data["data"]
        context.user_data["test_mode"] = False

        await context.bot.send_message(update.effective_chat.id,
                                       "Отмена обновления данных! Тестовый режим отключен!")

        logging.info("Process of updating data is canceled!")


async def upload_zip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Try of adding a zip file was detected!")

    if await auth(update, context):
        zip_path = update.message.document
        zip_file = await context.bot.get_file(zip_path)
        await zip_file.download_to_drive('./assets/files/images.zip')
        with ZipFile('./assets/files/images.zip', 'r') as zip_arcive:
            zip_arcive.extractall('./assets/images')
    await context.bot.send_message(update.effective_chat.id, "Изображения загружены!")


async def upload_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Try of adding an image was detected!")

    if await auth(update, context):
        image = update.message.document
        file = await context.bot.get_file(image.file_id)
        await file.download_to_drive(f'./assets/images/{image.file_name}')
        await context.bot.send_message(update.effective_chat.id, f"Файл '{image.file_name}' успешно загружен!")


async def upload_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Try of adding an photo was detected!")

    if await auth(update, context):
        await context.bot.send_message(update.effective_chat.id, 'Прошу прощения, но я принимаю изображения только в формате файлов. В окне загрузки своих картинок обязательно снимите галочку "Сжать изображение".')


async def define_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.sticker.file_id)


