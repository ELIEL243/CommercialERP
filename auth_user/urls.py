from django.urls import path
from .views import LoginView, Logout

urlpatterns = [
    path('', LoginView, name="login"),
    path('logout/', Logout, name="logout"),
]