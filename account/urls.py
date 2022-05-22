from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.registrationPage, name='registrationPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('account/', views.accountPage, name='accountPage'),
    path('account/details/', views.createUpdateUserDetails,
         name='createUpdateUserDetails'),
    path('account/address/', views.createUpdateUserAddress,
         name='createUpdateUserAddress'),
    path('account/card/', views.createUpdateUserCard,
         name='createUpdateUserCard'),
]
