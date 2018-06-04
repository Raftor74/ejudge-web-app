""" Класс для работы с контестами """
import os
import re
import json
import configparser, itertools
from collections import OrderedDict
from bs4 import BeautifulSoup
from mysite import settings
from .models import Cntsregs, Logins, Problems


# Класс для создания задач для Контестов
class ProblemsCreator(object):

    _eof = "\n"
    _path_to_xml_example = settings.EJUDGE_FILE_EXAMPLES_FOLDER + "task.xml"
    _errors = list()
    _xml_name = "statement.xml"

    # Возвращает список ошибок
    def get_error_list(self):
        return self._errors

    # Проверяет, существует ли директория с контестом
    def is_contest_dir_exist(self, path_to_dir):
        return os.path.isdir(path_to_dir)

    # Проверяет, существует ли тестовый XML файл
    def is_example_exist(self):
        return os.path.isfile(self._path_to_xml_example)

    # Оборачивает входные данные в XML тег input
    def wrap_input(self, text):
        return "<input>" + text + "</input>"

    # Оборачивает входные данные в XML тег output
    def wrap_output(self, text):
        return "<output>" + text + "</output>"

    # Оборачивает входные данные в XML тег example
    def wrap_example(self, text):
        eof = self._eof
        return "<example>" + eof + text + eof + "</example>"

    # Создаёт примеры для XML файла
    def create_examples(self, inputs_outputs_json):

        examples = ""
        eof = self._eof
        items = list

        try:
            items = json.loads(inputs_outputs_json)
        except:
            self._errors.append("Cannot parse input-output JSON")
            return False

        for item in items:
            input_text = str(item.input)
            output_text = str(item.output)
            text = self.wrap_input(input_text) + eof + self.wrap_output(output_text)
            text = self.wrap_example(text)
            examples = examples + text + eof

        return examples

    # Создаёт папку для задачи
    def create_problem_folder(self, path_to_contest_folder, problem_id):
        problem_folder = path_to_contest_folder + str(problem_id) + "/"
        tests_folder = problem_folder + "tests/"

        if not self.is_contest_dir_exist(path_to_contest_folder):
            self._errors.append("Contest dir for task doesn't exist")
            return False

        try:
            os.mkdir(problem_folder)
        except:
            self._errors.append("Cannot create folder for problem")
            return False

        try:
            os.mkdir(tests_folder)
        except:
            self._errors.append("Cannot create test folder for problem")
            return False

        return problem_folder

    # Создаёт XML файл с описанием задачи
    # path_to_contest_folder - путь до папки контеста
    # id - ID задачи в базе данных
    # xml_task_id - ID задачи для XML
    def create_xml(self, path_to_problem_folder, id, xml_task_id):
        task_id_xml = str(xml_task_id)
        task_id = int(id)

        if not self.is_example_exist():
            self._errors.append("XML template for task doesn't exist")
            return False

        if not self.is_contest_dir_exist(path_to_problem_folder):
            self._errors.append("Contest dir for task doesn't exist")
            return False

        try:
            problem = Problems.objects.get(id=task_id)
        except:
            self._errors.append("Cannot get Problem with id: " + str(task_id))
            return False

        title = problem.title
        description = problem.description
        inputs_outputs_json = problem.input_output_examples
        examples = self.create_examples(inputs_outputs_json)

        example_filedata = ""
        output_xml = path_to_problem_folder + self._xml_name

        with open(self._path_to_xml_example) as fp:
            example_filedata = fp.read()

        example_filedata = example_filedata.replace("{{ ID }}", id)
        example_filedata = example_filedata.replace("{{ title }}", title)
        example_filedata = example_filedata.replace("{{ description }}", description)
        example_filedata = example_filedata.replace("{{ examples }}", examples)

        with open(output_xml, "w") as fp2:
            fp2.write(example_filedata)

        return True



# Вспомогательный класс для парсинга настроек контеста
class MultiDict(OrderedDict):
    _unique = 0   # class variable

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += "_" + str(self._unique)
        OrderedDict.__setitem__(self, key, val)


# Класс для парсинга настроек контеста
class SettingParser(object):

    # Удаляет номер из названия ключа при парсинге
    def delete_number_in_key(self, keyvalue):
        keyname = str(keyvalue)
        clear_keyname = re.sub('_[\d]+', '', keyname)
        return clear_keyname

    # Конвертирует строку из Windows-1251 в UTF-8
    def convert_from_windows1251_to_utf8(self, value):
        string = str(value)
        decoded_string = ""
        try:
            decoded_string = string.encode('windows-1251').decode('utf-8')
        except:
            decoded_string = string

        return decoded_string

    # Парсит конфиг контеста
    # Возвращает словарь
    def parse_config(self, filepath):
        config_data = dict()
        config = configparser.RawConfigParser(strict=False, allow_no_value=True, dict_type=MultiDict)

        with open(filepath) as fp:
            config.read_file(itertools.chain(['[general]'], fp), source=filepath)

        for key in config:
            config_data[key] = dict()
            for i in config.items(key):
                item_key = self.convert_from_windows1251_to_utf8(i[0])
                item_value = self.convert_from_windows1251_to_utf8(i[1])
                config_data[key][item_key] = item_value

        return config_data


# Класс-менеджер для обработки контестов
class ContestsManager(object):

    _errors = list()
    _problems_folder = "problems/"

    # Возвращает список ошибок
    @property
    def get_error_list(self):
        if not len(self._errors):
            return False

        return self._errors

    # Основная директория с контестами
    @property
    def main_dir(self):
        return settings.EJUDGE_CONTEST_PATH

    # Директория с Xml контестов
    @property
    def xml_contests_dir(self):
        return settings.EJUDGE_CONTEST_SETTINGS_PATH

    # Префикс для пути к файлу конфигурации
    @property
    def conf_prefix(self):
        return '/conf/serve.cfg'

    # Загружает данные о контестах для пользователя
    def upload_user_contests(self, user_id):
        user_contests = list()
        user_contests_obj = Cntsregs.objects.all().filter(user=user_id)
        for contest_object in user_contests_obj:
            contest_id = contest_object.contest_id
            user_contests.append(contest_id)

        return user_contests

    # Регистрирует пользователя на соревнование
    def reg_user_to_contest(self, user_id, contest_id):
        error = ""
        try:
            user = Logins.objects.get(user_id=user_id)
        except:
            error = "Cannot get User"
            return error
        try:
            is_register_exist = Cntsregs.objects.filter(user=user, contest_id=contest_id).exists()
        except:
            error = "Cannot check if record exist"
            return error
        if not is_register_exist:
            try:
                Cntsregs.objects.create(user=user, contest_id=contest_id, status=0)
            except:
                error = "Cannot add User to Contest"
                return error
        else:
            error = "Record already exist"
            return error

        return False


    # Генерирует путь к файлу конфигурации
    def get_config_path(self, full_id):
        return self.main_dir + str(full_id) + self.conf_prefix

    # Генерирует путь к папке с контестом
    def get_contest_dir(self, full_id):
        return self.main_dir + str(full_id) + "/"

    # Генерирует путь к файлу XML конфигурации
    def get_xml_config_path(self, full_id):
        return self.xml_contests_dir + str(full_id) + ".xml"

    # Существует ли файл конфигурации
    def is_config_exist(self, full_id):
        return os.path.isfile(self.main_dir + str(full_id) + self.conf_prefix)

    # Существует ли файл xml конфигурации
    def is_xml_config_exist(self, full_id):
        return os.path.isfile(self.xml_contests_dir + str(full_id) + ".xml")

    # Получает список всех xml для директорий
    def get_contests_xml_list(self):
        directory = self.xml_contests_dir
        if not os.path.isdir(directory):
            raise Exception("Директория с контестами не обнаружена")
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and re.search('.xml', f)]

        return files

    # Получает данные о контесте из xml
    def parse_contest_xml(self, filepath):
        if not os.path.isfile(filepath):
            return False
        try:
            file = open(filepath, 'r', encoding="utf-8")
        except IOError:
            return False

        soup = BeautifulSoup(file, 'xml')
        info = {
            "name": soup.find('name').get_text(),
            "sched_time": soup.find('sched_time').get_text(),
        }
        file.close()

        return info

    # Получает ID контеста из названия файла xml
    def parse_contest_id_from_xml(self, xmlname):
        search = re.match(r'\d+', str(xmlname))
        if search is not None:
            return search.group(0)
        else:
            return None

    # Парсит настройки контеста
    # Возвращает словарь или False
    def parse_contest_settings(self, contest_full_id):

        if not self.is_config_exist(contest_full_id):
            return False

        config_path = self.get_config_path(contest_full_id)
        setting_parser = SettingParser()
        config_data = setting_parser.parse_config(config_path)

        return config_data

    # Получает список id всех контестов из xml
    def get_contests_ids(self, filenames):
        ids = list()
        for filename in filenames:
            contest_id = self.parse_contest_id_from_xml(filename)
            ids.append(contest_id)
        return ids

    # Получает данные о контесте
    def get_contest(self, contest_full_id):
        contest = dict()
        contest_id = int(contest_full_id)
        contest_settings = ""
        contest_config_path = ""
        contest_xml_config_path = ""
        contest_info = dict()

        # Полный путь к файлу конфигурации контеста
        if (self.is_config_exist(contest_full_id)):
            contest_config_path = self.get_config_path(contest_full_id)
            try:
                contest_settings = self.parse_contest_settings(contest_full_id)
            except:
                contest_settings = dict()
                self._errors.append("Cannot parse contest settings")


        # Полный путь к xml файлу конфигурации контеста
        if (self.is_xml_config_exist(contest_full_id)):
            contest_xml_config_path = self.get_xml_config_path(contest_full_id)
            try:
                contest_info = self.parse_contest_xml(contest_xml_config_path)
            except:
                contest_info = dict()
                self._errors.append("Cannot parse contest XML")

        # Данные об контестах
        contest["full_id"] = contest_full_id
        contest["id"] = contest_id
        contest["dir"] = self.get_contest_dir(contest_full_id)
        contest["problems_dir"] = self.get_contest_dir(contest_full_id) + self._problems_folder

        if "name" in contest_info:
            contest["name"] = contest_info["name"]
        else:
            contest["name"] = "Unknown"
        if "sched_time" in contest_info:
            contest["sched_time"] = contest_info["sched_time"]
        else:
            contest["sched_time"] = "Unknown"

        contest["xml_config_path"] = contest_xml_config_path
        contest["config_path"] = contest_config_path
        contest["settings"] = contest_settings

        return contest

    # Получает данные о всех контестах
    def get_contests(self):
        contests = list()
        contest_xmls = self.get_contests_xml_list()

        for xml in contest_xmls:
            contest_full_id = self.parse_contest_id_from_xml(xml)
            contest = self.get_contest(contest_full_id)
            contests.append(contest)

        return contests