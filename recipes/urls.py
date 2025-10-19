from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('login/', views.login_page, name="login_page"),
    path('signup/', views.signup_page, name="signup_page"),
    path('logout/', views.logout_view, name="logout_page"),
    path('update/<int:id>/', views.update_recipe, name='update_recipe'),
    path('delete/<int:id>/', views.delete_recipe, name='delete_recipe'),
    path('auth-receiver/', views.auth_receiver, name="auth_receiver"),
]
