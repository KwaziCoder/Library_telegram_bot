import logging
import time

from telegram import Update
from telegram.ext import ContextTypes
from openpyxl import load_workbook


async def parse_excel(update: Update, context: ContextTypes.DEFAULT_TYPE, file=None) -> None:
    logging.info("Started to parse excel with data!")
    excel_parse_start_time = time.time()

    file_path = './assets/files/books.xlsx'

    if file:
        file_path = file

    wb = load_workbook(filename=file_path)
    ws = wb.active
    ws_list = list(ws)

    rows = [[item.value for item in row] for row in ws_list]

    """
    rows (индексы):
        [0] - Названия столбцов (они нам не нужны)
        [$] - Динамически определяемый индекс (начиная с 1)
        [$][0] - Возраст
        [$][1] - Жанр
        [$][2] - Поджанр
        [$][3] - Название книги
        [$][4] - Автор
        [$][5] - Описание книги
        [$][6] - Название картинки
    """

    data_dict = dict()

    first_level = ""
    second_level = ""
    third_level = ""

    for i in range(1, len(rows)):
        for j in range(0, len(rows[i])):
            if j == 0:  # Возраст
                if rows[i][j] in data_dict:
                    continue
                else:
                    data_dict[rows[i][j]] = dict()
                    first_level = rows[i][j]
            elif j == 1:  # Жанр
                if rows[i][j] in data_dict[first_level]:
                    continue
                else:
                    data_dict[first_level][rows[i][j]] = dict()
                    second_level = rows[i][j]
            elif j == 2:  # Поджанр
                if rows[i][j] in data_dict[first_level][second_level]:
                    continue
                else:
                    data_dict[first_level][second_level][rows[i][j]] = list()
                    third_level = rows[i][j]
            elif j == 3:
                data_dict[first_level][second_level][third_level].append(list())
                data_dict[first_level][second_level][third_level][-1].append(rows[i][j])
            else:
                data_dict[first_level][second_level][third_level][-1].append(rows[i][j])

    test_mode = False

    if "test_mode" in context.user_data:
        test_mode = context.user_data["test_mode"]

    if test_mode:
        context.user_data["data"] = data_dict
    else:
        context.bot_data["data"] = data_dict
        context.bot_data["update_date"] = time.time()

    excel_parse_finish_time = time.time()
    logging.info(f"Finished to parse excel in { (excel_parse_finish_time - excel_parse_start_time) * 1000} milliseconds!")

    """
        {
            '0+': {
                'Жанр1': {
                    'Поджанр 1': ['Книга 1', 'Автор 1', 'Описание 1', 'book1.jpg']
                }
            }
        }
    """


