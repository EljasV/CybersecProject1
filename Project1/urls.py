"""
URL configuration for Project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from Project1.views import index_view, send_view, delete_view, new_account_view, new_account_submit_view, \
    LoggingLoginView

urlpatterns = [
    path('', index_view),
    path('send', send_view),
    path('delete', delete_view),

    #Logging in without logs being made. Use lower line for logging.
    path('login/', LoginView.as_view(template_name="login.html")),
    #path('login/', LoggingLoginView.as_view(template_name="login.html")),
    path('logout/', LogoutView.as_view(next_page="/")),
    path("new_account", new_account_view),
    path("new_account_submit", new_account_submit_view),
    path('admin/', admin.site.urls),

]
