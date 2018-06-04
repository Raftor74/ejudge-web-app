from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from mysite import settings
from .classes import ContestsManager
from users.classes import UserHelper


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
        "unavaliable_contests": unavaliable_contests
    }

    return render(request, 'contests/index.html', data)