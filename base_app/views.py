from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .models import Message, User


class MyLoginView(LoginView):
    template_name = "auth.html"
    redirect_authenticated_user = True
    extra_context = {'is_login': True}

    def get_success_url(self) -> str:
        return reverse('home')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth.html"
    model = User
    success_url = reverse_lazy('home')

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginCheckMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')


class MyLogOutView(LoginCheckMixin, LogoutView):

    def get_success_url(self) -> str:
        return reverse('login')


class ChatView(LoginCheckMixin, ListView):
    model = Message
    template_name = 'chat.html'
    context_object_name = 'messages'

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.messages.all()

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        if content:
            Message.objects.create(content=content,
                                   owner=request.user)
        return redirect('home')
