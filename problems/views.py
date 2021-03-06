import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from .classes import ProblemsCreator
from mysite import settings
from users.classes import UserHelper
from .models import Problems


def index(request):
    if not UserHelper.is_auth(request):
        return redirect(reverse('login'))

    tasks = Problems.objects.all().order_by('createtime')
    return render(request, 'problems/index.html', {'tasks':tasks})


def show(request, task_id):
    if not UserHelper.is_auth(request):
        return redirect(reverse('login'))

    task = get_object_or_404(Problems, id=task_id)
    try:
        examples = json.loads(task.input_output_examples)
    except json.JSONDecodeError:
        examples = list()
    try:
        tests = json.loads(task.tests)
    except json.JSONDecodeError:
        tests = list()

    return render(request, 'problems/show.html', {'task': task, 'examples': examples, 'tests': tests})


def edit(request, task_id):
    if not UserHelper.is_admin(request):
        return redirect(reverse('login'))

    manager = ProblemsCreator()
    checkers = settings.EJUDGE_CHECKERS
    task = get_object_or_404(Problems, id=task_id)

    if request.method == 'POST':
        success = manager.update_problem(request.POST)
        if not success:
            message = {'status': 'fail'}
            return JsonResponse(message)
        else:
            message = {'status': 'ok'}
            return JsonResponse(message)

    try:
        examples = json.loads(task.input_output_examples)
    except json.JSONDecodeError:
        examples = list()
    try:
        tests = json.loads(task.tests)
    except json.JSONDecodeError:
        tests = list()

    examples_len = len(examples)
    tests_len = len(tests)
    return render(request, 'problems/edit.html', {'task': task,
                                                  'examples': examples,
                                                  'examples_len': examples_len,
                                                  'tests': tests,
                                                  'tests_len': tests_len,
                                                  'checkers':checkers})


def add(request):
    if not UserHelper.is_admin(request):
        return redirect(reverse('login'))

    errors = ""
    manager = ProblemsCreator()

    if request.method == 'POST':
        success = manager.save_problem(request.POST)
        if not success:
            message = {'status': 'fail'}
            return JsonResponse(message)
        else:
            message = {'status': 'ok'}
            return JsonResponse(message)
    checkers = settings.EJUDGE_CHECKERS
    return render(request, 'problems/add.html', {'checkers':checkers, 'errors':errors})