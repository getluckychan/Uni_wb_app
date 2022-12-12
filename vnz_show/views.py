from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import *
from .utils import *

# TODO: create a new view for index page


def index(request):
    if not request.user.is_authenticated:
        contex = {
            'menu': menu_not_login,
            'title': 'Home page'
        }
        return render(request, 'home/home.html', context=contex)

    current_user = get_object_or_404(MyUser, pk=request.user.id)
    if current_user.is_student is True:
        menu = menu_student
    elif current_user.is_educator is True:
        menu = menu_educator
    contex = {
        'menu': menu,
        'title': 'Home page',
        'name': current_user.full_name,
    }
    return render(request, 'home/home.html', context=contex)




def about(request):
    return HttpResponse('About page')


@login_required(login_url='/login/')
def my_profile(request):
    current_user = get_object_or_404(MyUser, pk=request.user.id)
    if current_user.is_student is True:
        menu = menu_student
    elif current_user.is_educator is True:
        menu = menu_educator
    else:
        menu = menu_not_login
        if request.method == 'POST':
            form = UserSetUp(request.POST)
            job = form.cleaned_data['job']
            if job == 'STUDENT':
                current_user.is_student = True
                current_user.save()
                return HttpResponseRedirect(reverse('sign_up_student', args=[current_user.pk]))
            elif job == 'EDUCATOR':
                current_user.is_educator = True
                current_user.save()
                return HttpResponseRedirect(reverse('sign_up_educator', args=[current_user.pk]))

        contex = {
            'menu': menu,
            'title': 'Home page',
            'name': current_user.full_name,
        }
        return render(request, 'home/home.html', context=contex)



def declined_area(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(MyUser, pk=request.user.id)
        if current_user.is_student is True:
            menu = menu_student
            text = 'Student`s are not allowed here'
        elif current_user.is_educator is True:
            menu = menu_educator
    else:
        menu = menu_not_login
        text = 'Please signin ar signup'
    contex = {
        'menu': menu,
        'title': 'Declined page',
        'text': text
    }
    return render(request, 'areas/declined.html', context=contex)


def profile(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(MyUser, pk=user_id)
        if user.is_student is True:
            profile = Student.objects.get(user=user)
            info = [profile.user, profile.speciality, profile.acception]
            menu = menu_student
        elif user.is_educator is True:
            profile = Educator.objects.get(user=user)
            info = [profile.user, profile.rank, profile.department]
            menu = menu_educator

        context = {
            'user': user,
            'menu': menu,
            'title': user.full_name,
            'info': info,
        }
        return render(request, 'home/profile.html', context=context)
    else:
        contex = {
            'menu': menu_not_login,
            'title': 'Home page'
        }
        return render(request, 'home/home.html', context=contex)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            job = form.cleaned_data['job']
            password = form.cleaned_data['password']
            print(form.cleaned_data)
            user = MyUser.objects.create_user(email, full_name, date_of_birth, password)
            if job == 'STUDENT':
                user.is_student = True
                user.save()
                my_bitch = authenticate(request, email=email, password=password)
                login(request, my_bitch)
                request.session['user_id'] = user.pk
                return HttpResponseRedirect(reverse('sign_up_student', args=[user.pk]))
            elif job == 'EDUCATOR':
                user.is_educator = True
                user.save()
                my_bitch = authenticate(request, email=email, password=password)
                login(request, my_bitch)
                request.session['user_id'] = user.pk
                return HttpResponseRedirect(reverse('sign_up_educator', args=[user.pk]))

                # return redirect('sign_up_student', kwargs={'user': user})
    else:
        form = RegistrationForm()
        context = {
            'menu': menu_not_login,
            'form': form,
            'title': 'Sign Up'
        }
        return render(request, 'registration/registration.html', context=context)


def sign_up_student(request, user_id):
    if request.method == 'POST':
        form = StudentSetUpForm(request.POST)
        if form.is_valid():
            speciality = form.cleaned_data['speciality']
            acception = form.cleaned_data['acception']
            graduation = form.cleaned_data['graduation']
            user = MyUser.objects.get(pk=user_id)
            student = Student.objects.create(user=user,
                                             speciality=speciality,
                                             acception=acception,
                                             graduation=graduation
                                             )
            student.save()
            request.session['user_id'] = user.pk
            return HttpResponseRedirect(reverse('profile', args=[user.pk]))
    else:
        form = StudentSetUpForm()
        context = {
            'menu': menu_not_login,
            'form': form,
            'title': 'Sign Up as Student'
        }
        return render(request, 'registration/as_student.html', context=context)


def sign_up_educator(request, user_id):
    if request.method == 'POST':
        form = EducatorSetUpForm(request.POST)
        if form.is_valid():
            rank = form.cleaned_data['rank']
            department = form.cleaned_data['department']
            acception = form.cleaned_data['acception']
            user = MyUser.objects.get(pk=user_id)
            educator = Educator.objects.create(user=user,
                                               rank=rank,
                                               department=department,
                                               acception=acception
                                               )
            educator.save()
            request.session['user_id'] = user.pk
            return HttpResponseRedirect(reverse('my_profile'))

    else:
        form = EducatorSetUpForm()
        context = {
            'menu': menu_not_login,
            'form': form,
            'title': 'Sign Up as Student'
        }
        return render(request, 'registration/as_educator.html', context=context)


def logout_view(request):
    logout(request)
    contex = {
        'menu': menu_not_login,
        'title': 'Home page',
        'text': 'Logout successful'
    }
    return render(request, 'home/home.html', context=contex)


def login_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('my_profile'))
                else:
                    print(form.errors)
                    return form.add_error(None, 'Incorrect email or password')
            except Exception:
                return form.add_error(None, 'Something went wrong, please try again')
    else:
        form = LoginForm()
        context = {
            'menu': menu_not_login,
            'form': form,
            'title': 'Sign In'
        }
        return render(request, 'registration/login.html', context=context)


def create_test(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(MyUser, pk=request.user.id)
        if current_user.is_educator is True:
            if request.method == 'POST':
                form = CreateTestForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    theme = data['theme']
                    subject = data['subject']
                    time = data['time']
                    author = educator_recognizer(current_user.pk)
                    test = Test.objects.create(theme=theme,
                                               author=author,
                                               subject=subject,
                                               time=time)
                    test.save()
                    return HttpResponseRedirect(reverse('create_task', args=[test.pk]))
            else:
                form = CreateTestForm()
                context = {
                    'menu': menu_educator,
                    'form': form,
                    'title': 'Create test',
                    'name': current_user.full_name,
                }
                return render(request, 'educator/create_test.html', context=context)
        else:
            return HttpResponseRedirect(reverse('declined_area'))

    else:
        contex = {
            'menu': menu_not_login,
            'title': 'Home page'
        }
        return render(request, 'home/home.html', context=contex)


# FIXME: add test creator and fix function create_task
def create_task(request, test_id):
    if request.user.is_authenticated:
        current_user = get_object_or_404(MyUser, pk=request.user.id)
        if current_user.is_educator is True:
            if request.method == 'POST':
                form = CreateTaskForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    question = data['question']
                    correct_answer = data['correct_answer']
                    incorrect_answers = data['incorrect_answers']
                    test = Test.objects.get(pk=test_id)
                    task = Task.objects.create(test=test,
                                               question=question,
                                               )
                    task.save()
                    answer_correct_in_data = Answer.objects.create(task, correct_answer)
                    answer_correct_in_data.save()
                    in_cor = incorrect_answers.split('|')
                    for i in in_cor:
                        answer_incorrect_in_data = Answer.objects.create(task, i)
                        answer_incorrect_in_data.save()
                    return HttpResponseRedirect(reverse('create_task', args=[test.pk]))
            else:
                form = CreateTaskForm()
                tests = Test.objects.get(pk=test_id)
                form_test = TestForm(instance=tests)
                try:
                    tasks = Task.objects.get(test_id=test_id)
                    form_task = TaskForm(instance=tasks)
                    answers = Answer.objects.get(task_id=tasks.pk)
                    tittle = answers.answer
                    correctnes = answers.correctness
                    context = {
                        'menu': menu_educator,
                        'form': form,
                        'form_test': form_test,
                        'form_task': form_task,
                        'name': current_user.full_name,
                    }
                    return render(request, 'educator/create_task.html', context=context)
                except Task.DoesNotExist:
                    context = {
                        'menu': menu_educator,
                        'form': form,
                        'form_test': form_test,
                        'name': current_user.full_name,
                    }
                    return render(request, 'educator/create_task.html', context=context)
                except Answer.DoesNotExist:
                    tasks = Task.objects.get(test_id=test_id)
                    form_task = TaskForm(instance=tasks)
                    context = {
                        'menu': menu_educator,
                        'form': form,
                        'form_test': form_test,
                        'form_task': form_task,
                        'name': current_user.full_name,
                    }
                    return render(request, 'educator/create_task.html', context=context)
    else:
        return HttpResponseRedirect(reverse('declined_area'))


def set_marks(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(MyUser, pk=request.user.id)
        if current_user.is_educator is True:
            if request.method == 'POST':
                form = CreateMarkForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    student = Student.objects.get(user=data['student'])
                    subject = Subjects.objects.get(subject_name=data['subject'])
                    mark = data['mark']
                    educator = educator_recognizer(current_user.pk)
                    setted_mark = Marks.objects.create(student=student,
                                                       subject=subject,
                                                       mark=mark,
                                                       setted_by=educator)
                    setted_mark.save()
                    return HttpResponse('saved')
            else:
                form = CreateMarkForm()
                context = {
                    'menu': menu_educator,
                    'form': form,
                    'name': current_user.full_name,
                }
                return render(request, 'educator/set_marks.html', context=context)
    else:
        return HttpResponseRedirect(reverse('declined_area'))


def show_tests(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(MyUser, pk=request.user.id)
        if current_user.is_educator is True:
            tests = Test.objects.all()
            context = {
                'menu': menu_educator,
                'tests': tests,
                'name': current_user.full_name,
            }
            return render(request, 'educator/show_tests.html', context=context)
    else:
        return HttpResponseRedirect(reverse('declined_area'))


def chat_page(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    current_user = get_object_or_404(MyUser, pk=request.user.id)
    if current_user.is_educator is True:
        menu = menu_educator
    elif current_user.is_student is True:
        menu = menu_student
    context = {
        'menu': menu,
        'name': current_user.full_name,
    }
    return render(request, "chat/chat_page.html", context)
