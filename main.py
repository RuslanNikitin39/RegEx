from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

def read_file():
    with open("phonebook_raw.csv", encoding="utf8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list

def write_file(contacts_list):
    with open("phonebook.csv", "w", newline="", encoding="utf8") as f:
      datawriter = csv.writer(f, delimiter=',')
      datawriter.writerows(contacts_list)

def get_new_number(phone_number):
    """
    преобразование номера телефона по шаблону
    :param phone_number: номер в произвольном формате
    :return: новый номер в заданном формате
    """
    if phone_number == "":
        return ""

    pattern = r'(\+7|8)?(\s*)?(\(*)(\d{3})?(\)*)?(\s|-?)(\d{3})(\s|-?)(\d{2})(\s|-?)(\d*)(\s*)?(\(*)?((доб.|доб.)*)?(\s*)(\d*)?((\))*)'
    substitution = r"+7(\4)\7-\9-\11 \15\17"

    return re.sub(pattern, substitution, phone_number)


def get_new_list(contacts_list):
    """
    формирование записи телефонной книги
    :param row: список из файла
    :return: нормально структурированный список
    """
    contacts_dict = {}
    new_contacts_list = []
    for row in contacts_list:
        if row == contacts_list[0]:
            contacts_dict.setdefault('header', row)
            continue
        full_name = f'{row[0]} {row[1]} {row[2]}'
        # уберем лишние пробелы, вдруг они есть
        pattern = r'\s+'
        row_list = re.sub(pattern, ' ', full_name).split(' ')
        if len(row_list) > 3:
            row_list.remove('')
        for i in range(3, 7):
            # поработаем с номером телефона
            if i == 5:
                row_list.append(get_new_number(row[i]))
            else:
                row_list.append(row[i])

        key = f'{row_list[0]} {row_list[1]}'
        j = 0
        if key in contacts_dict:
            for elm in contacts_dict[key]:
                if not row_list[j] == "":
                    contacts_dict[key][j] = row_list[j]
                j += 1
        else:
            contacts_dict.setdefault(key, row_list)

    pprint(contacts_dict)

    return list(contacts_dict.values())


if __name__ == '__main__':
    contacts_list = read_file()
    write_file(get_new_list(contacts_list))
    print(f'Записан файл контактов.')

