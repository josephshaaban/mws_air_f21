"""mws_air_s21 URL Configuration

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
from django.urls import path

from air_app.views import data_entry_view, home_view, search_query_view, display_question_view

urlpatterns = [
    # todo: home page.
    path('', home_view, name='home'),
    path('enter-Q&A/', data_entry_view, name='data_entry'),
    path('search/', search_query_view, name='search_query'),
    path('question/<pk>/', display_question_view, name='display_question')
]
