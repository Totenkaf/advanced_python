import random
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from askme_app.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from askme_app.forms import *
from askme.settings import LOGIN_URL
from django.views.decorators.http import require_http_methods

def paginate(list_data, per_page, curr_page):
    paginator = Paginator(list_data, per_page)
    num_pages = paginator.num_pages
    if curr_page < 0 or curr_page >= num_pages: # проверяем, что текущая не вылезла за все страницы
        return (0, [])
    page = paginator.page(curr_page + 1)
    paginator_data = {
        'enabled_previous': page.has_previous(), #есть ли предыдущая страница
        'page_start': 1,
        'prev_prev_page': curr_page - 1,
        'prev_page': curr_page,
        'page': curr_page + 1,
        'next_page': curr_page + 2,
        'next_next_page': curr_page + 3,
        'page_prev_end': num_pages - 1,
        'page_end': num_pages,
        'enabled_next': page.has_next()
    }
    return (page, paginator_data)


def index(request: HttpRequest):
    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    questions = Question.manager.get_new_questions()
    page, paginator_data = paginate(questions, 10, input_page)
    if not paginator_data:
        return HttpResponse(status=404)

    tags = Tag.manager.top_of_tags(10)
    members = Profile.manager.top_of_profiles(10)

    context = {
        'questions': page.object_list,
        'paginator': paginator_data,
        'curr_url': 'index',
        'tags': tags,
        'members': members
    }
    return render(request, 'index.html', context=context)


def question(request: HttpRequest, question_id: int):
    try:
        question_item = Question.manager.get_question_by_id(question_id)
    except:
        return HttpResponseBadRequest()

    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    ANSWERS = question_item.get_answers()
    TAGS = Tag.manager.top_of_tags(10)
    MEMBERS = Profile.manager.top_of_profiles(10)

    page, paginator_data = paginate(ANSWERS, 5, input_page)
    if not page and len(list(ANSWERS)) != 0:
        return HttpResponse(status=404)

    if request.method == "POST":
        if not request.user.is_authenticated:
            response = redirect(LOGIN_URL)
            response['Location'] += f'?next={request.get_full_path()}'
            return response

        text = request.POST['text']
        profile_id = Profile.manager.get_profile_by_user_id(request.user.id).id
        answer_form = AnswerForm(request.POST, question_id=question_id, profile_id=profile_id, initial={'text': text})
        if answer_form.is_valid():
            new_answer = answer_form.save()
            if new_answer:
                ANSWERS = question_item.get_answers()
                id_answers = list(question_item.get_id_answers())
                need_page = id_answers.index((new_answer.id,)) // 5

                response = redirect('question', question_id)
                response['Location'] += f'?page={need_page}' + f'#answer-{new_answer.id}'
                return response

    elif request.method == "GET":
        answer_form = AnswerForm()

    context = {'curr_user': request.user, 'request': request, 'question': question_item, 'id': question_id,
        'answers': page.object_list, 'paginator': paginator_data, 'curr_url': 'question', 'tags': TAGS,
        'members': MEMBERS, 'answer_form': answer_form, 'input_page': input_page}
    return render(request, 'question.html', context=context)


@require_http_methods(["POST"])
def like_question(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'not_auth'})
    try:
        question_id = int(request.POST['question_id'])
        islike = int(request.POST['islike'])

        some_question = Question.objects.get_question_by_id(question_id)

        profile_id = request.user.profile.id

        if islike == 0:
            VoteQuestion.objects.create_vote_question_by_profile_and_question_id(question_id, profile_id)
            islike = 1
        elif islike == 1:
            vote = VoteQuestion.objects.get_vote_question_by_profile_and_question_id(question_id, profile_id)
            vote.delete()
            islike = 0

        return JsonResponse({'status': 'ok', 'islike': islike, 'likes_count': some_question.get_likes_count()})
    except:
        return JsonResponse({'status': 'error'})

def hot(request: HttpRequest):
    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    questions = Question.manager.get_top_questions()
    page, paginator_data = paginate(questions, 10, input_page)
    if not paginator_data:
        return HttpResponse(status=404)

    tags = Tag.manager.top_of_tags(10)
    members = Profile.manager.top_of_profiles(10)

    context = {'questions': page.object_list, 'paginator': paginator_data,
        'curr_url': 'hot', 'tags': tags, 'members': members}
    return render(request, 'hot.html', context=context)


@login_required
def settings(request: HttpRequest):

    if request.method == "POST":
        curr_username, email, avatar = request.user.username, request.POST['email'], request.POST['avatar']

        settings_form = SettingsForm(request.POST, request=request, initial={'username': curr_username, 'email': email, 'avatar': avatar})

        if settings_form.is_valid():
            settings_form.update()

    elif request.method == "GET":
        user_id = request.user.id
        user, profile = Profile.manager.get_user_by_id(user_id), Profile.manager.get_profile_by_user_id(user_id)
        settings_form = SettingsForm(initial={'username': user.username, 'email': user.email, 'avatar': profile.avatar})

    TAGS = Tag.manager.top_of_tags(10)
    MEMBERS = Profile.manager.top_of_profiles(10)

    context = {'curr_user': request.user, 'request': request,
        'curr_url': 'settings', 'tags': TAGS, 'members': MEMBERS,
        'form': settings_form}
    return render(request, 'settings.html', context=context)


def tag(request: HttpRequest, tag_name: str):
    input_page = request.GET.get('page', '0')
    if not input_page.isdigit():
        return HttpResponse(status=404)
    input_page = int(input_page)

    try:
        questions = Tag.manager.get_questions_by_tag(tag_name)
    except:
        return HttpResponseBadRequest()

    page, paginator_data = paginate(questions, 10, input_page)
    if not paginator_data:
        return HttpResponse(status=404)

    tags = Tag.manager.top_of_tags(10)
    members = Profile.manager.top_of_profiles(10)

    context = {'tag': tag_name, 'questions': page.object_list, 'paginator': paginator_data,
        'curr_url': 'tag', 'tags': tags, 'members': members}
    # context = {'questions': page.object_list, 'paginator': paginator_data, 'curr_url': 'tag'}
    return render(request, 'tag.html', context=context)

@login_required
def ask(request: HttpRequest):

    if request.method == "POST":
        title, text, tags = request.POST['title'], request.POST['text'], request.POST['tags']
        profile_id = Profile.objects.get_profile_by_user_id(request.user.id).id
        ask_form = AskForm(request.POST, profile_id=profile_id, initial={"title": title, "text": text, "tags": tags})
        if ask_form.is_valid():
            new_question = ask_form.save()
            if new_question:
                return redirect('question', question_id=new_question.id)

    elif request.method == "GET":
        ask_form = AskForm()

    TAGS = Tag.manager.top_of_tags(10)
    MEMBERS = Profile.manager.top_of_profiles(10)

    context = {'curr_user': request.user, 'request': request, 'curr_url': 'ask', 'tags': TAGS,
        'members': MEMBERS, 'ask_form': ask_form}
    return render(request, 'ask.html', context=context)


def signup(request: HttpRequest):

    if request.method == "POST":
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                auth_login(request, user)
                return redirect('index')

    elif request.method == "GET":
        signup_form = SignUpForm()

    TAGS = Tag.manager.top_of_tags(10)
    MEMBERS = Profile.manager.top_of_profiles(10)

    context = {'curr_user': request.user, 'curr_url': 'sign_up', 'request': request,
        'form': signup_form, 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'sign_up.html', context=context)


def login(request: HttpRequest):

    next_url = request.GET.get('next', 'index')

    if request.method == "POST":

        login_form = LoginForm(request.POST, request=request)

        if login_form.is_valid():
            user = authenticate(request=request, **login_form.cleaned_data)
            if user is not None:
                auth_login(request, user)
                return redirect(next_url)

    elif request.method == "GET":
        login_form = LoginForm()

    TAGS = Tag.manager.top_of_tags(10)
    MEMBERS = Profile.manager.top_of_profiles(10)

    context = {'curr_user': request.user, 'request': request, 'curr_url': 'login',
        'form': login_form, 'next_url': next_url, 'tags': TAGS, 'members': MEMBERS}
    return render(request, 'login.html', context=context)

@require_http_methods(["POST"])
def like_answer(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'not_auth'})
    try:
        answer_id = int(request.POST['answer_id'])
        islike = int(request.POST['islike'])

        some_answer = Answer.objects.get_answer_by_id(answer_id)

        profile_id = request.user.profile.id

        if islike == 0:
            AnswerLike.objects.create_vote_answer_by_profile_and_answer_id(answer_id, profile_id)
            islike = 1
        elif islike == 1:
            vote = AnswerLike.objects.get_vote_answer_by_profile_and_answer_id(answer_id, profile_id)
            vote.delete()
            islike = 0

        return JsonResponse({'status': 'ok', 'islike': islike, 'likes_count': some_answer.get_likes_count()})
    except:
        return JsonResponse({'status': 'error'})


@require_http_methods(["POST"])
def marked_as_correct(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'not_auth'})
    try:
        answer_id = int(request.POST['answer_id'])
        marked_as_correct = int(request.POST['marked_as_correct'])

        some_answer = Answer.objects.get_answer_by_id(answer_id)

        if marked_as_correct == 0:
            some_answer.marked_as_correct = True
            some_answer.save()
            marked_as_correct = 1
        elif marked_as_correct == 1:
            some_answer.marked_as_correct = False
            some_answer.save()
            marked_as_correct = 0

        return JsonResponse({'status': 'ok', 'marked_as_correct': marked_as_correct})
    except:
        return JsonResponse({'status': 'error'})


def logout(request: HttpRequest):
    next_url = request.GET.get('next', 'index')

    auth_logout(request)
    return redirect(next_url)




