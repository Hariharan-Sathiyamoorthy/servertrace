from django.urls import path

from . import views
app_name = 'server'
urlpatterns = [
    path("", views.laodLandingPage, name="laodLandingPage"),
    path("send_email/", views.send_email, name="send_email"),
]
