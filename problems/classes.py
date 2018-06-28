import os
import json
from mysite import settings
from .models import Problems


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
            input_text = str(item["input"])
            output_text = str(item["output"])
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

    # Создаёт тесты
    def create_tests(self, path_to_test_folder, test_json):
        test_sfx = ".dat"
        corr_sfx = ".ans"

        if not os.path.isdir(path_to_test_folder):
            return False

        tests = json.loads(test_json)

        i = 1
        for test in tests:
            index = str(i)
            input_data = test["input"]
            output_data = test["output"]

            while len(index) != 3:
                index = "0" + index

            input_filename = path_to_test_folder + index + test_sfx
            output_filename = path_to_test_folder + index + corr_sfx

            with open(input_filename, mode="w", encoding="utf-8") as fp:
                fp.write(input_data)

            with open(output_filename, mode="w", encoding="utf-8") as fp2:
                fp2.write(output_data)

            i = i + 1

        return True


    # Возвращает конфиг для задачи
    def get_problem_config(self, problem_object, number, short_name):
        template = settings.EJUDGE_FILE_EXAMPLES_FOLDER + "problem.cfg"

        with open(template, mode="r", encoding="utf-8") as fp:
            data = fp.read()

        data = data.replace("{{ ID }}", str(number))
        data = data.replace("{{ SHORT_ID }}", str(short_name))
        data = data.replace("{{ TITLE }}", str(problem_object.title))
        data = data.replace("{{ MAX_VM_SIZE }}", str(problem_object.max_vm_size) + "M")
        data = data.replace("{{ TIME_LIMIT }}", str(problem_object.max_exec_time))
        data = data.replace("{{ TIME_LIMIT }}", str(problem_object.max_exec_time))
        data = data.replace("{{ CHECKER }}", str(problem_object.comparison))

        epsilon = str(problem_object.epsilon)

        if len(epsilon):
            epsilon = 'checker_env = "EPS='+epsilon+'"'
            data = data.replace("{{ EPSILON }}", epsilon)
        else:
            data = data.replace("{{ EPSILON }}", "")

        return data


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

        example_filedata = example_filedata.replace("{{ ID }}", task_id_xml)
        example_filedata = example_filedata.replace("{{ title }}", title)
        example_filedata = example_filedata.replace("{{ description }}", description)
        example_filedata = example_filedata.replace("{{ examples }}", examples)

        with open(output_xml, mode="w", encoding="utf-8") as fp2:
            fp2.write(example_filedata)

        return True

    # Сохраняет данные с формы добавления задачи
    def save_problem(self, form_data):
        title = form_data.get('title')
        description = form_data.get('description')
        checker = form_data.get('task_checker')
        epsilon = form_data.get('eps')
        max_vm = form_data.get('max_vm')
        max_time = form_data.get('max_time')
        input_output = form_data.get('input_output')
        tests = form_data.get('tests')
        try:
            Problems.objects.create(title=title,
                                    description=description,
                                    comparison=checker,
                                    epsilon=epsilon,
                                    max_vm_size=max_vm,
                                    max_exec_time=max_time,
                                    input_output_examples=input_output,
                                    tests=tests)
        except:
            return False

        return True


    # Сохраняет данные с формы и обновляет задачу
    def update_problem(self, form_data):
        task_id = int(form_data.get('task_id'))

        try:
            task_object = Problems.objects.get(id=task_id)
        except:
            return False

        title = form_data.get('title')
        description = form_data.get('description')
        checker = form_data.get('task_checker')
        epsilon = form_data.get('eps')
        max_vm = form_data.get('max_vm')
        max_time = form_data.get('max_time')
        input_output = form_data.get('input_output')
        tests = form_data.get('tests')
        try:
            task_object.title = title
            task_object.description = description
            task_object.comparison = checker
            task_object.epsilon = epsilon
            task_object.max_vm_size = max_vm
            task_object.max_exec_time = max_time
            task_object.input_output_examples = input_output
            task_object.tests = tests
            task_object.save()
        except:
            return False

        return True