from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache

import csv
import os

from . import quest_assist_funcs


def index(request):
    return render(request, "index.html")


def quest_list(request):
    quests = quest_assist_funcs.get_quest_for_table()
    return render(request, "quest_list.html", context={"quests": quests})


def add_quest(request):
    return render(request, "add_quest.html")


def send_quest(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_quest = request.POST.get("new_quest", "")
        new_answer = request.POST.get("new_answer", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_quest) == 0:
            context["success"] = False
            context["comment"] = "Вам нужно написать вопрос"
        elif len(new_answer) == 0:
            context["success"] = False
            context["comment"] = "Вам нужно написать ответ на вопрос"
        else:
            context["success"] = True
            context["comment"] = "Ваш пара вопрос-ответ приняты!"
            quest_assist_funcs.add_quest(new_quest, new_answer)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "send_quest.html", context)
    else:
        add_quest(request)


def write_test(request):
    quests_path = os.path.join(settings.BASE_DIR, 'data', 'quests.csv')
    questions = []

    with open(quests_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            questions.append(row['quest'])

    return render(request, 'test.html', {'questions': questions})


def test_results(request):
    if request.method == "POST":
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'quests.csv')
        correct_answers = []

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                correct_answers.append({
                    'question': row['quest'],
                    'answer': row['answer']
                })

        user_answers = []
        for idx, item in enumerate(correct_answers, start=1):
            user_input = request.POST.get(f'answer_{idx}', '').strip()
            correct_answer = item['answer'].strip()

            user_answers.append({
                'question': item['question'],
                'correct_answer': correct_answer,
                'user_answer': user_input,
                'is_correct': user_input.lower() == correct_answer.lower()
            })

        correct_count = sum(1 for item in user_answers if item['is_correct'])

        return render(request, 'test_results.html', {
            'user_answers': user_answers,
            'correct_count': correct_count,
            'total': len(user_answers)
        })


def show_stats(request):
    stats = quest_assist_funcs.get_quests_stats()
    return render(request, "stats.html", stats)