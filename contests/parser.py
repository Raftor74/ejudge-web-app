import re
import os

# TODO: При одинаковых параметрах перезаписывается ключ. Необходимо это как-то устранить

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Парсит конфигурационный файл контеста Ejudge
def parse_config_file(file):
    # Записи сортируются по 4-м блокам
    blocks = {
        "settings": [],
        "problems": [],
        "languages": [],
        "testers": []
    }

    # Записи определяются по 4-м блокам
    patterns = {
        "end_block": re.compile('^\s+$'),
        "inline_property": re.compile('^\w+$'),
        "property_string": re.compile('^(?P<property>\w+)\s?=\s?(?P<value>.+)$'),
        "block_header": re.compile('^\[(?P<block_name>\w+)\]$')
    }

    # Текущий обрабатываемый блок
    current_block = []
    # Название последнего блока
    last_block = ""

    # Для всех строчек в файле
    for line in file.readlines():
        # Регулярное выражение для свойства
        prop = re.search(patterns["property_string"], line)
        # Регулярное выражение для начала блока
        block_start = re.search(patterns["block_header"], line)
        # Регулярное выражение для конца блока
        end_block = re.search(patterns["end_block"], line)
        # Регулярное выражение для однострочного параметра
        inline_property = re.search(patterns["inline_property"], line)
        # Если встретили пустую строку - значит блок закончился
        # Если нет - блок продолжается
        if end_block is None:
            if prop is not None:
                current_block.append({
                    prop.group('property'): prop.group('value').rstrip("\n")
                })
            elif block_start is not None:
                last_block = block_start.group('block_name')
            elif inline_property is not None:
                current_block.append({
                    inline_property.group(0): "SingleKey"
                })
        else:
            if current_block:
                if last_block == "language":
                    blocks["languages"].append(current_block)
                elif last_block == "problem":
                    blocks["problems"].append(current_block)
                elif last_block == "tester":
                    blocks["testers"].append(current_block)
                else:
                    blocks["settings"].append(current_block)
            current_block = []
            last_block = ""

    return blocks


# Записывает блок в файл
def write_block(block, file, blockname = ""):
    for iterator in block:
        if blockname != "":
            file.write(blockname + "\n")
        for item in iterator:
            for key in item.keys():
                if item[key] != "SingleKey":
                    file.write(key + " = " + item[key] + "\n")
                else:
                    file.write(key + "\n")
        file.write("\n")


# Выводит блок на консоль
def print_block(block, blockname):
    for iterator in block:
        print(blockname)
        for item in iterator:
            for key in item.keys():
                print(key,"=",item[key])
    print("")


def main():
    filename = 'serve.cfg'
    output_filename = "output.cfg"
    abs_file_path = os.path.join(BASE_DIR, filename)

    if not os.path.isfile(abs_file_path):
        raise FileExistsError()

    try:
        file = open(abs_file_path, "r", encoding="utf-8")
    except IOError:
        print("File", filename, "cannot be opened")

    blocks = parse_config_file(file)
    file.close()

    output_file = open(output_filename, "w+", encoding="utf-8")
    write_block(blocks["settings"], output_file)
    write_block(blocks["languages"], output_file, "[language]")
    write_block(blocks["problems"], output_file, "[problem]")
    write_block(blocks["testers"], output_file, "[tester]")
    output_file.close()

if __name__ == '__main__':
    main()
