from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('list/', views.users_list, name='users_list'),
    path('add-admin/<int:user_id>/', views.add_admin_role, name='add_admin_role'),
    path('remove-admin/<int:user_id>/', views.remove_admin_role, name='remove_admin_role'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add/', views.add_user, name='add_user'),
] 