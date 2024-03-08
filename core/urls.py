from django.urls import path

from . import views
app_name = 'core'
urlpatterns = [
    # Dashboard,
    path("dashboard/", views.getDashBoard, name="dashboard"),
    # Servers
    path("create/", views.createServer, name="create"),
    path("editServer/<int:id>/", views.updateServer, name="update"),
    path("deleteServer/<int:id>/", views.deleteServer, name="delete"),
    path("get_servers/", views.getServers, name="get_servers"),
    path("get_server/<int:id>/", views.viewServer, name="get_a_server"),
    # Logs
    path("get_logs/", views.getLogs, name="logs"),
    path("create_log/", views.createLog, name="create_log"),
    path("edit_log/<int:id>/", views.editLog, name="edit_log"),
    path("delete_log/<int:id>/", views.deleteLog, name="delete_log"),
    # Technicians
    path("get_technicians/", views.getTechnicians, name="get_technicians"),
    path("create_technician/", views.createTechnician, name="create_technician"),
    path("edit_technician/<int:id>/", views.editTechnician, name="edit_technician"),
    path("delete_technician/<int:id>/", views.deleteTechnician, name="delete_technician"),
]
