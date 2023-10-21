from django.urls import path

from . import views as V

urlpatterns = [
    path('', V.ChatView.as_view(), name='home'),
    path('login/', V.MyLoginView.as_view(), name='login'),
    path('logout/', V.MyLogOutView.as_view(), name='logout'),
    path('register/', V.RegisterView.as_view(), name='register'),
]
