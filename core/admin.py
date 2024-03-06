from django.contrib import admin
from .models import Server, Log,Technician

admin.site.register(Server)
admin.site.register(Technician)
admin.site.register(Log)
# Register your models here.
