from django.urls import path

from . import views
app_name = 'core'
urlpatterns = [
    # path("login/", views.userLogin, name="login"),
    path("dashboard/", views.getDashBoard, name="dashboard"),
    # path("logout/", views.userLogout, name="logout"),
    # path("register/", views.userRegistration, name="register")
    # path("login/", views.userLogin, name="login")
]
