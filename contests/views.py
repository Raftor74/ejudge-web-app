import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from .classes import ContestsManager
from users.classes import UserHelper
from .models import Problems, Contests, Cntsregs, Logins


def index(request):
    if not UserHelper.is_auth(request):
        return redirect(reverse('login'))

    user_id = UserHelper.get_user_id(request)
    manager = ContestsManager()

    # Регистрация пользователя на соревнование
    if request.method == 'POST':
        contest_id = int(request.POST.get('contest_id'))
        is_error = manager.reg_user_to_contest(user_id, contest_id)
        if is_error:
            callback = {'success': 'fail', 'error': is_error}
        else:
            callback = {'success': 'ok', 'error': is_error}
        return JsonResponse(callback)

    user_contests = manager.upload_user_contests(user_id)
    contests = manager.get_contests()
    avaliable_contests = list()
    unavaliable_contests = list()

    # Сортируем контесты на доступные и недоступные для пользователя
    for contest in contests:
        if contest["id"] in user_contests:
            unavaliable_contests.append(contest)
        else:
            avaliable_contests.append(contest)

    data = {
        "user_id": user_id,
        "avaliable_contests": avaliable_contests,
        "unavaliable_contests": unavaliable_contests,
    }

    return render(request, 'contests/index.html', data)


# View для добавления контеста
def add(request):
    if not UserHelper.is_admin(request):
        return redirect(reverse('login'))

    manager = ContestsManager()
    if request.method == "POST":
        success = manager.save_contest(request.POST)
        if success:
            message = {'status': 'ok', 'error': ""}
        else:
            message = {'status': 'fail', 'error': "Не могу создать контест"}

        return JsonResponse(message, safe=False)

    return render(request, 'contests/add.html')


# Возвращает список задач в виде JSON
def get_problems_list(request):

    if request.method == "POST":
        problems_json = []
        problems = Problems.objects.all()
        for problem in problems:
            item = {
                "label": "ID: " + str(problem.id) + " " + str(problem.title),
                "value": "ID: " + str(problem.id) + " " + str(problem.title),
                "id": problem.id,
                "active": True
            }
            problems_json.append(item)
        try:
            problems_json = json.dumps(problems_json)
        except:
            problems_json = []

        return JsonResponse(problems_json, safe=False)
    return False

# View редактирования контеста
def edit(request, contest_id):
    if not UserHelper.is_admin(request):
        return redirect(reverse('login'))

    return render(request, 'contests/edit.html')


# View для просмотра контестов
def contest_list(request):

    if not UserHelper.is_admin(request):
        return redirect(reverse('login'))

    contests = Contests.objects.all()

    return render(request, 'contests/list.html', {'contests': contests})

# View для просмотра контеста
def show(request, contest_id):

    if not UserHelper.is_admin(request):
        return redirect(reverse('login'))

    contest = get_object_or_404(Contests, id=contest_id)
    manager = ContestsManager()
    errors = list()
    deploy_ok = ""

    if request.method == "POST":
        if "deploy" in request.POST:
            success = manager.deploy_contest(contest_id)

            if not success:
                errors = manager.get_errors()
            else:
                errors = manager.get_errors()
                deploy_ok = "Контест успешно развёрнут"

        if "undeploy" in request.POST:
            success = manager.undeploy_contest(contest_id)

            if not success:
                errors = manager.get_errors()
            else:
                errors = manager.get_errors()
                deploy_ok = "Контест успешно удалён"

    # Из JSON получает ID контестов и берём о них информацию
    tasksList = list()
    try:
        tasks = json.loads(contest.problems)
    except:
        tasks = list()
    for task in tasks:
        task_id = task["id"]
        try:
            item = Problems.objects.get(pk=task_id)
            tasksList.append(item)
        except:
            continue

    try:
        ejudge_contest_id = int(contest.full_id)
        admin = Logins.objects.filter(user_id=1)
        is_admin_registered = Cntsregs.objects.filter(user=admin, contest_id=ejudge_contest_id).exists()
    except:
        is_admin_registered = False

    contest_deploy = {
        "config": manager.is_config_exist(contest.full_id),
        "xml": manager.is_xml_config_exist(contest.full_id),
        "main_dir": manager.is_contest_dir_exist(contest.full_id),
        "admin_registered" : is_admin_registered
    }

    return render(request, 'contests/show.html', {'contest': contest,
                                                  'tasks': tasksList,
                                                  'deploy': contest_deploy,
                                                  'errors': errors,
                                                  'deploy_ok': deploy_ok})