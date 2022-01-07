from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('password_reset/',views.password_reset,name='password_reset'),
    path('password_reset/done/',views.password_reset_done,name='password_reset_done',),
    path('reset/<uidb64>/<token>/',views.password_reset_confirm,name='password_reset_confirm',),
    path('reset/done/',views.password_reset_complete,name='password_reset_complete',),
    path('password_change',views.password_change,name='password_change'),
    path('password_change/done',views.password_change_done,name='password_change_done'),
]
