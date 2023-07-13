import json
import xlrd
import os

with open("liquorConfiguration.json") as f:
    configuration = json.load(f)


def liquorParser(folder):
    result = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            print(file_path)
            book = xlrd.open_workbook(file_path)
            sheet1 = book.sheets()[0]
            keys = sheet1.row_values(3)

            index = 0
            indexes = []
            for key in keys:
                if configuration.get("attributes").__contains__(key):
                    indexes.append([key, index])
                index += 1

            row_number = sheet1.nrows
            for i in range(4, row_number, 1):
                licence = {}
                row = sheet1.row_values(i)
                for index in indexes:
                    licence[index[0]] = row[index[1]]
                result.append(licence)

    return result


if __name__ == '__main__':
    print(liquorParser(configuration.get("folder")))
