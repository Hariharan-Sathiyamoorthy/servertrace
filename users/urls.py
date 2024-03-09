from django.urls import path

from . import views
app_name = 'users'
urlpatterns = [
    path("login/", views.userLogin, name="login"),
    path("logout/", views.userLogout, name="logout"),
    path("register/", views.userRegistration, name="register"),
    path("get_users/", views.getUsers, name="get_users"),
    path("edit_user/<int:id>/", views.userEdit, name="edit_user"),
    path("delete_user/<int:id>/", views.userDelete, name="delete_user"),
    path("profile/", views.userProfileEdit, name="profile"),

    # path("login/", views.userLogin, name="login")
]
