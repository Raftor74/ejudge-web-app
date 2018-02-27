""" Класс для работы с контестами """
import os
import re
from bs4 import BeautifulSoup
from mysite import settings



class ContestsManager(object):

    # Основная директория с контестами
    @property
    def main_dir(self):
        return settings.EJUDGE_CONTEST_PATH

    # Директория с Xml контестов
    @property
    def xml_contests_dir(self):
        return self.main_dir + '/data/contests/'

    #Префикс для пути к файлу конфигурации
    @property
    def conf_prefix(self):
        return '/conf/serve.cfg'

    # Генерирует путь к файлу конфигурации
    def get_config_path(self, full_id):
        return self.main_dir + str(full_id) + self.conf_prefix

    # Директория с конфигурацией
    def is_config_exist(self, full_id):
        return os.path.isfile(self.main_dir + str(full_id) + self.conf_prefix)

    # Получает список всех xml для директорий
    def get_contests_xml_list(self):
        directory = self.xml_contests_dir
        if not os.path.isdir(directory):
            raise Exception("Директория с контестами не обнаружена")
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and re.search('.xml', f)]

        return files

    # Получает данные о контесте из xml
    @staticmethod
    def parse_contest_xml(filepath):

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
    @staticmethod
    def parse_contest_id_from_xml(xmlname):
        search = re.match(r'\d+', str(xmlname))
        if search is not None:
            return search.group(0)
        else:
            return None

    # Загружает данные о конфига контеста
    def upload_config_info(self, full_id):

        if not self.is_config_exist(full_id):
            return None

        filepath = self.get_config_path(full_id)
        file = open(filepath, 'r', encoding="utf-8")
        data = dict()
        for line in file.readlines():
            pattern = '^(?P<property>\w+)\s?=\s?(?P<value>[А-Яа-я\w\s]+)$'
            search = re.match(pattern, line)
            if search is not None:
                data[search.group('property')] = search.group('value')
        file.close()

        return data


    # Загружает данные xml о контестах
    def upload_xml_info(self):
        xml_names = self.get_contests_xml_list()
        contests = dict()
        for name in xml_names:
            full_id = self.parse_contest_id_from_xml(name)
            if full_id is not None:
                id = int(full_id)
            else:
                id = None

            abs_contest_path = self.xml_contests_dir + name
            contests[name] = self.parse_contest_xml(abs_contest_path)
            contests[name]["id"] = id
            contests[name]["full_id"] = full_id
            contests[name]["config"] = self.upload_config_info(full_id)
        return contests
