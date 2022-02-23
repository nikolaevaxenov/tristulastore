from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.registrationPage, name='registrationPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('account/', views.accountPage, name='accountPage'),
]
