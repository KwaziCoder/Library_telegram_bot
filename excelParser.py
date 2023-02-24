from telegram import Update
from telegram.ext import ContextTypes
from openpyxl import load_workbook


async def parse_excel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    wb = load_workbook(filename='./assets/files/books.xlsx')
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
    print(rows)

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

    context.bot_data["data"] = data_dict
    print(context.bot_data["data"])

    """
        {
            '0+': {
                'Жанр1': {
                    'Поджанр 1': ['Книга 1', 'Автор 1', 'Описание 1', 'book1.jpg']
                }
            }
        }
    """


