from django.urls import path
from django.contrib.auth.views import LoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', view=LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True,
    ), name='login'),
]