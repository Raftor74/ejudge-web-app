from time import gmtime, strftime
from os.path import join

LOG_PATH = "/var/www/djangosite/mysite/"


def write(message):
    file = open(join(LOG_PATH, "app.log"), "a")
    log_message = message + " " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n"
    file.write(log_message)
    file.close()
