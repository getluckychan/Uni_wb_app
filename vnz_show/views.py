import json

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import ModelFormMixin

from .forms import *
from .utils import *


# TODO: create a new view for index page

def find_if_student(user):
    user = get_object_or_404(MyUser, pk=user.pk)
    if user.is_student:
        return HttpResponseRedirect(reverse('declined_area'))


def index(request):
    if not request.user.is_authenticated:
        contex = {
            'menu': menu_not_login,
            'title': 'Home page'
        }
        return HttpResponseRedirect(reverse('login'))

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


class MyProfileView(ListView, LoginRequiredMixin):
    template_name = 'home/profile.html'

    def get_queryset(self):
        self.user = get_object_or_404(MyUser, pk=self.request.user.id)
        return MyUser.objects.filter(id=self.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user.is_student:
            context['menu'] = menu_student
            context['info'] = Student.objects.get(user_id=self.user.id)
            context['job'] = 'Student'
        elif self.user.is_educator:
            context['job'] = 'Educator'
            context['info'] = Educator.objects.get(user_id=self.user.id)
            context['menu'] = menu_educator
        context['title'] = 'My profile'
        context['user'] = self.user
        context['name'] = self.user.full_name
        return context


class EditMyProfileView(LoginRequiredMixin, UpdateView):
    model = MyUser
    template_name = 'home/edit_profile.html'
    # form_class = EditMyProfileForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_student:
            context['menu'] = menu_student
        elif self.request.user.is_educator:
            context['menu'] = menu_educator
        context['title'] = 'Edit profile'
        context['name'] = self.request.user.full_name
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(MyUser, pk=self.request.user.id)

    def form_valid(self, form):
        form.save()
        return redirect('/')


class ProfileView(ListView, LoginRequiredMixin):
    template_name = 'home/profile_of_user.html'

    def dispatch(self, request, *args, **kwargs):
        self.auth_user = get_object_or_404(MyUser, pk=request.user.id)
        if request.user.id == self.kwargs['user_id']:
            return HttpResponseRedirect(reverse('my_profile'))
        if request.user.is_educator:
            self.menu = menu_educator
        elif request.user.is_student:
            self.menu = menu_student
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.user = get_object_or_404(MyUser, pk=self.kwargs['user_id'])
        return MyUser.objects.filter(id=self.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user.is_student:
            context['job'] = 'Student'
            info = Student.objects.get(user_id=self.user.id)
        elif self.user.is_educator:
            context['job'] = 'Educator'
            info = Educator.objects.get(user_id=self.user.id)
        context['info'] = info
        context['menu'] = self.menu
        context['title'] = 'Profile'
        context['user'] = self.auth_user
        context['searched_user'] = self.user
        context['name'] = self.request.user.full_name
        return context


# def search_results(request):
#     if request.accepts("application/json"):
#         search = request.POST.get('data')
#         print(search)
#         return JsonResponse({'search': search})

class MyUserSearchView(View):
    def post(self, request, *args, **kwargs):
        context = {}
        if request.accepts("application/json"):
            res = None
            search_query = request.POST.get("data")
            qs = MyUser.objects.filter(full_name__icontains=search_query)
            if len(search_query) and len(qs):
                data = []
                for i in qs:
                    searched_user = get_object_or_404(MyUser, pk=i.id)
                    if searched_user.is_student:
                        job = 'Student'
                    elif searched_user.is_educator:
                        job = 'Educator'
                    item = {
                        'pk': i.pk,
                        'full_name': i.full_name,
                        'job': job,
                        'avatar': str(i.avatar.url if i.avatar else None),
                    }
                    data.append(item)
                res = data
            else:
                res = 'No results'

            return JsonResponse({'search': res})
        return JsonResponse({})



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


class SignUpView(CreateView):
    # registration view
    form_class = UserCreateForm
    success_url = '/signup-as/'
    template_name = 'registration/registration.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # check if user is student or educator
        if user.is_student is True:
            return HttpResponseRedirect(reverse('sign_up_student', args=[user.pk]))
        elif user.is_educator is True:
            return HttpResponseRedirect(reverse('sign_up_educator', args=[user.pk]))
        return redirect('my_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_not_login
        context['title'] = 'Registration'
        return context


class SignUpStudentView(CreateView):
    # create student profile
    form_class = SignUpAsStudentForm
    success_url = '/my-profile/'
    template_name = 'registration/as_student.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        return super(SignUpStudentView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = get_object_or_404(MyUser, pk=self.kwargs['user_id'])
        form.instance.user = user
        form.save()
        return redirect('my_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_not_login
        context['title'] = 'Registration'
        return context


class SignUpEducatorView(CreateView):
    # create educator profile
    form_class = SignUpAsEducatorForm
    success_url = '/my_profile/'
    template_name = 'registration/as_educator.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        return super(SignUpEducatorView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = get_object_or_404(MyUser, pk=self.request.user.id)
        form.instance.user = user
        form.save()
        return redirect('my_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_not_login
        context['title'] = 'Registration'
        return context


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class LoginPageView(View):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('my_profile')
        form = self.form_class()
        message = ''
        context = {
            'form': form,
            'menu': menu_not_login,
            'title': 'Login',
            'message': message
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('index')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


class CreateTestView(CreateView):
    form_class = CreateTestForm
    template_name = 'educator/create_test.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        self.user = get_object_or_404(MyUser, pk=self.request.user.id)
        if self.user.is_educator is False:
            return HttpResponseRedirect(reverse('declined_area'))
        return super(CreateTestView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        educator = educator_recognizer(self.user)
        form.instance.author = educator
        new_test = form.save()
        object_of_test = Test.objects.get(id=new_test.id).pk
        return HttpResponseRedirect(reverse('create_task', args=[object_of_test]))

    def get_context_data(self, **kwargs):
        # form = CreateTestForm(instance=)
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_educator
        context['title'] = 'Create test'
        context['name'] = self.user.full_name
        return context


class CreateTaskView(CreateView):
    form_class = TaskForm
    template_name = 'educator/create_task.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        self.user = get_object_or_404(MyUser, pk=self.request.user.id)
        if self.user.is_educator is False:
            return HttpResponseRedirect(reverse('declined_area'))
        return super(CreateTaskView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        test = get_object_or_404(Test, pk=self.kwargs['test_id'])
        form.instance.test = test
        new_task = form.save()
        object_of_task = Task.objects.get(id=new_task.id).pk
        return HttpResponseRedirect(reverse('create_answer', args=[object_of_task]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_educator
        context['title'] = 'Create task'
        context['name'] = self.user.full_name
        try:
            context['test'] = Test.objects.get(pk=self.kwargs['test_id'])
            context['tasks'] = Task.objects.filter(test=self.kwargs['test_id'])
            context['answers'] = Answer.objects.filter(task__test=self.kwargs['test_id'])
        except Test.DoesNotExist:
            context['test'] = None
        except Task.DoesNotExist:
            context['tasks'] = None
        except Answer.DoesNotExist:
            context['answers'] = None
        return context


class CreateAnswerView(CreateView):
    form_class = AnswerForm
    success_url = '/create_task/'
    template_name = 'educator/create_answer.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        self.user = get_object_or_404(MyUser, pk=self.request.user.id)
        if self.user.is_educator is False:
            return HttpResponseRedirect(reverse('declined_area'))
        return super(CreateAnswerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        form.instance.task = task
        form.save()
        if 'add_another' in self.request.POST:
            return HttpResponseRedirect(reverse('create_answer', args=[self.kwargs['task_id']]))
        elif 'add_task' in self.request.POST:
            return HttpResponseRedirect(reverse('create_task', args=[task.test.id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_educator
        context['title'] = 'Create answer'
        context['name'] = self.user.full_name
        try:
            context['task'] = Task.objects.get(pk=self.kwargs['task_id'])
            context['answers'] = Answer.objects.filter(task=self.kwargs['task_id'])
        except Task.DoesNotExist:
            context['task'] = None
        except Answer.DoesNotExist:
            context['answers'] = None
        return context


class CreateMarkView(CreateView):
    form_class = CreateMarkForm
    template_name = 'educator/set_marks.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        self.user = get_object_or_404(MyUser, pk=self.request.user.id)
        if self.user.is_educator is False:
            return HttpResponseRedirect(reverse('declined_area'))
        return super(CreateMarkView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        educator = Educator.objects.get(get_object_or_404(MyUser, pk=self.request.user.id))
        group = Groups.objects.get(curator=educator)
        student = Student.objects.get_queryset(group=group)
        form.instance.setted_by = educator
        form.instance.student = student
        form.save()
        return HttpResponseRedirect(reverse('set_marks'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_educator
        context['title'] = 'Create mark'
        context['name'] = self.user.full_name
        return context


class ShowTestsView(ListView):
    model = Test
    template_name = 'educator/show_tests.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        self.user = get_object_or_404(MyUser, pk=self.request.user.id)
        if self.user.is_educator is False:
            return HttpResponseRedirect(reverse('declined_area'))
        return super(ShowTestsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        self.educator = educator_recognizer(self.request.user.id)
        return Test.objects.filter(author=self.educator)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_educator
        context['title'] = 'Show tests'
        context['name'] = self.user.full_name
        return context


class ShowDetailTestView(DetailView):
    model = Test
    template_name = 'educator/show_detail_test.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        self.user = get_object_or_404(MyUser, pk=self.request.user.id)
        if self.user.is_educator is False:
            return HttpResponseRedirect(reverse('declined_area'))
        return super(ShowDetailTestView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu_educator
        context['title'] = 'Show detail test'
        context['name'] = self.user.full_name
        try:
            context['tasks'] = Task.objects.filter(test=self.kwargs['pk'])
            context['answers'] = Answer.objects.filter(task__test=self.kwargs['pk'])
        except Task.DoesNotExist:
            context['tasks'] = None
        except Answer.DoesNotExist:
            context['answers'] = None
        return context


def get_courses_for_student(request, *args, **kwargs):
    if request.method == 'GET':
        speciality = request.GET.get('speciality')
        subjects = Subjects.objects.filter(speciality=speciality)
        return JsonResponse({'subjects': list(subjects.values())})


def get_marks_for_student(request, *args, **kwargs):
    if request.method == 'GET':
        student = request.GET.get('student')
        marks = Marks.objects.filter(student=student)
        return JsonResponse({'marks': list(marks.values())})
