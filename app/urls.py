from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
    path('index/', view=views.Home.as_view(), name='index'),
]