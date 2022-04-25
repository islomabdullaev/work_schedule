from django.urls import path

from authentication.views import RegisterView

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
]
