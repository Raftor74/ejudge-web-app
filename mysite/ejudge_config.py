# Ejudge config parametrs

# Путь к программе запуска
EJUDGE_CONTROL_PATH = '/home/ejudge/inst-ejudge/bin/ejudge-control'

# Путь к папке с контестами
EJUDGE_CONTEST_PATH = '/home/judges/'

# Путь к папке с настройками контестов
EJUDGE_CONTEST_SETTINGS_PATH = '/home/judges/data/contests/'

# Путь к файлам шаблонам
EJUDGE_FILE_EXAMPLES_FOLDER = "/var/www/djangosite/mysite/ejudge_examples/"

EJUDGE_CHECKERS = [
    {
        'value': 'cmp_file',
        'description': 'Cравнение двух файлов'
    },
    {
        'value': 'cmp_file_nospace',
        'description': 'Cравнение двух файлов с игнорированием повторяющихся пробелов'
    },
    {
        'value': 'cmp_bytes',
        'description': 'Cравнение двух файлов байт в байт'
    },
    {
        'value': 'cmp_int',
        'description': 'Cравнение двух знаковых 32-битных целых чисел'
    },
    {
        'value': 'cmp_int_seq',
        'description': 'Cравнение двух последовательностей знаковых 32-битных целых чисел'
    },
    {
        'value': 'cmp_long_long',
        'description': 'Cравнение двух знаковых 64-битных целых чисел'
    },
    {
        'value': 'cmp_long_long_seq',
        'description': 'Сравнение двух последовательностей знаковых 64-битных целых чисел'
    },
    {
        'value': 'cmp_unsigned_int',
        'description': 'Cравнение двух беззнаковых 32-битных целых чисел'
    },
    {
        'value': 'cmp_unsigned_int_seq',
        'description': 'Cравнение двух последовательностей беззнаковых 32-битных целых чисел'
    },
    {
        'value': 'cmp_unsigned_long_long',
        'description': 'Cравнение двух беззнаковых 64-битных целых чисел'
    },
    {
        'value': 'cmp_unsigned_long_long_seq',
        'description': 'Cравнение двух последовательностей беззнаковых 64-битных целых чисел'
    },
    {
        'value': 'cmp_huge_int',
        'description': 'Cравнение двух целых чисел произвольного размера'
    },
    {
        'value': 'cmp_double',
        'description': 'Cравнение двух вещественных чисел двойной точности с заданной максимальной ошибкой'
    },
    {
        'value': 'cmp_double_seq',
        'description': 'Cравнение двух последовательностей вещественных чисел двойной точности с заданной максимальной ошибкой'
    },
    {
        'value': 'cmp_long_double',
        'description': 'Cравнение двух вещественных чисел расширенной точности с заданной максимальной ошибкой'
    },
    {
        'value': 'cmp_long_double_seq',
        'description': 'Cсравнение двух последовательностей вещественных чисел расширенной точности с заданной максимальной ошибкой'
    },
    {
        'value': 'cmp_sexpr',
        'description': 'Cравнение двух вещественных чисел расширенной точности с заданной максимальной ошибкой'
    },
    {
        'value': 'cmp_yesno',
        'description': 'Сравнение двух ответов YES или NO'
    },
]
