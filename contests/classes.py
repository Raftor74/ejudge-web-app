""" Класс для работы с контестами """
import os
import re
import configparser, itertools
from collections import OrderedDict
from bs4 import BeautifulSoup
from mysite import settings
from .models import Cntsregs, Logins


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
            contest_settings = self.parse_contest_settings(contest_full_id)

        # Полный путь к xml файлу конфигурации контеста
        if (self.is_xml_config_exist(contest_full_id)):
            contest_xml_config_path = self.get_xml_config_path(contest_full_id)
            contest_info = self.parse_contest_xml(contest_xml_config_path)

        contest["full_id"] = contest_full_id
        contest["id"] = contest_id

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