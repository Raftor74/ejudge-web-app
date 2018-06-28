""" Класс для работы с контестами """
import os
import re
import json
import string
import shutil
import configparser, itertools
from collections import OrderedDict
from bs4 import BeautifulSoup
from mysite import settings
from .models import Cntsregs, Logins, Contests, Problems
from problems.classes import ProblemsCreator


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
    def get_errors(self):
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

    # Создаёт все необходимые папки для контеста
    def create_contest_dirs(self, full_id):
        contest_folder = self.main_dir + str(full_id) + "/"

        if os.path.isdir(contest_folder):
            self._errors.append("Contest dir already exist")
            return False

        conf_folder = contest_folder + "conf/"
        problems_folder = contest_folder + "problems/"
        var_folder = contest_folder + "var/"
        include_var_folders = ["archive", "run", "status", "team_extra", "work"]

        try:
            os.mkdir(contest_folder)
            os.mkdir(conf_folder)
            os.mkdir(problems_folder)
            os.mkdir(var_folder)
            for folder in include_var_folders:
                path = var_folder + folder + "/"
                os.mkdir(path)
        except:
            self._errors.append("Cannot create contest folders")
            return False

        return True

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

    # Существует ли директория с контестом
    def is_contest_dir_exist(self, full_id):
        return os.path.isdir(self.main_dir + str(full_id) + "/")

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

        try:
            name = soup.find('name').get_text()
        except:
            name = "Unknown"

        try:
            sched_time = soup.find('sched_time').get_text()
        except:
            sched_time = "Unknown"

        info = {
            "name": name,
            "sched_time": sched_time,
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
                #self._errors.append("Cannot parse contest settings")


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

    # Получает следующий уникальный FULL ID
    def get_next_full_id(self):
        contests = Contests.objects.all()
        ids = list()
        for contest in contests:
            ids.append(int(contest.full_id))
        if len(ids):
            last_id = int(max(ids))
            next_id = last_id + 1
        else:
            next_id = 1
        full_id = str(next_id)

        while len(full_id) != 6:
            full_id = "0" + full_id

        # Генерируем уникальный Full ID
        count = 0
        while self.is_contest_dir_exist(full_id):
            full_id = str(int(full_id) + 1)
            while len(full_id) != 6:
                full_id = "0" + full_id
            count = count + 1
            if count > 100:
                break

        return full_id

    # Сохраняет контест в БД
    def save_contest(self, form_data):
        name = form_data.get('name')
        sched_time = form_data.get('sched_time')
        problems = form_data.get('tasks')
        duration = form_data.get('duration')

        try:
            full_id = self.get_next_full_id()
        except:
            self._errors.append("Не могу получить следующий FULL_ID")
            return False

        contest_dir = self.get_contest_dir(full_id)
        xml_config_path = self.get_xml_config_path(full_id)
        config_path = self.get_config_path(full_id)

        try:
            Contests.objects.create(name=name,
                                    sched_time=sched_time,
                                    problems=problems,
                                    full_id=full_id,
                                    contest_dir=contest_dir,
                                    duration=duration,
                                    xml_config_path=xml_config_path,
                                    config_path=config_path)
        except:
            self._errors.append("Не удалось создать контест")
            return False

        return True

    # Создаёт XML файл для контеста
    def create_contest_xml(self, contest):
        filepath = self.get_xml_config_path(contest.full_id)
        xml_template = settings.EJUDGE_FILE_EXAMPLES_FOLDER + "config.xml"

        if os.path.isfile(filepath):
            self._errors.append("XML файл для контеста уже существует")
            return False

        if not os.path.isfile(xml_template):
            self._errors.append("Шаблон XML для контеста не существует")
            return False

        if contest.sched_time != "":
            sched_time = '<sched_time>' + contest.sched_time + '</sched_time>'
        else:
            sched_time = ""

        if contest.name != "":
            name = contest.name
        else:
            name = ""

        try:
            with open(xml_template, encoding="utf-8") as fp:
                xml_example_data = fp.read()

            xml_example_data = xml_example_data.replace("{{ name }}", name)
            xml_example_data = xml_example_data.replace("{{ sched_time }}", sched_time)
        except:
            self._errors.append("Не могу прочитать XML шаблон для контеста")
            return False

        try:
            with open(filepath, mode="w", encoding="utf-8") as fp2:
                fp2.write(xml_example_data)
        except:
            self._errors.append("Не могу создать XML для контеста")
            return False

        return True

    # Сворачивает контест
    def undeploy_contest(self, contest_id):

        try:
            contest_id = int(contest_id)
            contest = Contests.objects.get(pk=contest_id)
        except:
            self._errors.append("Ошибка получения контеста")
            return False

        if os.path.isfile(contest.config_path):
            os.remove(contest.config_path)

        if os.path.isfile(contest.xml_config_path):
            os.remove(contest.xml_config_path)

        if os.path.isdir(contest.contest_dir):
            shutil.rmtree(contest.contest_dir)

        ejudge_contest_id = int(contest.full_id)
        Cntsregs.objects.filter(contest_id=ejudge_contest_id).delete()

        return True

    # Разворачивает контест
    def deploy_contest(self, contest_id):
        # Шаг 1. Получаем контест
        try:
            contest_id = int(contest_id)
            contest = Contests.objects.get(pk=contest_id)
        except:
            self._errors.append("Ошибка получения контеста")
            return False

        # Шаг 2. Получаем связанные с ним задачи
        try:
            tasks = json.loads(contest.problems)
        except:
            self._errors.append("Не могу распарсить JSON с задачами")
            return False

        problems = list()

        for task in tasks:
            try:
                item = Problems.objects.get(pk=task["id"])
                problems.append(item)
            except:
                self._errors.append("Не могу получить задачу с ID " + task["id"])
                continue

        # Шаг 3. Создаём все папки
        create_dir_success = self.create_contest_dirs(contest.full_id)

        if not create_dir_success:
            self._errors.append("Ошибка создания директорий контеста")
            return False

        create_xml_success = self.create_contest_xml(contest)

        if not create_xml_success:
            self._errors.append("Ошибка создания XML для контеста")
            return False

        problemsManager = ProblemsCreator()
        # Каждой задаче задаём свой короткий буквенный ID
        problemsShortIds = list(string.ascii_uppercase)
        max_length = len(problemsShortIds)
        i = 0
        problems_dir = contest.contest_dir + "problems/"
        problems_configs = ""
        for problem in problems:
            if i >= max_length:
                break

            problem_id = problemsShortIds[i]
            create_problem_dir_success = problemsManager.create_problem_folder(problems_dir, problem_id)

            if not create_problem_dir_success:
                self._errors.append("Не могу создать директорию для задачи " + problem.title)
                return False

            create_xml_success = problemsManager.create_xml(create_problem_dir_success, problem.id, problem_id)

            if not create_xml_success:
                self._errors.append("Не могу создать XML для задачи " + problem.title)
                return False

            problem_dir = create_problem_dir_success + "/tests/"

            create_tests_success = problemsManager.create_tests(problem_dir, problem.tests)

            if not create_tests_success:
                self._errors.append("Не могу создать тесты для задачи " + problem.title)
                return False

            problems_config = problemsManager.get_problem_config(problem, i + 1, problem_id)
            problems_configs = problems_configs + problems_config + "\n"

            i = i + 1

        contest_config_template = settings.EJUDGE_FILE_EXAMPLES_FOLDER + "serve.cfg"

        with open(contest_config_template, mode="r", encoding="utf-8") as fp:
            serveCfg = fp.read()

        serveCfg = serveCfg.replace("{{ duration }}", str(contest.duration))
        serveCfg = serveCfg.replace("{{ problems }}", problems_configs)

        with open(contest.config_path, mode="w", encoding="utf-8") as fp2:
            fp2.write(serveCfg)

        try:
            self.reg_user_to_contest(1, int(contest.full_id))
        except:
            self._errors.append("Не могу зарегистрировать администратора")

        return True