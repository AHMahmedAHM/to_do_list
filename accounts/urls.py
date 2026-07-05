from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    #customised
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.custom_logout, name='logout'), 

    #fixed
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #uidb64 لمعرفة المستخدم ، <token> علشان يعرف انه استخدم مثلا قبل كده 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
