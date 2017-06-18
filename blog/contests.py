from django.db import connection, connections
from bs4 import BeautifulSoup
from . import log
from os import listdir
from os.path import isfile, join
import re


EJUDGE_CONTEST_PATH = '/home/judges/data/contests'

class EjudgeContests():

	def __init__(self,contest_id,name):
		self.name = name
		self.id = contest_id

	def get_contest_list():
		directory = EJUDGE_CONTEST_PATH
		files = [f for f in listdir(directory) if isfile(join(directory, f)) and re.search('.xml',f)]
		return files


	def parse_contest_name(filename):
		directory = EJUDGE_CONTEST_PATH
		path = join(directory,filename)
		file = open(path,'r',encoding="utf-8")
		xml = file.read()
		soup = BeautifulSoup(xml,'xml')
		name = soup.find('name').get_text()
		file.close()
		return name

	def get_contests_data(filter_id_set = [],include = False):
		data = []
		files = EjudgeContests.get_contest_list()
		files.sort()
		i = 1
		for filename in files:
			if include:
				if i in filter_id_set:
					contest_name = EjudgeContests.parse_contest_name(filename)
					contest_id = i
					contest = EjudgeContests(contest_id,contest_name)
					data.append(contest)
			else:
				if i not in filter_id_set:
					contest_name = EjudgeContests.parse_contest_name(filename)
					contest_id = i
					contest = EjudgeContests(contest_id,contest_name)
					data.append(contest)
			i += 1
		return data

	def get_user_contest(user_id):
		_user_id = str(user_id)
		error = ''
		try:
			ejudge_db = connections['ejudge'].cursor()
		except Exception:
			error = "Cannot connect to database"
			return {'data':False,'error':error}
		try:
			sql = "SELECT contest_id FROM cntsregs WHERE user_id=%s"
			data = (_user_id)
			ejudge_db.execute(sql,data)
		except Exception:
			error = "Error in SQL Query. Get user contests function"
			return {'data':False,'error':error}
		try:
			contests_ids = ejudge_db.fetchall()
			data = []
			for contest_id in contests_ids:
				data.extend(contest_id)
			return {'data':data,'error':error}
		except Exception:
			error = "No data"
			return {'data':False,'error':error}


	def register_to_contest(user_id,contest_id):
		_user_id = str(user_id)
		_contest_id = str(contest_id)
		error = ''
		try:
			ejudge_db = connections['ejudge'].cursor()
		except Exception:
			error = "Cannot connect to database"
			return {'data':False,'error':error}
		try:
			sql = "INSERT INTO cntsregs (user_id,contest_id,status) VALUES (%s,%s,0)"
			data = (_user_id,_contest_id)
			ejudge_db.execute(sql,data)
			return {'data':True,'error':error}
		except Exception:
			error = "Error in SQL Query. Register contest function"
			return {'data':False,'error':error}

	def register_exist(user_id,contest_id):
		_user_id = int(user_id)
		_contest_id = int(contest_id)
		try:
			ejudge_db = connections['ejudge'].cursor()
		except Exception:
			log.write("Cannot connect to database")
			return True
		try:
			sql = "SELECT * FROM cntsregs WHERE user_id = %s AND contest_id = %s"
			data = (_user_id,_contest_id)
			ejudge_db.execute(sql,data)
		except Exception:
			log.write("Error in SQL Query. Register exist function")
			return True
		try:
			exist = ejudge_db.fetchone()[0]
			return True
		except Exception:
			return False

	def delete_contests(user_id,contest_id):
		_user_id = int(user_id)
		_contest_id = int(contest_id)
		try:
			ejudge_db = connections['ejudge'].cursor()
		except Exception:
			log.write("Cannot connect to database")
			return False
		try:
			sql = "DELETE FROM cntsregs WHERE user_id = %s AND contest_id = %s"
			data = (_user_id,_contest_id)
			ejudge_db.execute(sql,data)
			return True
		except Exception:
			log.write("Error in SQL Query. Delete contest function")
			return False
