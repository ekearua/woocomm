"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

admin.site.site_header = 'Waraqata Admin'
admin.site.site_title = 'Waraqata Admin'
#admin.site.site_url = 'http://admin.waraqata.com/'
admin.site.index_title = 'Waraqata Administration'
admin.empty_value_display = '**Empty**'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('accounts/',include(('accounts.urls','django.contrib.auth.urls'),namespace='accounts')),
    path('orders/',include('dash.urls',namespace='orders')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('thanks/',views.ThanksPage.as_view(),name='thanks'),
    path('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset'),
    path('admin/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='admin_password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='admin_password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='admin_password_reset_complete'),
    path('admin/', admin.site.urls),
    path('carts/',include('carts.urls',namespace='carts')),
    path('products/',include('products.urls',namespace='products'))
]
