from django.db import connection, connections
from bs4 import BeautifulSoup
from . import log
from os import listdir
from os.path import isfile, join
import re
from blog.models import Cntsregs

EJUDGE_CONTEST_PATH = '/home/judges/data/contests'


class EjudgeContests:

    def __init__(self, contest_id, contest_name):
        super(EjudgeContests, self).__init__()
        self.contest_id = contest_id
        self.contest_name = contest_name


# Получает список всех файлов в директории
def get_contest_list():
    directory = EJUDGE_CONTEST_PATH
    files = [f for f in listdir(directory) if isfile(join(directory, f)) and re.search('.xml', f)]
    return files


# Получает название контеста
def parse_contest_name(filename):
    directory = EJUDGE_CONTEST_PATH
    path = join(directory, filename)
    file = open(path, 'r', encoding="utf-8")
    xml = file.read()
    soup = BeautifulSoup(xml, 'xml')
    name = soup.find('name').get_text()
    file.close()
    return name


def get_contests_data(filter_id_set=[], include=False):
    data = []
    files = get_contest_list()
    if not files:
        return False
    files.sort()
    i = 1
    for filename in files:
        if include:
            if i in filter_id_set:
                contest_name = parse_contest_name(filename)
                contest_id = i
                contest = EjudgeContests(contest_id, contest_name)
                data.append(contest)
        else:
            if i not in filter_id_set:
                contest_name = parse_contest_name(filename)
                contest_id = i
                contest = EjudgeContests(contest_id, contest_name)
                data.append(contest)
        i += 1
    return data


def get_user_contests(user_id):
    contest_ids = list()
    try:
        user_contests = Cntsregs.objects.filter(user_id=user_id)
    except Exception:
        return contest_ids
    for contest in user_contests:
        contest_ids.append(contest.contest_id)
    return contest_ids


def register_to_contest(user_id, contest_id):
    try:
        Cntsregs.objects.create(user_id=user_id, contest_id=contest_id, status=0)
        return True
    except Exception:
        log.write("Cannot create new note in reg_to_contest")
        return False


def register_exist(user_id, contest_id):
    try:
        Cntsregs.objects.get(user_id=user_id, contest_id=contest_id)
        return True
    except Exception:
        return False


def delete_contests(user_id, contest_id):
    try:
        note = Cntsregs.objects.get(user_id=user_id, contest_id=contest_id)
        note.delete()
        return True
    except Exception:
        log.write("Cannot delete contest")
        return False