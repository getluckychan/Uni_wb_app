from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, CreateView

from vnz_show.utils import *
from . import consumers
from .forms import *
from .models import *


@login_required(login_url='login')
def index(request):
    user = get_object_or_404(MyUser, pk=request.user.pk)
    if user.is_student:
        menu = menu_student
    elif user.is_educator:
        menu = menu_educator
    return render(request, "chat/chat_page.html", {"menu": menu, 'name': user.full_name})


# class UserSearchForChatView(LoginRequiredMixin, FormView):
#     form_class = SearchForm
#     template_name = "chat/user_search.html"
#     login_url = 'login'
#
#     def form_valid(self, form):
#         user = get_object_or_404(MyUser, pk=self.request.user.pk)
#         form = form.cleaned_data
#         search = form['search']
#         searched_users = MyUser.objects.filter(Q(full_name__icontains=search) | Q(username__icontains=search))
#         if user.is_student:
#             menu = menu_student
#         elif user.is_educator:
#             menu = menu_educator
#         return render(self.request, "chat/user_search.html", {"menu": menu,
#                                                               'name': user.full_name,
#                                                               "users": searched_users})
#
#     def form_invalid(self, form):
#         return redirect("chat_main")


@login_required(login_url='login')
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "chat/room_list.html"
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(MyUser, pk=self.request.user.pk)
        if user.is_student:
            menu = menu_student
        elif user.is_educator:
            menu = menu_educator
        context["menu"] = menu
        context["name"] = user.full_name
        return context